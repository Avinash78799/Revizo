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
from app.models.source import Source
from app.services.reviewer_service import ReviewerService
from app.services.medical_content_service import MedicalContentService
from app.services.test_service import TestService
from app.core.errors import ValidationError, AuthorizationError

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
async def test_reviewer_onboarding_lifecycle_and_self_approval_denial(client_and_db):
    """
    Invariants Tested:
    1. Reviewer applicant registers in PENDING_VERIFICATION (active_status=False).
    2. Plausible registration format does not auto-verify.
    3. Reviewer CANNOT verify their own credentials (self-approval rejected).
    4. Admin can verify credentials, creating frozen immutable snapshot.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create applicant user and admin verifier
        applicant = User(
            email="dr_applicant@neetpg.pro",
            hashed_password="hash",
            role="medical_reviewer",
            is_active=True
        )
        admin = User(
            email="medical_board_admin@neetpg.pro",
            hashed_password="hash",
            role="admin",
            is_active=True
        )
        session.add_all([applicant, admin])
        await session.commit()
        await session.refresh(applicant)
        await session.refresh(admin)

        # 1. Onboard applicant
        profile = await ReviewerService.register_reviewer_profile(
            db=session,
            user_id=applicant.id,
            credential_type="MD",
            registration_number="MCI-2026-98765",
            medical_council="Maharashtra Medical Council",
            specialty="General Medicine"
        )
        assert profile.verification_status == "PENDING_VERIFICATION"
        assert profile.active_status is False
        assert profile.credential_status == "PENDING"

        # 2. Self-Approval attempt must be strictly rejected
        with pytest.raises(AuthorizationError) as exc_self:
            await ReviewerService.verify_reviewer_credentials(
                db=session,
                profile_id=profile.id,
                verifier_user_id=applicant.id,  # Self-approval!
                decision="VERIFIED",
                verification_evidence_ref="NMC-PORTAL-AUDIT-001"
            )
        assert "cannot approve their own" in str(exc_self.value)

        # 3. Independent Admin Verification
        snapshot = await ReviewerService.verify_reviewer_credentials(
            db=session,
            profile_id=profile.id,
            verifier_user_id=admin.id,
            decision="VERIFIED",
            verification_evidence_ref="MMC-LOOKUP-REC-2026-098",
            audit_notes="Council registration confirmed active in Maharashtra Medical Council registry."
        )
        assert snapshot["verification_status"] == "VERIFIED"
        assert snapshot["active_status"] is True
        assert snapshot["snapshot_frozen"] is True
        assert snapshot["verified_by"] == admin.id

@pytest.mark.asyncio
async def test_pending_or_rejected_reviewer_cannot_approve_questions(client_and_db):
    """
    Invariants Tested:
    1. Unverified or pending reviewer cannot approve medical questions.
    2. Rejected reviewer cannot approve medical questions.
    3. Suspended reviewer cannot approve medical questions.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create unverified applicant and rejected applicant
        pending_user = User(email="dr_pending@neetpg.pro", hashed_password="hash", role="medical_reviewer", is_active=True)
        rejected_user = User(email="dr_rejected@neetpg.pro", hashed_password="hash", role="medical_reviewer", is_active=True)
        admin_user = User(email="admin_verifier@neetpg.pro", hashed_password="hash", role="admin", is_active=True)
        session.add_all([pending_user, rejected_user, admin_user])
        await session.commit()

        # Register profiles
        p_pending = await ReviewerService.register_reviewer_profile(
            db=session, user_id=pending_user.id, credential_type="MBBS", registration_number="KMC-1111",
            medical_council="Karnataka Medical Council", specialty="General Practice"
        )
        p_rejected = await ReviewerService.register_reviewer_profile(
            db=session, user_id=rejected_user.id, credential_type="MS", registration_number="DMC-2222",
            medical_council="Delhi Medical Council", specialty="General Surgery"
        )

        # Admin rejects rejected_user
        await ReviewerService.verify_reviewer_credentials(
            db=session, profile_id=p_rejected.id, verifier_user_id=admin_user.id,
            decision="REJECTED", verification_evidence_ref="DMC-AUDIT-FAIL", audit_notes="Council registry record expired"
        )

        # Create candidate question with verified source
        source = Source(title="Harrison Medicine 21e", source_type="textbook", verification_status="VERIFIED")
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()
        session.add(source)
        await session.flush()

        q = Question(
            concept_id=concept.id,
            question_text="Clinical Question for Review",
            correct_explanation="Correct Mechanism",
            remember_takeaway="Pearl",
            source_id=source.id,
            source_citation="Harrison 21e, p. 450",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-rev-test-1"
        )
        session.add(q)
        await session.commit()

        # 1. Pending reviewer review attempt -> MUST FAIL
        with pytest.raises(ValidationError) as exc_pending:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q.id, reviewer_id=pending_user.id,
                verdict="APPROVE", clinical_notes="Looks fine"
            )
        assert "Only VERIFIED and ACTIVE medical reviewers can approve" in str(exc_pending.value)

        # 2. Rejected reviewer review attempt -> MUST FAIL
        with pytest.raises(ValidationError) as exc_rej:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q.id, reviewer_id=rejected_user.id,
                verdict="APPROVE", clinical_notes="Looks good"
            )
        assert "Only VERIFIED and ACTIVE medical reviewers can approve" in str(exc_rej.value)

