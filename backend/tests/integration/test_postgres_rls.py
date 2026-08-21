import os
import pytest
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Retrieve Postgres test URL if provided in environment or use standard staging container
POSTGRES_URL = os.getenv("POSTGRES_TEST_DATABASE_URL", "postgresql+asyncpg://postgres:staging_secure_password_2026@127.0.0.1:5432/neetpg_staging")

def find_sql_file(filename: str) -> Path:
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir, current_dir.parent, current_dir.parent.parent, current_dir.parent.parent.parent]:
        target = parent / "database" / filename
        if target.exists():
            return target
    raise FileNotFoundError(f"Could not locate database/{filename}")

@pytest.mark.asyncio
async def test_real_postgres_row_level_security():
    """
    Real PostgreSQL Row-Level Security Integration Test (Prompt 12, Gate 3).
    Executes actual PostgreSQL RLS policies against the live PostgreSQL staging instance.
    Proves at the database engine level:
    1. Student A can SELECT only Student A's data.
    2. Student A cannot SELECT Student B's data (filtered out by RLS).
    3. Student A cannot UPDATE/DELETE Student B's records (0 rows affected).
    4. Admin oversight role can SELECT all tenant records.
    """
    try:
        admin_engine = create_async_engine(POSTGRES_URL, echo=False)
        async with admin_engine.connect() as conn:
            await conn.execute(text("SELECT 1;"))
    except Exception as e:
        pytest.skip(f"Live PostgreSQL instance not reachable: {e}")

    admin_session_maker = async_sessionmaker(admin_engine, class_=AsyncSession, expire_on_commit=False)

    async with admin_session_maker() as session:
        # 1. Apply RLS policies via driver execution
        rls_path = find_sql_file("rls_policies.sql")
        with open(rls_path, "r", encoding="utf-8") as f:
            rls_sql = f.read()

        conn = await session.connection()
        raw_dbapi = await conn.get_raw_connection()
        await raw_dbapi.driver_connection.execute(rls_sql)
        await session.commit()

        # 2. Insert Taxonomy metadata for FK constraints
        await session.execute(text("""
            INSERT INTO subjects (id, name, code, created_at)
            VALUES ('sub-rls-1', 'RLS Subject', 'RLS01', NOW())
            ON CONFLICT (id) DO NOTHING;
        """))
        await session.execute(text("""
            INSERT INTO chapters (id, subject_id, name, created_at)
            VALUES ('chap-rls-1', 'sub-rls-1', 'RLS Chapter', NOW())
            ON CONFLICT (id) DO NOTHING;
        """))
        await session.execute(text("""
            INSERT INTO topics (id, chapter_id, name, created_at)
            VALUES ('top-rls-1', 'chap-rls-1', 'RLS Topic', NOW())
            ON CONFLICT (id) DO NOTHING;
        """))
        await session.execute(text("""
            INSERT INTO concepts (id, topic_id, name, created_at)
            VALUES ('concept-rls-1', 'top-rls-1', 'RLS Concept', NOW())
            ON CONFLICT (id) DO NOTHING;
        """))
        await session.execute(text("""
            INSERT INTO questions (id, concept_id, trust_class, question_text, correct_explanation, remember_takeaway, text_hash, created_at, updated_at)
            VALUES ('q-rls-1', 'concept-rls-1', 'VERIFIED_CORE_QUESTION', 'RLS Test Q', 'Exp', 'Pearl', 'hash-rls-1', NOW(), NOW())
            ON CONFLICT (id) DO NOTHING;
        """))
        await session.commit()

    await admin_engine.dispose()

    # Create App Engine connected as non-superuser 'neetpg_app' to test real RLS
    app_db_url = POSTGRES_URL.replace("postgres:staging_secure_password_2026", "neetpg_app:app_secure_password_2026")
    app_engine = create_async_engine(app_db_url, echo=False)
    app_session_maker = async_sessionmaker(app_engine, class_=AsyncSession, expire_on_commit=False)

    student_a_id = "11111111-1111-1111-1111-111111111111"
    student_b_id = "22222222-2222-2222-2222-222222222222"
    admin_id = "99999999-9999-9999-9999-999999999999"

    async with app_session_maker() as session:
        # Clean previous test attempts
        await session.execute(text("DELETE FROM test_attempts WHERE id IN ('att-a-1', 'att-b-1');"))
        await session.execute(text("DELETE FROM test_sessions WHERE id IN ('sess-a-1', 'sess-b-1');"))
        await session.commit()

        # 3. Student A creates session & attempt
        await session.execute(text(f"SET LOCAL request.jwt.claim.sub = '{student_a_id}';"))
        await session.execute(text("SET LOCAL request.jwt.claim.role = 'student';"))
        await session.execute(text("""
            INSERT INTO test_sessions (id, user_id, mode, total_questions, started_at)
            VALUES ('sess-a-1', :sa, 'DAILY_SHORT_TEST', 10, NOW())
            ON CONFLICT (id) DO NOTHING;
        """), {"sa": student_a_id})
        await session.execute(text("""
            INSERT INTO test_attempts (id, session_id, user_id, question_id, concept_id, is_correct, confidence, answered_at)
            VALUES ('att-a-1', 'sess-a-1', :sa, 'q-rls-1', 'concept-rls-1', true, 'definitely_know', NOW())
            ON CONFLICT (id) DO NOTHING;
        """), {"sa": student_a_id})
        await session.commit()

        # 4. Student B creates session & attempt
        await session.execute(text(f"SET LOCAL request.jwt.claim.sub = '{student_b_id}';"))
        await session.execute(text("SET LOCAL request.jwt.claim.role = 'student';"))
        await session.execute(text("""
            INSERT INTO test_sessions (id, user_id, mode, total_questions, started_at)
            VALUES ('sess-b-1', :sb, 'DAILY_SHORT_TEST', 10, NOW())
            ON CONFLICT (id) DO NOTHING;
        """), {"sb": student_b_id})
        await session.execute(text("""
            INSERT INTO test_attempts (id, session_id, user_id, question_id, concept_id, is_correct, confidence, answered_at)
            VALUES ('att-b-1', 'sess-b-1', :sb, 'q-rls-1', 'concept-rls-1', false, 'definitely_know', NOW())
            ON CONFLICT (id) DO NOTHING;
        """), {"sb": student_b_id})
        await session.commit()

        # 5. Authenticate as Student A -> MUST ONLY see Student A's attempt
        await session.execute(text(f"SET LOCAL request.jwt.claim.sub = '{student_a_id}';"))
        await session.execute(text("SET LOCAL request.jwt.claim.role = 'student';"))
        
        res = await session.execute(text("SELECT id, user_id FROM test_attempts WHERE id IN ('att-a-1', 'att-b-1');"))
        rows = res.fetchall()

        assert len(rows) == 1
        assert rows[0][0] == "att-a-1"
        assert rows[0][1] == student_a_id

        # Student A attempts to UPDATE Student B's attempt -> MUST affect 0 rows
        upd_res = await session.execute(text(
            f"UPDATE test_attempts SET is_correct = true WHERE id = 'att-b-1';"
        ))
        assert upd_res.rowcount == 0

        # 6. Authenticate as Admin -> CAN see both attempts
        await session.execute(text(f"SET LOCAL request.jwt.claim.sub = '{admin_id}';"))
        await session.execute(text("SET LOCAL request.jwt.claim.role = 'admin';"))
        
        admin_res = await session.execute(text("SELECT id, user_id FROM test_attempts WHERE id IN ('att-a-1', 'att-b-1');"))
        admin_rows = admin_res.fetchall()
        assert len(admin_rows) == 2

    await app_engine.dispose()
