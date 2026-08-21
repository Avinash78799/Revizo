-- ==========================================
-- NEET-PG AI Practice & Revision Platform
-- PostgreSQL & Supabase Database Initialization Script
-- ==========================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. USERS & PROFILES
CREATE TYPE user_role AS ENUM ('student', 'medical_reviewer', 'admin');

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'student',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(150),
    target_exam_year INT,
    daily_question_goal INT NOT NULL DEFAULT 10,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. TAXONOMY
CREATE TABLE IF NOT EXISTS subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    order_index INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    order_index INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(subject_id, name)
);
CREATE INDEX IF NOT EXISTS idx_chapters_subject ON chapters(subject_id);

CREATE TABLE IF NOT EXISTS topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    order_index INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(chapter_id, name)
);
CREATE INDEX IF NOT EXISTS idx_topics_chapter ON topics(chapter_id);

CREATE TABLE IF NOT EXISTS concepts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    high_yield_notes TEXT,
    clinical_pearl TEXT,
    exam_relevance_score NUMERIC(3, 2) NOT NULL DEFAULT 0.80 CHECK (exam_relevance_score BETWEEN 0.00 AND 1.00),
    embedding vector(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_concepts_topic ON concepts(topic_id);

-- 3. SOURCES & PYQS
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(150),
    source_type VARCHAR(50) NOT NULL,
    edition_or_year VARCHAR(50),
    reference_identifier VARCHAR(150),
    license_status VARCHAR(50) NOT NULL DEFAULT 'reference_only',
    verified_by UUID REFERENCES users(id),
    verified_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    version_label VARCHAR(50) NOT NULL,
    changes_summary TEXT,
    superseded_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TYPE pyq_provenance_type AS ENUM ('real_pyq', 'pyq_derived_concept', 'ai_generated_exam_style');

CREATE TABLE IF NOT EXISTS pyq_references (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE RESTRICT,
    exam_name VARCHAR(50) NOT NULL,
    exam_year INT NOT NULL,
    exam_session VARCHAR(20),
    provenance_type pyq_provenance_type NOT NULL,
    source_id UUID REFERENCES sources(id) ON DELETE SET NULL,
    verification_status VARCHAR(50) NOT NULL DEFAULT 'verified',
    historical_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_pyq_concept ON pyq_references(concept_id);

-- 4. QUESTIONS
CREATE TYPE question_status AS ENUM (
    'draft', 'ai_generated', 'validating', 'review_required',
    'verified', 'published', 'quarantined', 'retired'
);

CREATE TYPE question_trust_class AS ENUM (
    'verified_core_question', 'ai_assisted_question', 'dynamic_practice_question'
);

CREATE TYPE question_difficulty AS ENUM ('easy', 'moderate', 'hard');
CREATE TYPE question_type AS ENUM ('clinical_vignette', 'single_best_answer', 'rapid_recall', 'image_based', 'assertion_reasoning');

CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE RESTRICT,
    trust_class question_trust_class NOT NULL DEFAULT 'ai_assisted_question',
    question_type question_type NOT NULL DEFAULT 'clinical_vignette',
    difficulty question_difficulty NOT NULL DEFAULT 'moderate',
    status question_status NOT NULL DEFAULT 'draft',
    is_high_yield BOOLEAN NOT NULL DEFAULT false,
    
    question_text TEXT NOT NULL,
    image_url TEXT,
    
    correct_explanation TEXT NOT NULL,
    remember_takeaway TEXT NOT NULL,
    exam_connection TEXT,
    detailed_explanation TEXT,
    
    source_id UUID REFERENCES sources(id) ON DELETE SET NULL,
    source_citation TEXT,
    pyq_reference_id UUID REFERENCES pyq_references(id) ON DELETE SET NULL,
    
    is_ai_generated BOOLEAN NOT NULL DEFAULT true,
    ai_model_name VARCHAR(50),
    prompt_version VARCHAR(20),
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,
    review_notes TEXT,
    
    text_hash VARCHAR(64) NOT NULL,
    embedding vector(1536),
    content_version INT NOT NULL DEFAULT 1,
    last_reviewed_at TIMESTAMPTZ,
    review_due_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_questions_status_trust ON questions(status, trust_class);
CREATE INDEX IF NOT EXISTS idx_questions_concept ON questions(concept_id);
CREATE INDEX IF NOT EXISTS idx_questions_text_hash ON questions(text_hash);

CREATE TABLE IF NOT EXISTS question_options (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    option_key CHAR(1) NOT NULL CHECK (option_key IN ('A', 'B', 'C', 'D')),
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT false,
    why_wrong_explanation TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(question_id, option_key)
);
CREATE INDEX IF NOT EXISTS idx_options_question ON question_options(question_id);

CREATE TABLE IF NOT EXISTS question_quality_scorecards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE UNIQUE,
    medical_accuracy_passed BOOLEAN NOT NULL,
    syllabus_alignment_passed BOOLEAN NOT NULL,
    single_best_answer_passed BOOLEAN NOT NULL,
    ambiguity_flag BOOLEAN NOT NULL DEFAULT false,
    source_verified BOOLEAN NOT NULL DEFAULT false,
    duplicate_risk_score NUMERIC(3, 2) DEFAULT 0.00,
    overall_quality_score NUMERIC(3, 2) NOT NULL,
    validation_report JSONB NOT NULL,
    evaluated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS question_quarantine_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    quarantine_reason VARCHAR(100) NOT NULL,
    resolution_status VARCHAR(50) NOT NULL DEFAULT 'quarantined',
    audit_notes TEXT,
    quarantined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    revalidated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS question_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    reason VARCHAR(50) NOT NULL,
    comment TEXT,
    is_serious_medical_error BOOLEAN NOT NULL DEFAULT false,
    resolved BOOLEAN NOT NULL DEFAULT false,
    resolved_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. TESTS & ATTEMPTS
CREATE TYPE test_mode AS ENUM (
    'quick_test', 'topic_test', 'chapter_test', 'rapid_recall',
    'weekly_test', 'mistake_revision', 'adaptive', 'five_minute_revision', 'grand_test'
);

CREATE TABLE IF NOT EXISTS test_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(150) NOT NULL,
    mode test_mode NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    template_id UUID REFERENCES test_templates(id),
    mode test_mode NOT NULL,
    subject_id UUID REFERENCES subjects(id) ON DELETE SET NULL,
    chapter_id UUID REFERENCES chapters(id) ON DELETE SET NULL,
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    total_questions INT NOT NULL,
    completed_questions INT NOT NULL DEFAULT 0,
    score INT NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_sessions_user_mode ON test_sessions(user_id, mode, started_at DESC);

CREATE TYPE confidence_level AS ENUM ('definitely_know', 'somewhat_confident', 'guessing');

CREATE TABLE IF NOT EXISTS test_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES test_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE RESTRICT,
    concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE RESTRICT,
    selected_option_key CHAR(1),
    is_correct BOOLEAN NOT NULL,
    confidence confidence_level NOT NULL DEFAULT 'somewhat_confident',
    time_spent_seconds INT NOT NULL DEFAULT 0,
    is_danger_zone_item BOOLEAN NOT NULL DEFAULT false,
    answered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_attempts_user_concept ON test_attempts(user_id, concept_id);
CREATE INDEX IF NOT EXISTS idx_attempts_danger_zone ON test_attempts(user_id, is_danger_zone_item);

CREATE TABLE IF NOT EXISTS student_concept_mastery (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    total_attempts INT NOT NULL DEFAULT 0,
    correct_attempts INT NOT NULL DEFAULT 0,
    high_confidence_wrong_count INT NOT NULL DEFAULT 0,
    mastery_percentage NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    
    last_practiced_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    next_revision_due TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '1 day',
    revision_interval_days INT NOT NULL DEFAULT 1,
    ease_factor NUMERIC(3, 2) NOT NULL DEFAULT 2.50,
    consecutive_correct_count INT NOT NULL DEFAULT 0,
    
    UNIQUE(user_id, concept_id)
);
CREATE INDEX IF NOT EXISTS idx_mastery_user_due ON student_concept_mastery(user_id, next_revision_due);

CREATE TABLE IF NOT EXISTS integrity_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES test_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_metadata JSONB,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. AI LOGS & AUDIT LOGS
CREATE TABLE IF NOT EXISTS ai_generations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concept_id UUID NOT NULL REFERENCES concepts(id) ON DELETE RESTRICT,
    provider VARCHAR(50) NOT NULL,
    model_name VARCHAR(50) NOT NULL,
    prompt_version VARCHAR(20) NOT NULL,
    prompt_tokens INT NOT NULL DEFAULT 0,
    completion_tokens INT NOT NULL DEFAULT 0,
    estimated_cost_usd NUMERIC(8, 6) DEFAULT 0.00,
    raw_response JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    target_entity VARCHAR(50) NOT NULL,
    target_id UUID NOT NULL,
    details JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
