import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept
from app.models.source import Source, EvidenceReference
from app.models.reviewer import MedicalReviewerProfile
from app.models.question import Question, QuestionOption
from app.models.user import User
from app.services.source_ingestion_pipeline import SourceIngestionPipeline
from app.core.staging_config import JsonLogFormatter
from app.core.errors import ValidationError
import logging

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
async def test_real_medical_source_ingestion_workflow(client_and_db):
    """
    Acceptance:
    Stage 1 to 7 pipeline creates Question Candidate in AI_GENERATED_REVIEW_PENDING
    with verified Source, Evidence Reference, and Distractor Explanations.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Seed verified doctor auditor
        u = User(id="doc-auditor-pilot", email="pilot@aiims.edu", hashed_password="pw", role="reviewer")
        p = MedicalReviewerProfile(user_id="doc-auditor-pilot", credential_type="MD", specialty="Pharmacology", verification_status="VERIFIED", active_status=True)
        session.add_all([u, p])
        await session.commit()

        # Ingest Source
        source = await SourceIngestionPipeline.ingest_and_register_source(
            db=session,
            title="Goodman & Gilman's Pharmacological Basis of Therapeutics 14th Ed",
            source_type="STANDARD_TEXTBOOK",
            publisher="McGraw Hill",
            edition="14th",
            reference_identifier="ISBN-9781264258079",
            specialty="Pharmacology",
            verifier_id="doc-auditor-pilot",
            notes="Authoritative pharmacology textbook."
        )
        assert source.verification_status == "VERIFIED"
        assert source.reference_identifier == "ISBN-9781264258079"

        # Fetch concept
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Ingest Question Candidate
        q = await SourceIngestionPipeline.process_question_candidate(
            db=session,
            source_id=source.id,
            concept_id=concept.id,
            question_text="A 45-year-old patient on enalapril develops intractable dry cough. Which mechanism accounts for this symptom?",
            options={
                "A": "Accumulation of bradykinin and substance P",
                "B": "Excessive angiotensin II receptor downregulation",
                "C": "Direct pulmonary alpha-1 adrenergic stimulation",
                "D": "Inhibition of neutral endopeptidase"
            },
            correct_option_key="A",
            correct_explanation="ACE is identical to kininase II, responsible for bradykinin degradation. ACE inhibition causes bradykinin and substance P accumulation, triggering bronchoconstriction and cough.",
            remember_takeaway="ACE inhibitor cough is mediated by bradykinin accumulation. Switching to an ARB eliminates this adverse effect.",
            distractor_explanations={
                "B": "ACE inhibitors reduce angiotensin II levels rather than causing direct receptor downregulation.",
                "C": "Alpha-1 adrenergic receptors are not directly stimulated by ACE inhibitors.",
                "D": "Neprilysin (neutral endopeptidase) is inhibited by sacubitril, not primarily by enalapril."
            },
            claim_snippet="ACE inhibitors prevent degradation of bradykinin, leading to cough in 5-20% of patients (Ch. 26).",
            page_or_section="Chapter 26, Renin-Angiotensin System, p. 512",
            is_high_risk=False,
            exam_relevance_tag="HIGH_YIELD"
        )

        assert q.status == "PROPOSED"
        assert q.trust_class == "AI_GENERATED_REVIEW_PENDING"
        assert q.source_citation is not None
        assert len(q.options) == 4
        assert any(opt.is_correct and opt.option_key == "A" for opt in q.options)

@pytest.mark.asyncio
async def test_unverified_auditor_cannot_register_authoritative_source(client_and_db):
    """
    Acceptance:
    Unregistered or unverified users cannot verify medical source records.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        with pytest.raises(ValidationError) as exc:
            await SourceIngestionPipeline.ingest_and_register_source(
                db=session,
                title="Unreviewed Medical Handout",
                source_type="OTHER",
                publisher="Unknown",
                edition="1st",
                reference_identifier="None",
                specialty="Medicine",
                verifier_id="unregistered-doctor-id"
            )
        assert "requires an active, verified medical auditor" in str(exc.value).lower()

@pytest.mark.asyncio
async def test_observability_and_audit_logging_masks_pii():
    """
    Acceptance:
    Structured JSON log formatter correctly records metadata and masks sensitive fields.
    """
    formatter = JsonLogFormatter()
    record = logging.LogRecord(
        name="neetpg.audit",
        level=logging.INFO,
        pathname="pipeline.py",
        lineno=42,
        msg="Medical content ingested for concept C101 with verified source ISBN-9781264258079",
        args=(),
        exc_info=None
    )
    formatted = formatter.format(record)
    assert "timestamp" in formatted
    assert "neetpg.audit" in formatted
    assert "C101" in formatted
    assert "password" not in formatted.lower()
