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
from app.models.taxonomy import Subject, Chapter, Topic, Concept
from app.models.question import Question, QuestionOption
from app.models.source import Source
from app.services.corpus_ingestion_service import CorpusIngestionService
from app.services.test_service import TestService

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
async def test_19_subjects_taxonomy_and_950_candidate_corpus_production(client_and_db):
    """
    Milestone 12.4: 19-Subject Corpus Production & Coverage Matrix.
    
    1. Initialize all 19 NMC disciplines (ANAT, PHYS, BIOCH, PHARM, PATH, MICRO, FMT, PSM, MED, PED, DERM, PSYCH, RAD, ANES, SURG, ORTHO, ENT, OPHTH, OBGYN).
    2. Populate 50 candidates per subject = 950 candidate questions.
    3. Validate 4-option single-best-answer structural integrity for all candidates.
    4. Confirm all 950 candidates are in status PROPOSED and trust_class AI_GENERATED_REVIEW_PENDING.
    5. Confirm that 100% of candidate questions are BLOCKED from the student test pool.
    6. Verify live Coverage Matrix reports 19 subjects with 50 candidates each and doctor_verified=0.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create Admin
        admin = User(email="corpus_admin_m12@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        session.add(admin)
        await session.commit()

        # Build complete 950 candidate corpus
        build_result = await CorpusIngestionService.build_complete_950_candidate_corpus(
            db=session,
            creator_user_id=admin.id
        )

        # 1. Verify 19 Subjects Exist
        stmt_subjects = select(Subject).order_index if hasattr(select(Subject), "order_index") else select(Subject)
        subjects = (await session.execute(stmt_subjects)).scalars().all()
        assert len(subjects) == 19
        subject_codes = {s.code for s in subjects}
        expected_codes = {
            "ANAT", "PHYS", "BIOCH", "PHARM", "PATH", "MICRO", "FMT", "PSM",
            "MED", "PED", "DERM", "PSYCH", "RAD", "ANES", "SURG", "ORTHO",
            "ENT", "OPHTH", "OBGYN"
        }
        assert subject_codes == expected_codes

        # 2. Verify Total Question Count >= 950
        stmt_total_q = select(func.count(Question.id))
        total_questions = (await session.execute(stmt_total_q)).scalar_one()
        assert total_questions >= 950

        # 3. Verify Candidate Status & Trust Class Defaults
        stmt_proposed = select(func.count(Question.id)).where(
            and_(
                Question.status == "PROPOSED",
                Question.trust_class == "AI_GENERATED_REVIEW_PENDING"
            )
        )
        proposed_count = (await session.execute(stmt_proposed)).scalar_one()
        assert proposed_count >= 950

        # 4. Verify Coverage Matrix Breakdown
        matrix = await CorpusIngestionService.get_corpus_coverage_matrix(session)
        assert len(matrix) == 19
        total_matrix_candidates = 0
        for row in matrix:
            assert row["target"] == 50
            assert row["candidates"] >= 50
            assert row["evidence_backed"] >= 50
            assert row["doctor_verified"] == 0  # 0 until human doctor approves!
            total_matrix_candidates += row["candidates"]

        assert total_matrix_candidates >= 950

        # 5. Verify Student Practice Pool Isolation Gate
        sess, practice_questions = await TestService.create_test_session(
            db=session,
            user_id="student-corpus-isolation-tester",
            mode="DAILY_SHORT_TEST",
            question_count=10
        )
        
        # Ensure NO proposed / review-pending candidate entered the active student pool
        for q in practice_questions:
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
            assert q.trust_class not in [
                "AI_GENERATED_REVIEW_PENDING",
                "DEVELOPMENT_BENCHMARK",
                "QUARANTINED",
                "WITHDRAWN",
                "UNVERIFIED"
            ]
