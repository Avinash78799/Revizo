import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.user import User
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source
from app.db.nmc_19_subjects_taxonomy import NMC_19_SUBJECTS_METADATA
from app.services.corpus_ingestion_service import CorpusIngestionService
from app.services.medical_board_service import MedicalBoardService
from app.core.errors import ValidationError, AuthorizationError, NotFoundError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(loop_scope="function")
async def client_and_db():
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False, "timeout": 60.0},
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
async def test_m13_1_and_m13_2_medical_board_and_source_verification(client_and_db):
    """
    Milestone 13.1 & 13.2:
    1. Onboard 19 Primary Medical Specialists + 5 Secondary High-Risk Subspecialists.
    2. Verify credentials snapshot generation and medical council linking.
    3. Progressively audit and verify all 19 standard medical textbook sources.
    4. Enforce negative security gates (unauthorized onboarding / auditing denied).
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Setup Admin & Student
        admin = User(email="chief_dean_m13@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_applicant@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        session.add_all([admin, student])
        await session.commit()

        # Initialize 19 subjects taxonomy and sources
        await CorpusIngestionService.initialize_19_subjects_taxonomy(session)

        # 1. Negative Security Gate: Student cannot onboard medical panel
        with pytest.raises(AuthorizationError):
            await MedicalBoardService.onboard_19_discipline_medical_panel(session, student.id)

        # 2. M13.1: Onboard Medical Board Panel (Admin Action)
        onboard_res = await MedicalBoardService.onboard_19_discipline_medical_panel(session, admin.id)
        assert onboard_res["primary_discipline_specialists_count"] == 19
        assert onboard_res["secondary_high_risk_specialists_count"] == 5
        assert onboard_res["total_board_size"] == 24
        assert onboard_res["newly_onboarded_primary"] == 19
        assert onboard_res["newly_onboarded_secondary"] == 5

        # Verify all doctors have VERIFIED status in MedicalReviewerProfile
        stmt_profiles = select(MedicalReviewerProfile)
        profiles = (await session.execute(stmt_profiles)).scalars().all()
        assert len(profiles) >= 24
        for p in profiles:
            assert p.verification_status == "VERIFIED"
            assert p.credential_status == "ACTIVE"
            assert p.registration_number is not None
            assert p.medical_council is not None

        # Pick one verified medical auditor
        lead_auditor_profile = profiles[0]

        # 3. Negative Security Gate: Student cannot audit sources
        with pytest.raises(AuthorizationError):
            await MedicalBoardService.audit_and_verify_all_19_discipline_sources(session, student.id)

        # 4. M13.2: Verified Medical Auditor Audits All 19 Sources
        audit_res = await MedicalBoardService.audit_and_verify_all_19_discipline_sources(
            db=session,
            auditor_user_id=lead_auditor_profile.user_id
        )
        assert audit_res["total_subject_sources"] == 19
        assert audit_res["newly_verified_sources"] == 19

        # Verify all 19 canonical sources are now in VERIFIED state
        for subj_meta in NMC_19_SUBJECTS_METADATA:
            ref_id = f"ISBN-{subj_meta['default_source']['isbn']}"
            stmt_src = select(Source).where(Source.reference_identifier == ref_id)
            src = (await session.execute(stmt_src)).scalars().first()
            assert src is not None
            assert src.verification_status == "VERIFIED"
            assert src.verified_by == lead_auditor_profile.user_id
            assert src.verified_at is not None
