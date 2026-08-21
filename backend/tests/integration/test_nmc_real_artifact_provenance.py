import os
import hashlib
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.taxonomy import SyllabusRegistry, SyllabusSourceArtifact
from app.services.source_provenance_service import SourceProvenanceService
from app.core.errors import ValidationError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.mark.asyncio
async def test_nmc_pgmer_2023_official_artifact_provenance():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False
    )
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    pdf_path = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "nmc", "PGMER_2023_Official_Gazette.pdf")
    assert os.path.exists(pdf_path), f"Official PDF not found at {pdf_path}"

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    assert len(pdf_bytes) == 478482
    computed_hash = hashlib.sha256(pdf_bytes).hexdigest()
    assert computed_hash == "2e9c4d39b83bcd35cf85208b952ccc1e98d0a03467219a3c8dd52cfc8e6edd8f"

    async with async_session() as session:
        # Register artifact
        artifact = await SourceProvenanceService.register_syllabus_candidate_artifact(
            db=session,
            syllabus_version="neet-pg-nmc-pgmer-2023-v1.0",
            document_identifier="GAZETTE-INDIA-EXTRAORDINARY-PART-III-SEC-4-NO-907",
            document_hash=computed_hash,
            source_name="National Medical Commission (NMC)",
            source_url="https://egazette.gov.in/WriteReadData/2023/250982.pdf",
            effective_date="2023-12-29"
        )
        assert artifact.verification_status == "UNVERIFIED"
        assert artifact.verified_by is None
        assert artifact.document_hash == computed_hash

        # Verify registry entry
        stmt_reg = select(SyllabusRegistry).where(SyllabusRegistry.syllabus_version == "neet-pg-nmc-pgmer-2023-v1.0")
        reg = (await session.execute(stmt_reg)).scalars().first()
        assert reg is not None
        assert reg.verification_status == "UNVERIFIED"

    await engine.dispose()
