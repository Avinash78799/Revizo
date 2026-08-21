import asyncio
import os
import sys
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.services.source_provenance_service import SourceProvenanceService
from app.models.taxonomy import SyllabusRegistry, SyllabusSourceArtifact
from sqlalchemy import select

# Live PostgreSQL staging URL or fallback to environment
DATABASE_URL = os.getenv("POSTGRES_TEST_DATABASE_URL", "postgresql+asyncpg://postgres:staging_secure_password_2026@127.0.0.1:5432/neetpg_staging")

async def main():
    print(f"Connecting to live staging database: {DATABASE_URL}")
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    pdf_path = os.path.join(os.path.dirname(__file__), "..", "artifacts", "nmc", "PGMER_2023_Official_Gazette.pdf")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Downloaded PDF not found at {pdf_path}")

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    computed_hash = hashlib.sha256(pdf_bytes).hexdigest()
    print(f"PDF Size: {len(pdf_bytes)} bytes")
    print(f"Computed SHA-256 Digest: {computed_hash}")

    async with session_maker() as session:
        # Register Candidate Artifact in UNVERIFIED status
        artifact = await SourceProvenanceService.register_syllabus_candidate_artifact(
            db=session,
            syllabus_version="neet-pg-nmc-pgmer-2023-v1.0",
            document_identifier="GAZETTE-INDIA-EXTRAORDINARY-PART-III-SEC-4-NO-907",
            document_hash=computed_hash,
            source_name="National Medical Commission (NMC)",
            source_url="https://egazette.gov.in/WriteReadData/2023/250982.pdf",
            effective_date="2023-12-29"
        )
        print("\n--- NMC SYLLABUS ARTIFACT REGISTERED IN STAGING POSTGRESQL ---")
        print(f"Artifact ID: {artifact.id}")
        print(f"Syllabus Version: {artifact.syllabus_version}")
        print(f"Document Identifier: {artifact.document_identifier}")
        print(f"Document SHA-256: {artifact.document_hash}")
        print(f"Official URL: {artifact.source_url}")
        print(f"Effective Date: {artifact.effective_date}")
        print(f"Verification Status: {artifact.verification_status}")
        print(f"Verified By: {artifact.verified_by} (UNVERIFIED / PENDING AUDIT)")
        print(f"Retrieved At: {artifact.retrieved_at.isoformat()}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
