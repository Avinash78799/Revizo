import os
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

POSTGRES_URL = os.getenv("POSTGRES_TEST_DATABASE_URL", "postgresql+asyncpg://postgres:staging_secure_password_2026@127.0.0.1:5432/neetpg_staging")

@pytest.mark.asyncio
async def test_live_pgvector_cosine_similarity():
    """
    Gate 4: Real pgvector Extension & Cosine Similarity Test (Prompt 12, Gate 4).
    Verifies pgvector extension, 1536-dimension vector insertion, and cosine distance query.
    """
    try:
        pg_engine = create_async_engine(POSTGRES_URL, echo=False)
        async with pg_engine.connect() as conn:
            await conn.execute(text("SELECT 1;"))
    except Exception as e:
        pytest.skip(f"Live pgvector instance not reachable: {e}")

    session_maker = async_sessionmaker(pg_engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        # 1. Verify extension
        res = await session.execute(text("SELECT extversion FROM pg_extension WHERE extname = 'vector';"))
        ext_row = res.fetchone()
        assert ext_row is not None
        assert ext_row[0] == "0.8.6"

        # 2. Add embedding column to concepts if not present and test vector operations
        await session.execute(text("ALTER TABLE concepts ADD COLUMN IF NOT EXISTS embedding vector(1536);"))
        await session.commit()

        # 3. Create test vectors (1536 dimensions)
        vec_a = "[" + ",".join(["1.0" if i == 0 else "0.0" for i in range(1536)]) + "]"
        vec_b = "[" + ",".join(["0.99" if i == 0 else ("0.01" if i == 1 else "0.0") for i in range(1536)]) + "]"
        vec_c = "[" + ",".join(["1.0" if i == 1 else "0.0" for i in range(1536)]) + "]"

        await session.execute(text("""
            INSERT INTO concepts (id, topic_id, name, embedding, created_at)
            VALUES 
                ('concept-vec-a', 'top-rls-1', 'Vector Concept A', CAST(:va AS vector), NOW()),
                ('concept-vec-b', 'top-rls-1', 'Vector Concept B', CAST(:vb AS vector), NOW()),
                ('concept-vec-c', 'top-rls-1', 'Vector Concept C', CAST(:vc AS vector), NOW())
            ON CONFLICT (id) DO UPDATE SET embedding = EXCLUDED.embedding;
        """), {"va": vec_a, "vb": vec_b, "vc": vec_c})
        await session.commit()

        # 4. Execute Cosine Distance Query (<=>) searching for nearest to Vector A
        search_res = await session.execute(text("""
            SELECT id, name, embedding <=> CAST(:query_vec AS vector) AS distance
            FROM concepts
            WHERE id IN ('concept-vec-a', 'concept-vec-b', 'concept-vec-c')
            ORDER BY distance ASC;
        """), {"query_vec": vec_a})
        
        matches = search_res.fetchall()
        assert len(matches) == 3
        
        # Closest match to Vector A must be Vector A (distance 0.0)
        assert matches[0][0] == "concept-vec-a"
        assert abs(float(matches[0][2])) < 1e-5

        # Second closest must be Vector B (small cosine distance)
        assert matches[1][0] == "concept-vec-b"
        assert float(matches[1][2]) < 0.05

        # Third must be Vector C (orthogonal, distance 1.0)
        assert matches[2][0] == "concept-vec-c"
        assert float(matches[2][2]) > 0.95

    await pg_engine.dispose()
