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
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.question import Question, QuestionOption, QuestionReview
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source, EvidenceReference, PyqReference
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
async def test_m12_controlled_pilot_batch_execution(client_and_db):
    """
    Milestone 12.3: Controlled Evidence-Linked Pilot Batch.
    
    1. Authoritative Source: Harrison's Principles of Internal Medicine 21st Ed (VERIFIED).
    2. Medical Reviewers:
       - Dr. Ramesh (MD General Medicine, KMC-45120) -> VERIFIED
       - Dr. Priya (MD Cardiology, TMC-88901) -> VERIFIED
    3. Pilot Questions:
       - Standard-Risk Pilot 1 (Cardiology Biomarkers): Harrison 21e Ch. 270
       - Standard-Risk Pilot 2 (Diabetic Ketoacidosis Triad): Harrison 21e Ch. 397
       - Standard-Risk Pilot 3 (PCP Prophylaxis in HIV): Harrison 21e Ch. 202
       - High-Risk Pilot 1 (IM Epinephrine in Anaphylaxis): Harrison 21e Ch. 350
       - High-Risk Pilot 2 (Aortic Dissection Beta-Blocker Precedence): Harrison 21e Ch. 274
    4. PYQ Provenance Gate:
       - Candidate claiming PYQ without authentic master paper evidence remains UNVERIFIED.
    5. Two-Doctor Gate for High-Risk:
       - Single doctor approval leaves status as REVIEW_PENDING.
       - Distinct 2nd doctor approval promotes to APPROVED / VERIFIED_CORE_QUESTION.
    6. Student Practice Pool Gate:
       - Unapproved candidates, pending reviews, and unverified PYQs are 100% blocked.
       - Fully approved pilot questions are admitted.
    7. Immutable Audit Snapshots verified.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # 1. Setup Admin & Medical Reviewers
        admin = User(email="chief_admin_m12@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        dr_ramesh = User(email="dr_ramesh_internalmed@aiims.edu", hashed_password="pw", role="medical_reviewer", is_active=True)
        dr_priya = User(email="dr_priya_cardio@cmcvellore.ac.in", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([admin, dr_ramesh, dr_priya])
        await session.commit()

        p_ramesh = await ReviewerService.register_reviewer_profile(
            db=session, user_id=dr_ramesh.id, credential_type="MD",
            registration_number="KMC-45120", medical_council="Karnataka Medical Council", specialty="General Medicine"
        )
        p_priya = await ReviewerService.register_reviewer_profile(
            db=session, user_id=dr_priya.id, credential_type="MD",
            registration_number="TMC-88901", medical_council="Tamil Nadu Medical Council", specialty="Cardiology"
        )
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_ramesh.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="KMC-AUDIT-45120")
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_priya.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="TMC-AUDIT-88901")

        # 2. Register & Audit Harrison 21e Source
        harrison_src = await SourceProvenanceService.register_source_candidate(
            db=session, title="Harrison's Principles of Internal Medicine", source_type="STANDARD_TEXTBOOK",
            publisher="McGraw Hill Professional", edition="21st Edition", reference_identifier="ISBN-9781264268504",
            url="https://accessmedicine.mhmedical.com/book.aspx?bookid=3095", specialty="General Medicine"
        )
        await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=harrison_src.id, verifier_id=dr_ramesh.id, decision="VERIFIED",
            reference_identifier="ISBN-9781264268504", edition="21st Edition", publisher="McGraw Hill Professional",
            audit_evidence_notes="Audited physical print 2-volume edition and AccessMedicine entry."
        )

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # =========================================================================
        # PILOT QUESTION 1: Standard-Risk (Cardiology - Harrison 21e Ch. 270)
        # =========================================================================
        q1 = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="A 58-year-old man presents to the emergency department with 2 hours of retrosternal pressure. Which cardiac biomarker is the gold standard for detecting myocardial necrosis due to its high tissue specificity?",
            options={
                "A": "Cardiac Troponin (cTnI / cTnT)",
                "B": "Creatine Kinase-MB (CK-MB)",
                "C": "Myoglobin",
                "D": "Lactate Dehydrogenase (LDH-1)"
            },
            correct_option_key="A",
            correct_explanation="Cardiac Troponins (cTnI and cTnT) are the preferred and gold-standard biomarkers for myocardial necrosis due to their near-absolute myocardial tissue specificity and high sensitivity.",
            remember_takeaway="Cardiac Troponin (cTnI/cTnT) is the gold standard for acute myocardial infarction diagnosis; rises in 2-4 hours and remains elevated for 7-10 days.",
            source_id=harrison_src.id,
            source_citation="Harrison's Principles of Internal Medicine, 21st Ed, Chapter 270, p. 1978–1983",
            page_or_section="Chapter 270, p. 1980",
            claim_snippet="Cardiac troponins I and T are the preferred biomarkers for myocardial necrosis because of their high sensitivity and cardiac specificity."
        )
        # Approval by 1 Verified Doctor (Dr. Ramesh)
        rev_q1 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q1.id, reviewer_id=dr_ramesh.id, verdict="APPROVE",
            clinical_notes="Verified cardiac biomarker kinetics against Harrison 21e Chapter 270."
        )
        assert rev_q1["status"] == "APPROVED"
        assert rev_q1["trust_class"] == "VERIFIED_CORE_QUESTION"
        q1.status = "PUBLISHED"

        # =========================================================================
        # PILOT QUESTION 2: Standard-Risk (Endocrinology - Harrison 21e Ch. 397)
        # =========================================================================
        q2 = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="A 22-year-old woman with Type 1 Diabetes presents with nausea, vomiting, Kussmaul breathing, and fruity breath. Which laboratory triad confirms the diagnosis of Diabetic Ketoacidosis (DKA)?",
            options={
                "A": "Blood glucose >250 mg/dL, positive serum ketones, and arterial pH <7.30 with bicarbonate <18 mEq/L",
                "B": "Blood glucose >600 mg/dL, negative ketones, and arterial pH >7.35 with osmolality >320 mOsm/kg",
                "C": "Blood glucose <70 mg/dL, positive urine ketones, and normal arterial blood gas",
                "D": "Blood glucose >200 mg/dL, normal anion gap, and respiratory alkalosis"
            },
            correct_option_key="A",
            correct_explanation="Diabetic Ketoacidosis is defined biochemically by the triad of hyperglycemia (plasma glucose >250 mg/dL), ketonemia/ketonuria, and high anion-gap metabolic acidosis (pH <7.30, HCO3 <18 mEq/L).",
            remember_takeaway="DKA triad: Hyperglycemia (>250 mg/dL), Ketonemia (beta-hydroxybutyrate), and High Anion-Gap Acidosis (pH <7.30, HCO3 <18).",
            source_id=harrison_src.id,
            source_citation="Harrison's Principles of Internal Medicine, 21st Ed, Chapter 397, p. 2930–2936",
            page_or_section="Chapter 397, p. 2932",
            claim_snippet="The diagnostic criteria for DKA include a blood glucose concentration >250 mg/dL, a positive serum ketone test, and metabolic acidosis with an arterial pH <7.30 and serum bicarbonate <18 mEq/L."
        )
        rev_q2 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q2.id, reviewer_id=dr_ramesh.id, verdict="APPROVE",
            clinical_notes="Verified DKA diagnostic criteria against Harrison 21e Chapter 397."
        )
        assert rev_q2["status"] == "APPROVED"
        q2.status = "PUBLISHED"

        # =========================================================================
        # PILOT QUESTION 3: Standard-Risk (Infectious Diseases - Harrison 21e Ch. 202)
        # =========================================================================
        q3 = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="A 34-year-old HIV-positive male with a CD4+ T-lymphocyte count of 140 cells/uL is evaluated in clinic. Which antimicrobial regimen is the first-line choice for primary prophylaxis against Pneumocystis jirovecii pneumonia (PCP)?",
            options={
                "A": "Trimethoprim-Sulfamethoxazole (TMP-SMX) 1 double-strength tablet daily",
                "B": "Aerosolized Pentamidine 300 mg monthly",
                "C": "Oral Dapsone 100 mg daily alone",
                "D": "Oral Atovaquone 1500 mg daily with meals"
            },
            correct_option_key="A",
            correct_explanation="Trimethoprim-sulfamethoxazole (TMP-SMX) is the first-line drug of choice for primary prophylaxis against Pneumocystis jirovecii pneumonia in HIV patients with CD4 counts <200/uL.",
            remember_takeaway="TMP-SMX is first-line for PCP prophylaxis when CD4 <200/uL; also provides cross-protection against Toxoplasma gondii.",
            source_id=harrison_src.id,
            source_citation="Harrison's Principles of Internal Medicine, 21st Ed, Chapter 202, p. 1420–1425",
            page_or_section="Chapter 202, p. 1422",
            claim_snippet="Trimethoprim-sulfamethoxazole (one double-strength tablet daily) is the preferred prophylactic agent for PCP in patients with CD4+ T cell counts <200/uL."
        )
        rev_q3 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q3.id, reviewer_id=dr_ramesh.id, verdict="APPROVE",
            clinical_notes="Verified opportunistic infection prophylaxis guideline against Harrison 21e Chapter 202."
        )
        assert rev_q3["status"] == "APPROVED"
        q3.status = "PUBLISHED"

        # =========================================================================
        # PILOT QUESTION 4: High-Risk (Emergency Management / Anaphylaxis - Harrison 21e Ch. 350)
        # =========================================================================
        q4_hr = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="A 26-year-old male develops sudden urticaria, laryngeal stridor, bronchospasm, and hypotension (BP 80/50 mmHg) 10 minutes after a wasp sting. What is the immediate first-line lifesaving pharmacotherapy?",
            options={
                "A": "Intramuscular Epinephrine 0.3 to 0.5 mg (1:1000) in anterolateral thigh",
                "B": "Intravenous Diphenhydramine 50 mg slow push",
                "C": "Intravenous Hydrocortisone 200 mg bolus",
                "D": "Inhaled Albuterol nebulization 5 mg"
            },
            correct_option_key="A",
            correct_explanation="Intramuscular epinephrine (1:1000, 0.3-0.5 mg in adults) injected into the anterolateral mid-thigh is the immediate first-line lifesaving drug for acute systemic anaphylaxis.",
            remember_takeaway="Intramuscular Epinephrine (anterolateral thigh, 1:1000, 0.3-0.5 mg) is the absolute first-line drug for anaphylaxis; antihistamines and corticosteroids are adjuncts only.",
            source_id=harrison_src.id,
            source_citation="Harrison's Principles of Internal Medicine, 21st Ed, Chapter 350, p. 2568–2571",
            page_or_section="Chapter 350, p. 2570",
            claim_snippet="Epinephrine is the treatment of choice for anaphylaxis and must be administered immediately. The recommended dose is 0.3 to 0.5 mg of a 1:1000 dilution intramuscularly in the anterolateral thigh.",
            is_high_risk=True,
            high_risk_category="emergency_management"
        )
        assert q4_hr.is_high_risk is True

        # Step 1: Doctor 1 approves -> Status remains REVIEW_PENDING (Two-Doctor Gate)
        rev_q4_doc1 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q4_hr.id, reviewer_id=dr_ramesh.id, verdict="APPROVE",
            clinical_notes="Doctor 1: Verified anaphylaxis epinephrine dosage and route."
        )
        assert rev_q4_doc1["status"] == "REVIEW_PENDING"
        assert q4_hr.trust_class == "AI_GENERATED_REVIEW_PENDING"

        # Step 2: Doctor 2 (distinct cardiologist/internist) approves -> Promoted to APPROVED / VERIFIED_CORE_QUESTION
        rev_q4_doc2 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q4_hr.id, reviewer_id=dr_priya.id, verdict="APPROVE",
            clinical_notes="Doctor 2: Confirmed IM anterolateral thigh route and 0.3-0.5 mg dosage."
        )
        assert rev_q4_doc2["status"] == "APPROVED"
        assert rev_q4_doc2["trust_class"] == "VERIFIED_CORE_QUESTION"
        q4_hr.status = "PUBLISHED"

        # =========================================================================
        # PILOT QUESTION 5: High-Risk (Cardiology / Aortic Dissection - Harrison 21e Ch. 274)
        # =========================================================================
        q5_hr = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="A 62-year-old man presents with sudden tearing interscapular back pain and blood pressure of 210/120 mmHg. CT angiography confirms an acute Stanford Type B aortic dissection. In medical management, which hemodynamic drug class MUST be initiated before administering vasodilators like sodium nitroprusside?",
            options={
                "A": "Intravenous Beta-Blocker (e.g. Esmolol or Labetalol)",
                "B": "Intravenous Sodium Nitroprusside alone",
                "C": "Intravenous Hydralazine bolus",
                "D": "Oral Amlodipine"
            },
            correct_option_key="A",
            correct_explanation="In acute aortic dissection, beta-blockers must always be initiated before or concurrently with vasodilators to reduce heart rate below 60 bpm and decrease aortic wall shear stress (dP/dt). Administering a pure vasodilator alone causes reflex tachycardia and accelerates dissection propagation.",
            remember_takeaway="In acute aortic dissection: Beta-blockers (Esmolol/Labetalol) MUST precede vasodilators to abolish reflex tachycardia and reduce dP/dt.",
            source_id=harrison_src.id,
            source_citation="Harrison's Principles of Internal Medicine, 21st Ed, Chapter 274, p. 2012–2016",
            page_or_section="Chapter 274, p. 2014",
            claim_snippet="Beta-adrenergic blockade should be initiated before vasodilator therapy is started, because vasodilators can cause reflex tachycardia and an increase in dP/dt, which may promote further dissection.",
            is_high_risk=True,
            high_risk_category="contraindications"
        )
        assert q5_hr.is_high_risk is True

        # Two distinct doctor reviews for Q5
        await MedicalContentService.perform_medical_review(
            db=session, question_id=q5_hr.id, reviewer_id=dr_ramesh.id, verdict="APPROVE",
            clinical_notes="Doctor 1: Verified beta-blocker precedence rule in aortic dissection."
        )
        rev_q5_doc2 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q5_hr.id, reviewer_id=dr_priya.id, verdict="APPROVE",
            clinical_notes="Doctor 2: Concur with dP/dt shear stress physiology and esmolol priority."
        )
        assert rev_q5_doc2["status"] == "APPROVED"
        assert rev_q5_doc2["trust_class"] == "VERIFIED_CORE_QUESTION"
        q5_hr.status = "PUBLISHED"

        # =========================================================================
        # 4. PYQ PROVENANCE INTERLOCK TEST (Anti-Fabrication Gate)
        # =========================================================================
        # Create an unverified PYQ candidate without authentic master paper
        unverified_pyq_ref = PyqReference(
            id="pyq-ref-unverified-m12",
            concept_id=concept.id,
            exam_name="NEET-PG",
            exam_year=2023,
            pyq_status="UNVERIFIED",
            verification_status="UNVERIFIED"
        )
        session.add(unverified_pyq_ref)
        await session.commit()

        # Attempting candidate ingestion with unverified PYQ claim -> MUST BE REJECTED
        with pytest.raises(ValidationError) as exc_pyq:
            await MedicalCandidateService.ingest_candidate_question(
                db=session,
                creator_user_id=admin.id,
                concept_id=concept.id,
                question_text="Clinical candidate claiming PYQ without verified master paper?",
                options={"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
                correct_option_key="A",
                correct_explanation="Explanation",
                remember_takeaway="Takeaway",
                pyq_reference_id=unverified_pyq_ref.id
            )
        assert "Candidate cannot claim PYQ provenance from unverified reference" in str(exc_pyq.value)

        # =========================================================================
        # 5. STUDENT TEST POOL SELECTION INTEGRATION
        # =========================================================================
        await session.commit()
        sess, student_questions = await TestService.create_test_session(
            db=session, user_id="student-m12-pilot-tester", mode="DAILY_SHORT_TEST", question_count=10
        )
        
        selected_ids = {q.id for q in student_questions}
        # Verify that all published, verified pilot questions are eligible
        assert q1.id in selected_ids
        assert q2.id in selected_ids
        assert q3.id in selected_ids
        assert q4_hr.id in selected_ids
        assert q5_hr.id in selected_ids

        for q in student_questions:
            assert q.trust_class in ["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED", "development_seed"]
            assert q.status.upper() in ("PUBLISHED", "APPROVED")

        # =========================================================================
        # 6. IMMUTABLE REVIEW AUDIT VERIFICATION
        # =========================================================================
        stmt_reviews = select(QuestionReview).where(QuestionReview.question_id.in_([q1.id, q4_hr.id]))
        reviews = (await session.execute(stmt_reviews)).scalars().all()
        assert len(reviews) == 3  # 1 for Q1, 2 for Q4_HR
        for r in reviews:
            assert r.reviewer_credential_status in ("MD_VERIFIED", "DM_VERIFIED")
            assert r.source_verification_decision == "VERIFIED"
            assert r.created_at is not None
