"""Medical provenance, reviewer profiles and benchmark schema

Revision ID: 0002_medical_provenance
Revises: 0001_initial_schema
Create Date: 2026-08-19 18:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0002_medical_provenance'
down_revision: Union[str, None] = '0001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Medical Reviewer Profiles Table
    op.create_table(
        'medical_reviewer_profiles',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('credential_type', sa.String(length=50), nullable=False),
        sa.Column('registration_number', sa.String(length=100), nullable=True),
        sa.Column('medical_council', sa.String(length=150), nullable=True),
        sa.Column('specialty', sa.String(length=100), nullable=False),
        sa.Column('verification_status', sa.String(length=50), nullable=False, server_default='PENDING'),
        sa.Column('credential_status', sa.String(length=50), nullable=False, server_default='ACTIVE'),
        sa.Column('active_status', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('verified_by', sa.String(length=36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('suspension_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_reviewer_verification', 'medical_reviewer_profiles', ['verification_status'])

    # 2. Benchmark Cases Table
    op.create_table(
        'benchmark_cases',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('benchmark_case_id', sa.String(length=50), nullable=False, unique=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('correct_option_key', sa.String(length=1), nullable=True),
        sa.Column('expected_result', sa.String(length=50), nullable=False),
        sa.Column('expected_validator_behavior', sa.String(length=100), nullable=False),
        sa.Column('medical_rationale', sa.Text(), nullable=False),
        sa.Column('authoritative_source', sa.String(length=255), nullable=False),
        sa.Column('provenance_status', sa.String(length=50), nullable=False, server_default='DEVELOPMENT_BENCHMARK'),
        sa.Column('reviewer_id', sa.String(length=36), nullable=True),
        sa.Column('expert_verified_by', sa.String(length=150), nullable=False),
        sa.Column('verification_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('benchmark_version', sa.String(length=50), nullable=False, server_default='gold-benchmark-v1.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_benchmark_category', 'benchmark_cases', ['category'])

    # 3. Syllabus Source Artifacts Table
    op.create_table(
        'syllabus_source_artifacts',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('syllabus_version', sa.String(length=50), nullable=False),
        sa.Column('source_name', sa.String(length=200), nullable=False),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('document_identifier', sa.String(length=100), nullable=False),
        sa.Column('document_hash', sa.String(length=64), nullable=False),
        sa.Column('retrieved_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('effective_date', sa.String(length=10), nullable=False),
        sa.Column('verification_status', sa.String(length=50), nullable=False, server_default='UNVERIFIED'),
        sa.Column('verified_by', sa.String(length=36), nullable=True),
        sa.Column('verification_timestamp', sa.DateTime(timezone=True), nullable=True)
    )

    # 4. Source Conflicts Table
    op.create_table(
        'source_conflicts',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('concept_id', sa.String(length=36), sa.ForeignKey('concepts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_a_id', sa.String(length=36), sa.ForeignKey('sources.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_b_id', sa.String(length=36), sa.ForeignKey('sources.id', ondelete='CASCADE'), nullable=False),
        sa.Column('conflicting_claim', sa.Text(), nullable=False),
        sa.Column('specialty', sa.String(length=100), nullable=True),
        sa.Column('jurisdiction', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='REVIEW_REQUIRED'),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('resolved_by', sa.String(length=36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('source_conflicts')
    op.drop_table('syllabus_source_artifacts')
    op.drop_table('benchmark_cases')
    op.drop_table('medical_reviewer_profiles')
