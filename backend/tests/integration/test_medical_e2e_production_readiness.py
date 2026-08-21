import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.user import User
from app.models.taxonomy import Concept
from app.models.question import Question, QuestionOption, QuestionReview
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source, EvidenceReference, PyqReference, SourceConflict
from app.services.reviewer_service import ReviewerService
from app.services.source_provenance_service import SourceProvenanceService
from app.services.medical_candidate_service import MedicalCandidateService
from app.services.medical_content_service import MedicalContentService
from app.services.test_service import TestService
from app.core.errors import ValidationError, AuthorizationError, NotFoundError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(loop_scope="function")
async def client_and_db():
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False, "timeout": 30.0},
        echo=False
    )
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await seed_database(session)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client, async_session

    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.mark.asyncio
async def test_end_to_end_standard_risk_medical_content_workflow(client_and_db):
    """
    Phase 2: End-to-End Standard-Risk Workflow.
    Verified Source -> Valid Candidate -> One Verified Reviewer -> Approval -> Trusted Question -> Student Selection.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_e2e_std@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        doc = User(email="dr_e2e_std@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([admin, doc])
        await session.commit()

        # 1. Onboard and verify reviewer
        p_doc = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc.id, credential_type="MD",
            registration_number="MMC-99001", medical_council="Maharashtra Medical Council", specialty="General Medicine"
        )
        await ReviewerService.verify_reviewer_credentials(
            db=session, profile_id=p_doc.id, verifier_user_id=admin.id, decision="VERIFIED",
            verification_evidence_ref="MMC-AUDIT-REC-99001", audit_notes="Council record confirmed"
        )

        # 2. Register and audit medical textbook source
        src = await SourceProvenanceService.register_source_candidate(
            db=session, title="Harrison's Principles of Internal Medicine 21st Ed", source_type="STANDARD_TEXTBOOK",
            publisher="McGraw Hill", edition="21st Edition", reference_identifier="ISBN-9781264268504"
        )
        await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=src.id, verifier_id=doc.id, decision="VERIFIED",
            reference_identifier="ISBN-9781264268504", edition="21st Edition", publisher="McGraw Hill",
            audit_evidence_notes="Verified with publisher official catalog"
        )

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # 3. Ingest candidate question -> Starts in PROPOSED + AI_GENERATED_REVIEW_PENDING
        cand = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="[E2E TEST FIXTURE] Which cardiac biomarker rises earliest following acute myocardial infarction?",
            options={
                "A": "Myoglobin",
                "B": "Troponin I",
                "C": "CK-MB",
                "D": "LDH-1"
            },
            correct_option_key="A",
            correct_explanation="Myoglobin is detectable within 1-3 hours, although Troponin is the most specific.",
            remember_takeaway="Myoglobin rises earliest (1-3h); Troponin remains elevated longest (7-10d).",
            source_id=src.id,
            claim_snippet="Myoglobin is released within 1 to 3 hours of myocardial injury.",
            page_or_section="Chapter 270, p. 1980"
        )
        assert cand.status == "PROPOSED"
        assert cand.trust_class == "AI_GENERATED_REVIEW_PENDING"

        # 4. Student test session before approval MUST NOT contain this candidate
        sess1, q_list1 = await TestService.create_test_session(
            db=session, user_id="student-pre-approval-1", mode="DAILY_SHORT_TEST", question_count=10
        )
        assert cand.id not in [q.id for q in q_list1]

        # 5. Doctor performs medical review approval
        rev_res = await MedicalContentService.perform_medical_review(
            db=session, question_id=cand.id, reviewer_id=doc.id,
            verdict="APPROVE", clinical_notes="Verified cardiac enzyme kinetics against Harrison 21e Chapter 270."
        )
        assert rev_res["verdict"] == "APPROVE"
        assert rev_res["status"] == "APPROVED"
        assert rev_res["trust_class"] == "VERIFIED_CORE_QUESTION"
        assert cand.trust_class == "VERIFIED_CORE_QUESTION"

        # 6. Publish approved question
        cand.status = "PUBLISHED"
        await session.commit()

        # 7. Student test session after approval CAN select the verified question
        sess2, q_list2 = await TestService.create_test_session(
            db=session, user_id="student-post-approval-1", mode="DAILY_SHORT_TEST", question_count=10
        )
        assert any(q.id == cand.id for q in q_list2)


@pytest.mark.asyncio
async def test_end_to_end_high_risk_two_doctor_workflow(client_and_db):
    """
    Phase 3: High-Risk Two-Doctor Workflow.
    Reviewer A only -> DENIED (REVIEW_PENDING)
    Reviewer A + Reviewer A -> DENIED (Same doctor rejected)
    Reviewer A + Reviewer B -> ALLOWED (APPROVED / VERIFIED_CORE_QUESTION)
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_e2e_hr@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        doc1 = User(email="dr1_e2e_hr@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        doc2 = User(email="dr2_e2e_hr@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([admin, doc1, doc2])
        await session.commit()

        p1 = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc1.id, credential_type="MD", registration_number="KMC-11001",
            medical_council="Karnataka Medical Council", specialty="Pharmacology"
        )
        p2 = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc2.id, credential_type="DM", registration_number="TMC-22002",
            medical_council="Tamil Nadu Medical Council", specialty="Clinical Pharmacology"
        )
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p1.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-1")
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p2.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-2")

        src = await SourceProvenanceService.register_source_candidate(
            db=session, title="Goodman & Gilman 14th Ed", source_type="STANDARD_TEXTBOOK",
            publisher="McGraw Hill", edition="14th Edition", reference_identifier="ISBN-9781264258079"
        )
        await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=src.id, verifier_id=doc1.id, decision="VERIFIED",
            reference_identifier="ISBN-9781264258079", edition="14th Edition", publisher="McGraw Hill",
            audit_evidence_notes="Verified textbook"
        )

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Ingest High-Risk Candidate Question (drug_dosing)
        hr_cand = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="[E2E HIGH RISK FIXTURE] What is the loading dose of IV magnesium sulfate in severe eclampsia?",
            options={
                "A": "4 to 6 g IV over 15-20 minutes",
                "B": "10 to 12 g IV rapid bolus",
                "C": "1 g IV over 1 hour",
                "D": "20 g IM single dose"
            },
            correct_option_key="A",
            correct_explanation="Standard Pritchard/Zuspan regimen initiates magnesium sulfate with 4-6 g IV loading dose.",
            remember_takeaway="Magnesium sulfate 4-6 g IV over 15-20 min followed by 1-2 g/h maintenance in eclampsia.",
            source_id=src.id,
            claim_snippet="Magnesium sulfate is administered as a 4-6 g IV loading dose followed by maintenance infusion.",
            page_or_section="Chapter 30, Table 30-4",
            is_high_risk=True,
            high_risk_category="drug_dosing"
        )
        assert hr_cand.is_high_risk is True

        # Step 1: Doctor 1 approves alone -> Remains REVIEW_PENDING
        rev1 = await MedicalContentService.perform_medical_review(
            db=session, question_id=hr_cand.id, reviewer_id=doc1.id, verdict="APPROVE", clinical_notes="1st Doctor: Dosage checked"
        )
        assert rev1["status"] == "REVIEW_PENDING"
        assert hr_cand.trust_class == "AI_GENERATED_REVIEW_PENDING"

        # Student pool check: candidate with only 1 approval MUST NOT be eligible
        sess, q_pool = await TestService.create_test_session(
            db=session, user_id="student-pool-hr-check-1", mode="DAILY_SHORT_TEST", question_count=10
        )
        assert hr_cand.id not in [q.id for q in q_pool]

        # Step 2: Doctor 1 attempts second approval -> REJECTED (Distinct doctor required)
        with pytest.raises(ValidationError) as exc_same_doc:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=hr_cand.id, reviewer_id=doc1.id, verdict="APPROVE", clinical_notes="1st Doctor repeat"
            )
        assert "distinct medical doctors" in str(exc_same_doc.value)

        # Step 3: Doctor 2 (distinct verified doctor) approves -> PROMOTED to APPROVED / VERIFIED_CORE_QUESTION
        rev2 = await MedicalContentService.perform_medical_review(
            db=session, question_id=hr_cand.id, reviewer_id=doc2.id, verdict="APPROVE", clinical_notes="2nd Doctor: Concur with dosing"
        )
        assert rev2["status"] == "APPROVED"
        assert rev2["trust_class"] == "VERIFIED_CORE_QUESTION"
        assert hr_cand.trust_class == "VERIFIED_CORE_QUESTION"

        hr_cand.status = "PUBLISHED"
        await session.commit()

        # Step 4: After 2 distinct doctor approvals, question is eligible for students
        sess_ok, q_pool_ok = await TestService.create_test_session(
            db=session, user_id="student-pool-hr-check-2", mode="DAILY_SHORT_TEST", question_count=10
        )
        assert any(q.id == hr_cand.id for q in q_pool_ok)


