# Security & Data Isolation Architecture

## 1. Application-Level Authorization vs. Database RLS
We maintain defense-in-depth across two distinct layers:
1. **Application-Level Authorization (`AuthorizationService`)**:
   - Every route querying student-owned resources explicitly verifies that `current_user.id == resource.user_id`.
   - Verified across automated unit and integration tests.
2. **Database-Level Row-Level Security (PostgreSQL / Supabase RLS)**:
   - Defined in [database/rls_policies.sql](file:///c:/Users/91863/Downloads/neet%20pg%20pro/database/rls_policies.sql).
   - Enforces table-level policies on `profiles`, `test_sessions`, `test_attempts`, `student_concept_mastery`, `revision_schedule`, and `integrity_events`.
   - Tested against PostgreSQL using [tests/integration/test_postgres_rls.py](file:///c:/Users/91863/Downloads/neet%20pg%20pro/backend/tests/integration/test_postgres_rls.py).

## 2. Insecure Direct Object Reference (IDOR) Prevention
- Proved by `test_attack_idor_submission_to_another_users_attempt`:
  - Student A cannot submit answers to Student B's test session.
  - Student A cannot view Student B's test results.
  - Returns `403 Forbidden` with standardized error envelope.

## 3. Client Sanitization & Anti-Cheat
- During active testing, the server strips `is_correct`, `why_wrong_explanation`, `correct_explanation`, `remember_takeaway`, `exam_connection`, `detailed_explanation`, and all scorecard ratings.
- The client NEVER computes correctness or scores; the server is the sole authority.
- Test timing is strictly server-authoritative.

## 4. Question Quarantine & Withdrawal Safety
- Reporting a question with `is_serious_medical_error = True` triggers an automated quarantine transition in the same transaction, pulling the question from active rotation immediately.

## 5. Audit Logging
- Administrative actions (`question_published`, `question_quarantined`, `report_resolved`, `taxonomy_mutated`) are logged in `audit_logs` without capturing passwords, secrets, or tokens.