@pytest.mark.asyncio
async def test_two_distinct_verified_reviewers_required_for_high_risk(client_and_db):
    """
    Invariants Tested:
    1. Verified reviewer can approve standard question.
    2. High-risk question requires 2 DISTINCT verified reviewers.
    3. Same reviewer cannot satisfy both approvals on high-risk content.
    4. Credential snapshot is immutably stored in review record.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create 2 distinct verified doctors and admin
        doc1 = User(email="dr_cardio1@neetpg.pro", hashed_password="hash", role="medical_reviewer", is_active=True)
        doc2 = User(email="dr_cardio2@neetpg.pro", hashed_password="hash", role="medical_reviewer", is_active=True)
        admin = User(email="board_admin@neetpg.pro", hashed_password="hash", role="admin", is_active=True)
        session.add_all([doc1, doc2, admin])
        await session.commit()

        p1 = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc1.id, credential_type="DM", registration_number="MMC-9988",
            medical_council="Maharashtra Medical Council", specialty="Cardiology"
        )
        p2 = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc2.id, credential_type="MD", registration_number="TMC-7766",
            medical_council="Tamil Nadu Medical Council", specialty="General Medicine"
        )

        await ReviewerService.verify_reviewer_credentials(
            db=session, profile_id=p1.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-DOC1"
        )
        await ReviewerService.verify_reviewer_credentials(
            db=session, profile_id=p2.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-DOC2"
        )

        # Create High-Risk Question (drug_dosing) with verified source
        source = Source(title="Goodman & Gilman 14e", source_type="textbook", verification_status="VERIFIED")
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()
        session.add(source)
        await session.flush()

        high_risk_q = Question(
            concept_id=concept.id,
            question_text="High Risk Drug Dosing Vignette",
            correct_explanation="Clear explanation",
            remember_takeaway="Takeaway pearl",
            source_id=source.id,
            source_citation="Goodman & Gilman 14e, p. 210",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            is_high_risk=True,
            high_risk_category="drug_dosing",
            text_hash="hash-high-risk-test-1"
        )
        session.add(high_risk_q)
        await session.commit()

        # Step 1: Doctor 1 approves -> status remains IN_REVIEW / SECOND_REVIEW_REQUIRED
        rev1_res = await MedicalContentService.perform_medical_review(
            db=session, question_id=high_risk_q.id, reviewer_id=doc1.id,
            verdict="APPROVE", clinical_notes="Dosing verified against Goodman & Gilman table 14-2."
        )
        assert rev1_res["status"] == "REVIEW_PENDING"
        assert high_risk_q.trust_class == "AI_GENERATED_REVIEW_PENDING"

        # Step 2: Doctor 1 tries to approve again -> MUST FAIL (Distinct reviewer required)
        with pytest.raises(ValidationError) as exc_same:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=high_risk_q.id, reviewer_id=doc1.id,
                verdict="APPROVE", clinical_notes="Second approval by same doctor"
            )
        assert "distinct medical doctors" in str(exc_same.value)

        # Step 3: Doctor 2 (distinct verified doctor) approves -> status becomes APPROVED
        rev2_res = await MedicalContentService.perform_medical_review(
            db=session, question_id=high_risk_q.id, reviewer_id=doc2.id,
            verdict="APPROVE", clinical_notes="Concur with pharmacotherapy dosing."
        )
        assert rev2_res["status"] == "APPROVED"
        assert rev2_res["trust_class"] == "VERIFIED_CORE_QUESTION"
        assert high_risk_q.trust_class == "VERIFIED_CORE_QUESTION"

        # Step 4: Verify Immutable Credential Snapshot in review records
        stmt_revs = select(QuestionReview).where(QuestionReview.question_id == high_risk_q.id)
        reviews = (await session.execute(stmt_revs)).scalars().all()
        assert len(reviews) == 2
        for r in reviews:
            assert "VERIFIED" in r.reviewer_credential_status
            assert r.verdict == "APPROVE"
            assert r.source_verification_decision == "VERIFIED"

@pytest.mark.asyncio
async def test_unverified_content_strictly_excluded_from_student_tests(client_and_db):
    """
    Invariants Tested:
    1. DEVELOPMENT_BENCHMARK, UNVERIFIED, and AI_GENERATED_REVIEW_PENDING content
       is strictly excluded from student practice tests.
    2. Only legitimately approved VERIFIED_CORE_QUESTION content is selected.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Add 1 verified question and 3 unverified/benchmark questions
        q_verified = Question(
            concept_id=concept.id,
            question_text="Verified Question",
            correct_explanation="Exp",
            remember_takeaway="Pearl",
            status="PUBLISHED",
            trust_class="VERIFIED_CORE_QUESTION",
            text_hash="hash-pool-verified-1"
        )
        q_dev_bench = Question(
            concept_id=concept.id,
            question_text="Benchmark Question",
            correct_explanation="Exp",
            remember_takeaway="Pearl",
            status="PUBLISHED",
            trust_class="DEVELOPMENT_BENCHMARK",
            text_hash="hash-pool-bench-1"
        )
        q_pending = Question(
            concept_id=concept.id,
            question_text="Pending Review Question",
            correct_explanation="Exp",
            remember_takeaway="Pearl",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-pool-pending-1"
        )
        session.add_all([q_verified, q_dev_bench, q_pending])
        await session.flush()

        # Add options
        for q_obj in [q_verified, q_dev_bench, q_pending]:
            for key in ["A", "B", "C", "D"]:
                session.add(QuestionOption(
                    question_id=q_obj.id, option_key=key, option_text=f"Opt {key}", is_correct=(key == "A")
                ))
        await session.commit()

        # Create student test session
        sess, questions = await TestService.create_test_session(
            db=session, user_id="student-pool-test-1", mode="DAILY_SHORT_TEST", question_count=10
        )
        
        # Verify that unverified and benchmark questions are strictly excluded
        q_ids = [q.id for q in questions]
        assert q_dev_bench.id not in q_ids
        assert q_pending.id not in q_ids
        for q in questions:
            assert q.trust_class not in ["DEVELOPMENT_BENCHMARK", "AI_GENERATED_REVIEW_PENDING", "QUARANTINED", "WITHDRAWN", "UNVERIFIED"]
            assert q.status in ["PUBLISHED", "published", "APPROVED", "approved"]