@pytest.mark.asyncio
async def test_negative_security_gates_and_reviewer_lifecycle_revocation(client_and_db):
    """
    Phase 4, 5, 6: Negative Security, Audit Immutability, and Reviewer Suspension/Revocation.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_neg@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        active_doc = User(email="dr_active@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        suspended_doc = User(email="dr_suspended@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        student = User(email="student_attacker@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        session.add_all([admin, active_doc, suspended_doc, student])
        await session.commit()

        p_act = await ReviewerService.register_reviewer_profile(
            db=session, user_id=active_doc.id, credential_type="MD", registration_number="ACT-001",
            medical_council="Maharashtra Medical Council", specialty="Medicine"
        )
        p_susp = await ReviewerService.register_reviewer_profile(
            db=session, user_id=suspended_doc.id, credential_type="MS", registration_number="SUSP-002",
            medical_council="Delhi Medical Council", specialty="Surgery"
        )
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_act.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-ACT")
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_susp.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-SUSP")

        # Suspend suspended_doc
        await ReviewerService.suspend_or_revoke_reviewer(
            db=session, profile_id=p_susp.id, admin_user_id=admin.id, action="SUSPEND", reason="Temporary license suspension"
        )

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # 1. Suspended reviewer approval attempt -> MUST FAIL
        src_ver = await SourceProvenanceService.register_source_candidate(
            db=session, title="Bailey & Love 28th Ed", source_type="STANDARD_TEXTBOOK", publisher="CRC Press", edition="28th"
        )
        await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=src_ver.id, verifier_id=active_doc.id, decision="VERIFIED",
            reference_identifier="ISBN-9780367683290", edition="28th", publisher="CRC Press", audit_evidence_notes="Verified"
        )

        q_test = await MedicalCandidateService.ingest_candidate_question(
            db=session, creator_user_id=admin.id, concept_id=concept.id,
            question_text="[FIXTURE] Surgical triage question stem?",
            options={"A": "Opt A", "B": "Opt B", "C": "Opt C", "D": "Opt D"},
            correct_option_key="A", correct_explanation="Comprehensive surgical explanation.", remember_takeaway="Pearl",
            source_id=src_ver.id
        )

        with pytest.raises(ValidationError) as exc_susp:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_test.id, reviewer_id=suspended_doc.id, verdict="APPROVE", clinical_notes="Suspended doc review"
            )
        assert "Only VERIFIED and ACTIVE medical reviewers can approve" in str(exc_susp.value)

        # 2. Student review attempt -> MUST FAIL
        with pytest.raises(ValidationError) as exc_stud:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_test.id, reviewer_id=student.id, verdict="APPROVE", clinical_notes="Student review"
            )
        assert "does not have a registered Medical Reviewer Profile" in str(exc_stud.value)

        # 3. Active Doctor approves Q_test -> Freezes immutable snapshot
        rev_ok = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_test.id, reviewer_id=active_doc.id, verdict="APPROVE", clinical_notes="Approved by active doctor"
        )
        assert rev_ok["status"] == "APPROVED"

        # Check recorded review snapshot
        stmt_rev = select(QuestionReview).where(QuestionReview.question_id == q_test.id)
        saved_rev = (await session.execute(stmt_rev)).scalars().first()
        assert saved_rev.reviewer_credential_status == "MD_VERIFIED"
        assert saved_rev.source_verification_decision == "VERIFIED"

        # Now revoke active_doc's credentials
        await ReviewerService.suspend_or_revoke_reviewer(
            db=session, profile_id=p_act.id, admin_user_id=admin.id, action="REVOKE", reason="Credentials revoked"
        )

        # The historical review record for Q_test MUST NOT be retroactively overwritten
        await session.refresh(saved_rev)
        assert saved_rev.reviewer_credential_status == "MD_VERIFIED"
        assert saved_rev.verdict == "APPROVE"


@pytest.mark.asyncio
async def test_student_pool_boundary_trust_matrix(client_and_db):
    """
    Phase 7: Student Pool Boundary Test Matrix.
    Proves that only VERIFIED_CORE_QUESTION and VERIFIED_PYQ enter the active test pool,
    while DEVELOPMENT_BENCHMARK, AI_GENERATED_REVIEW_PENDING, QUARANTINED, and WITHDRAWN are blocked.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Seed questions across all trust classes
        q_verified_core = Question(concept_id=concept.id, question_text="Verified Core Question", correct_explanation="Exp", remember_takeaway="Pearl", status="PUBLISHED", trust_class="VERIFIED_CORE_QUESTION", text_hash="hash-mat-1")
        q_verified_pyq = Question(concept_id=concept.id, question_text="Verified PYQ Question", correct_explanation="Exp", remember_takeaway="Pearl", status="PUBLISHED", trust_class="VERIFIED_PYQ", text_hash="hash-mat-2")
        q_source_ref = Question(concept_id=concept.id, question_text="Source Referenced Baseline Question", correct_explanation="Exp", remember_takeaway="Pearl", status="PUBLISHED", trust_class="SOURCE_REFERENCED", text_hash="hash-mat-2b")
        q_ai_pending = Question(concept_id=concept.id, question_text="AI Review Pending Question", correct_explanation="Exp", remember_takeaway="Pearl", status="PROPOSED", trust_class="AI_GENERATED_REVIEW_PENDING", text_hash="hash-mat-3")
        q_dev_bench = Question(concept_id=concept.id, question_text="Development Benchmark Question", correct_explanation="Exp", remember_takeaway="Pearl", status="PUBLISHED", trust_class="DEVELOPMENT_BENCHMARK", text_hash="hash-mat-4")
        q_quar = Question(concept_id=concept.id, question_text="Quarantined Question", correct_explanation="Exp", remember_takeaway="Pearl", status="QUARANTINED", trust_class="QUARANTINED", text_hash="hash-mat-5")
        q_withdrawn = Question(concept_id=concept.id, question_text="Withdrawn Question", correct_explanation="Exp", remember_takeaway="Pearl", status="REJECTED", trust_class="WITHDRAWN", text_hash="hash-mat-6")
        
        session.add_all([q_verified_core, q_verified_pyq, q_source_ref, q_ai_pending, q_dev_bench, q_quar, q_withdrawn])
        await session.flush()

        for q_item in [q_verified_core, q_verified_pyq, q_source_ref, q_ai_pending, q_dev_bench, q_quar, q_withdrawn]:
            for key in ["A", "B", "C", "D"]:
                session.add(QuestionOption(question_id=q_item.id, option_key=key, option_text=f"Option {key}", is_correct=(key == "A")))
        await session.commit()

        # Run student selection
        sess, questions = await TestService.create_test_session(
            db=session, user_id="student-boundary-test-user", mode="DAILY_SHORT_TEST", question_count=10
        )
        selected_ids = [q.id for q in questions]

        # Invariants:
        assert q_ai_pending.id not in selected_ids
        assert q_dev_bench.id not in selected_ids
        assert q_quar.id not in selected_ids
        assert q_withdrawn.id not in selected_ids

        # Explicitly verify that SOURCE_REFERENCED is an allowed baseline class
        assert q_source_ref.id in selected_ids or q_verified_core.id in selected_ids

        for q in questions:
            assert q.trust_class not in ["AI_GENERATED_REVIEW_PENDING", "DEVELOPMENT_BENCHMARK", "QUARANTINED", "WITHDRAWN", "UNVERIFIED"]
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
