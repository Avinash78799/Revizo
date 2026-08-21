"""Initial database schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-08-19 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Users & Profiles
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='student'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_users_email', 'users', ['email'])

    op.create_table(
        'profiles',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('full_name', sa.String(length=150), nullable=True),
        sa.Column('target_exam_year', sa.Integer(), nullable=True),
        sa.Column('daily_question_goal', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    # 2. Taxonomy
    op.create_table(
        'subjects',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('code', sa.String(length=20), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'chapters',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('subject_id', sa.String(length=36), sa.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('subject_id', 'name', name='uq_subject_chapter')
    )

    op.create_table(
        'topics',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('chapter_id', sa.String(length=36), sa.ForeignKey('chapters.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('chapter_id', 'name', name='uq_chapter_topic')
    )

    op.create_table(
        'concepts',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('topic_id', sa.String(length=36), sa.ForeignKey('topics.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('high_yield_notes', sa.Text(), nullable=True),
        sa.Column('clinical_pearl', sa.Text(), nullable=True),
        sa.Column('exam_relevance_score', sa.Float(), nullable=False, server_default='0.80'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_concepts_topic', 'concepts', ['topic_id'])

    # 3. Sources & PYQ Registry
    op.create_table(
        'sources',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('publisher', sa.String(length=150), nullable=True),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('edition_or_year', sa.String(length=50), nullable=True),
        sa.Column('reference_identifier', sa.String(length=150), nullable=True),
        sa.Column('license_status', sa.String(length=50), nullable=False, server_default='reference_only'),
        sa.Column('verified_by', sa.String(length=36), nullable=True),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'source_versions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('source_id', sa.String(length=36), sa.ForeignKey('sources.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_label', sa.String(length=50), nullable=False),
        sa.Column('changes_summary', sa.Text(), nullable=True),
        sa.Column('superseded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'pyq_references',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('concept_id', sa.String(length=36), sa.ForeignKey('concepts.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('exam_name', sa.String(length=50), nullable=False),
        sa.Column('exam_year', sa.Integer(), nullable=False),
        sa.Column('exam_session', sa.String(length=20), nullable=True),
        sa.Column('provenance_type', sa.String(length=50), nullable=False),
        sa.Column('source_id', sa.String(length=36), sa.ForeignKey('sources.id', ondelete='SET NULL'), nullable=True),
        sa.Column('verification_status', sa.String(length=50), nullable=False, server_default='verified'),
        sa.Column('historical_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    # 4. Questions & Lifecycle
    op.create_table(
        'questions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('concept_id', sa.String(length=36), sa.ForeignKey('concepts.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('trust_class', sa.String(length=50), nullable=False, server_default='ai_assisted_question'),
        sa.Column('question_type', sa.String(length=50), nullable=False, server_default='clinical_vignette'),
        sa.Column('difficulty', sa.String(length=20), nullable=False, server_default='moderate'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='draft'),
        sa.Column('is_high_yield', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('correct_explanation', sa.Text(), nullable=False),
        sa.Column('remember_takeaway', sa.Text(), nullable=False),
        sa.Column('exam_connection', sa.Text(), nullable=True),
        sa.Column('detailed_explanation', sa.Text(), nullable=True),
        sa.Column('source_id', sa.String(length=36), sa.ForeignKey('sources.id', ondelete='SET NULL'), nullable=True),
        sa.Column('source_citation', sa.String(length=255), nullable=True),
        sa.Column('pyq_reference_id', sa.String(length=36), sa.ForeignKey('pyq_references.id', ondelete='SET NULL'), nullable=True),
        sa.Column('is_ai_generated', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('ai_model_name', sa.String(length=50), nullable=True),
        sa.Column('prompt_version', sa.String(length=20), nullable=True),
        sa.Column('reviewed_by', sa.String(length=36), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.Column('text_hash', sa.String(length=64), nullable=False),
        sa.Column('content_version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('last_reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('review_due_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_questions_status_trust', 'questions', ['status', 'trust_class'])
    op.create_index('idx_questions_concept', 'questions', ['concept_id'])
    op.create_index('idx_questions_text_hash', 'questions', ['text_hash'])

    op.create_table(
        'question_options',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('option_key', sa.String(length=1), nullable=False),
        sa.Column('option_text', sa.Text(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('why_wrong_explanation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('question_id', 'option_key', name='uq_question_option_key')
    )

    op.create_table(
        'question_versions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('snapshot_data', sa.JSON(), nullable=False),
        sa.Column('changed_by', sa.String(length=36), nullable=True),
        sa.Column('change_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'question_reviews',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reviewer_id', sa.String(length=36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('verdict', sa.String(length=50), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'question_quality_scorecards',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('medical_accuracy_passed', sa.Boolean(), nullable=False),
        sa.Column('syllabus_alignment_passed', sa.Boolean(), nullable=False),
        sa.Column('single_best_answer_passed', sa.Boolean(), nullable=False),
        sa.Column('ambiguity_flag', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('source_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('duplicate_risk_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('overall_quality_score', sa.Float(), nullable=False),
        sa.Column('validation_report', sa.JSON(), nullable=False),
        sa.Column('evaluated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'question_reports',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('reason', sa.String(length=50), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('is_serious_medical_error', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('resolved', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('resolved_by', sa.String(length=36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'question_quarantine_registry',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('quarantine_reason', sa.String(length=100), nullable=False),
        sa.Column('resolution_status', sa.String(length=50), nullable=False, server_default='quarantined'),
        sa.Column('audit_notes', sa.Text(), nullable=True),
        sa.Column('quarantined_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revalidated_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 5. Tests & Attempts
    op.create_table(
        'test_templates',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('mode', sa.String(length=50), nullable=False),
        sa.Column('config', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'test_sessions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('template_id', sa.String(length=36), sa.ForeignKey('test_templates.id', ondelete='SET NULL'), nullable=True),
        sa.Column('mode', sa.String(length=50), nullable=False),
        sa.Column('subject_id', sa.String(length=36), sa.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True),
        sa.Column('chapter_id', sa.String(length=36), sa.ForeignKey('chapters.id', ondelete='SET NULL'), nullable=True),
        sa.Column('topic_id', sa.String(length=36), sa.ForeignKey('topics.id', ondelete='SET NULL'), nullable=True),
        sa.Column('total_questions', sa.Integer(), nullable=False),
        sa.Column('completed_questions', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('score', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True)
    )
    op.create_index('idx_sessions_user_mode', 'test_sessions', ['user_id', 'mode'])

    op.create_table(
        'test_questions',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('session_id', sa.String(length=36), sa.ForeignKey('test_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('session_id', 'order_index', name='uq_session_order')
    )

    op.create_table(
        'test_attempts',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('session_id', sa.String(length=36), sa.ForeignKey('test_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('concept_id', sa.String(length=36), sa.ForeignKey('concepts.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('selected_option_key', sa.String(length=1), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('confidence', sa.String(length=30), nullable=False, server_default='somewhat_confident'),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_danger_zone_item', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('answered_at', sa.DateTime(timezone=True), nullable=False)
    )
    op.create_index('idx_attempts_user_concept', 'test_attempts', ['user_id', 'concept_id'])
    op.create_index('idx_attempts_danger_zone', 'test_attempts', ['user_id', 'is_danger_zone_item'])

    # 6. Student Mastery, History & Revision
    op.create_table(
        'student_concept_mastery',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('concept_id', sa.String(length=36), sa.ForeignKey('concepts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('correct_attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('high_confidence_wrong_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('mastery_percentage', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('last_practiced_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('next_revision_due', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revision_interval_days', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('ease_factor', sa.Float(), nullable=False, server_default='2.50'),
        sa.Column('consecutive_correct_count', sa.Integer(), nullable=False, server_default='0'),
        sa.UniqueConstraint('user_id', 'concept_id', name='uq_user_concept_mastery')
    )

    op.create_table(
        'student_question_history',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_encounters', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('correct_encounters', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_encountered_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'revision_schedule',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('concept_id', sa.String(length=36), sa.ForeignKey('concepts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('scheduled_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True)
    )

    op.create_table(
        'integrity_events',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('session_id', sa.String(length=36), sa.ForeignKey('test_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('event_metadata', sa.JSON(), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False)
    )

    # 7. AI & Audit Logs
    op.create_table(
        'ai_generations',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('concept_id', sa.String(length=36), sa.ForeignKey('concepts.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('model_name', sa.String(length=50), nullable=False),
        sa.Column('prompt_version', sa.String(length=20), nullable=False),
        sa.Column('prompt_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completion_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_cost_usd', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('raw_response', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'ai_validation_results',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('generation_id', sa.String(length=36), sa.ForeignKey('ai_generations.id', ondelete='SET NULL'), nullable=True),
        sa.Column('question_id', sa.String(length=36), sa.ForeignKey('questions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('validator_version', sa.String(length=20), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('validation_stage', sa.String(length=50), nullable=False),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('actor_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('target_entity', sa.String(length=50), nullable=False),
        sa.Column('target_id', sa.String(length=36), nullable=False),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('ai_validation_results')
    op.drop_table('ai_generations')
    op.drop_table('integrity_events')
    op.drop_table('revision_schedule')
    op.drop_table('student_question_history')
    op.drop_table('student_concept_mastery')
    op.drop_table('test_attempts')
    op.drop_table('test_questions')
    op.drop_table('test_sessions')
    op.drop_table('test_templates')
    op.drop_table('question_quarantine_registry')
    op.drop_table('question_reports')
    op.drop_table('question_quality_scorecards')
    op.drop_table('question_reviews')
    op.drop_table('question_versions')
    op.drop_table('question_options')
    op.drop_table('questions')
    op.drop_table('pyq_references')
    op.drop_table('source_versions')
    op.drop_table('sources')
    op.drop_table('concepts')
    op.drop_table('topics')
    op.drop_table('chapters')
    op.drop_table('subjects')
    op.drop_table('profiles')
    op.drop_table('users')
