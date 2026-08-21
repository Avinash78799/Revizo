-- ==============================================================================
-- NEET-PG AI Practice Platform: Row-Level Security (RLS) Policies
-- Database: PostgreSQL 15+ / Supabase
-- Purpose: Enforce database-level multi-tenant isolation for student data
-- ==============================================================================

-- 0. Auth Context Helper Functions (Supabase & Standard Postgres Compatible)
CREATE SCHEMA IF NOT EXISTS auth;

CREATE OR REPLACE FUNCTION auth.uid() RETURNS text AS $$
BEGIN
    RETURN NULLIF(current_setting('request.jwt.claim.sub', true), '');
END;
$$ LANGUAGE plpgsql STABLE;

CREATE OR REPLACE FUNCTION auth.jwt() RETURNS jsonb AS $$
BEGIN
    RETURN COALESCE(
        NULLIF(current_setting('request.jwt.claims', true), '')::jsonb, 
        jsonb_build_object(
            'role', current_setting('request.jwt.claim.role', true), 
            'sub', current_setting('request.jwt.claim.sub', true)
        )
    );
END;
$$ LANGUAGE plpgsql STABLE;

-- 1. Create Dedicated Non-Superuser Application Role for Multi-Tenant RLS
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'neetpg_app') THEN
        CREATE ROLE neetpg_app WITH LOGIN PASSWORD 'app_secure_password_2026';
    END IF;
END $$;

GRANT USAGE ON SCHEMA public TO neetpg_app;
GRANT USAGE ON SCHEMA auth TO neetpg_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO neetpg_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO neetpg_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA auth TO neetpg_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO neetpg_app;

-- 2. Enable & Force RLS on all student-owned performance tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles FORCE ROW LEVEL SECURITY;

ALTER TABLE test_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_sessions FORCE ROW LEVEL SECURITY;

ALTER TABLE test_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_attempts FORCE ROW LEVEL SECURITY;

ALTER TABLE student_concept_mastery ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_concept_mastery FORCE ROW LEVEL SECURITY;

ALTER TABLE student_question_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_question_history FORCE ROW LEVEL SECURITY;

ALTER TABLE revision_schedule ENABLE ROW LEVEL SECURITY;
ALTER TABLE revision_schedule FORCE ROW LEVEL SECURITY;

ALTER TABLE integrity_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE integrity_events FORCE ROW LEVEL SECURITY;

ALTER TABLE question_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE question_reports FORCE ROW LEVEL SECURITY;

-- 3. Profiles: Students can only view and update their own profile
DROP POLICY IF EXISTS student_profile_select ON profiles;
CREATE POLICY student_profile_select ON profiles
    FOR SELECT
    USING (auth.uid() = user_id OR (auth.jwt() ->> 'role' = 'admin'));

DROP POLICY IF EXISTS student_profile_update ON profiles;
CREATE POLICY student_profile_update ON profiles
    FOR UPDATE
    USING (auth.uid() = user_id);

-- 4. Test Sessions: Strict student ownership
DROP POLICY IF EXISTS student_sessions_select ON test_sessions;
CREATE POLICY student_sessions_select ON test_sessions
    FOR SELECT
    USING (auth.uid() = user_id OR (auth.jwt() ->> 'role' IN ('admin', 'medical_reviewer')));

DROP POLICY IF EXISTS student_sessions_insert ON test_sessions;
CREATE POLICY student_sessions_insert ON test_sessions
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- 5. Test Attempts: Student can only query their own attempts
DROP POLICY IF EXISTS student_attempts_select ON test_attempts;
CREATE POLICY student_attempts_select ON test_attempts
    FOR SELECT
    USING (auth.uid() = user_id OR (auth.jwt() ->> 'role' IN ('admin', 'medical_reviewer')));

DROP POLICY IF EXISTS student_attempts_insert ON test_attempts;
CREATE POLICY student_attempts_insert ON test_attempts
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- 6. Student Concept Mastery: Private to student
DROP POLICY IF EXISTS student_mastery_select ON student_concept_mastery;
CREATE POLICY student_mastery_select ON student_concept_mastery
    FOR SELECT
    USING (auth.uid() = user_id OR (auth.jwt() ->> 'role' = 'admin'));

DROP POLICY IF EXISTS student_mastery_all ON student_concept_mastery;
CREATE POLICY student_mastery_all ON student_concept_mastery
    FOR ALL
    USING (auth.uid() = user_id);

-- 7. Revision Schedule: Private to student
DROP POLICY IF EXISTS student_revision_all ON revision_schedule;
CREATE POLICY student_revision_all ON revision_schedule
    FOR ALL
    USING (auth.uid() = user_id);

-- 8. Integrity Events: Insert allowed by session owner, viewable by owner & admin
DROP POLICY IF EXISTS integrity_events_insert ON integrity_events;
CREATE POLICY integrity_events_insert ON integrity_events
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS integrity_events_select ON integrity_events;
CREATE POLICY integrity_events_select ON integrity_events
    FOR SELECT
    USING (auth.uid() = user_id OR (auth.jwt() ->> 'role' = 'admin'));

-- 9. Question Reports: Students can view their own reports; Admins/Reviewers can view all
DROP POLICY IF EXISTS reports_insert ON question_reports;
CREATE POLICY reports_insert ON question_reports
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS reports_select ON question_reports;
CREATE POLICY reports_select ON question_reports
    FOR SELECT
    USING (auth.uid() = user_id OR (auth.jwt() ->> 'role' IN ('admin', 'medical_reviewer')));
