# NEET-PG Platform: REST API Reference (v1)

## Base URL
`/api/v1`

## Authentication
Bearer token in `Authorization: Bearer <access_token>` header.

---

## 1. Health & Readiness (Root)
- `GET /health`: Liveness probe. Returns `{"status": "healthy", "service": "neet-pg-api", "version": "1.0.0"}`.
- `GET /ready`: Readiness probe. Runs `SELECT 1` on database. Returns `{"status": "ready", "database": "connected"}`.

---

## 2. Authentication (`/auth`)
- `POST /api/v1/auth/register`
  - Body: `{"email": "dr.smith@neetpg.pro", "password": "...", "full_name": "Dr. Smith", "target_exam_year": 2026}`
  - Returns: `{"access_token": "...", "token_type": "bearer", "user_id": "...", "role": "student"}`
- `POST /api/v1/auth/login`
  - Body: `{"email": "...", "password": "..."}`
  - Returns: `{"access_token": "...", "token_type": "bearer", "user_id": "...", "role": "student"}`
- `GET /api/v1/auth/me`
  - Headers: `Authorization: Bearer <token>`
  - Returns: Authenticated user details, exam goal, and daily question target.
- `POST /api/v1/auth/logout`
  - Acknowledges client-side token termination.

---

## 3. Curriculum Taxonomy (`/taxonomy`)
- `GET /api/v1/taxonomy/subjects`: List all active subjects with ordering.
- `GET /api/v1/taxonomy/subjects/{id}/tree`: Full hierarchical tree (Subject $\rightarrow$ Chapters $\rightarrow$ Topics $\rightarrow$ Concepts).
- `GET /api/v1/taxonomy/chapters`: Filterable by `subject_id`.
- `GET /api/v1/taxonomy/topics`: Filterable by `chapter_id`.
- `GET /api/v1/taxonomy/concepts`: Filterable by `topic_id`.
- `POST /api/v1/taxonomy/subjects` [Admin]
- `POST /api/v1/taxonomy/chapters` [Admin]
- `POST /api/v1/taxonomy/topics` [Admin]
- `POST /api/v1/taxonomy/concepts` [Admin]
- `DELETE /api/v1/taxonomy/concepts/{id}` [Admin]: Safe deletion (aborts with 409 Conflict if active questions exist).

---

## 4. Practice Tests & Runner (`/tests`)
- `POST /api/v1/tests/start`
  - Body: `{"mode": "quick_test", "question_count": 5, "subject_id": "...", "topic_id": "..."}`
  - Returns: `TestSessionResponse` with **strictly sanitized questions** (no correct keys, no explanations).
- `POST /api/v1/tests/{attempt_id}/answers`
  - Body: `{"question_id": "...", "selected_option_key": "B", "confidence": "DEFINITELY_KNOW", "time_spent_seconds": 18}`
  - Returns: `EvaluationResultResponse` (server-evaluated correctness, why correct, distractor explanation, remember takeaway, danger zone indicator).
  - Idempotent: repeated identical submissions return the cached evaluation without duplicate records.
- `GET /api/v1/tests/{attempt_id}/result`
  - Returns: Detailed breakdown and scoring summary (NEET-PG +4/-1 score, accuracy, confidence stats).
- `POST /api/v1/tests/retest-concept`
  - Body: `{"concept_id": "...", "exclude_question_id": "..."}`
  - Returns: Alternative sanitized question for the same concept.
- `POST /api/v1/tests/{attempt_id}/integrity-events`
  - Body: `{"event_type": "TAB_HIDDEN", "metadata": {...}}`

---

## 5. Spaced Revision (`/revision`)
- `GET /api/v1/revision/due`: Returns list of concepts due for spaced review.
- `POST /api/v1/revision/complete`: Marks a scheduled revision item completed.
- `POST /api/v1/revision/five-minute-session`: Generates a bounded 5-question high-yield revision test session.

---

## 6. Student Intelligence & Dashboard (`/student`)
- `GET /api/v1/dashboard`: Real-time student diagnostics (today's practice, due revisions, weak areas, danger zone count).
- `GET /api/v1/student/danger-zone`: List of high-confidence wrong concept items.
- `GET /api/v1/student/mistakes`: Searchable mistake bank.
- `GET /api/v1/student/mastery`: Concept-level mastery matrix.

---

## 7. Admin & Medical Review (`/admin`)
- `GET /api/v1/admin/review-queue`: Candidate questions awaiting review.
- `POST /api/v1/admin/questions/{id}/publish`: Approves and publishes question to verified pool.
- `POST /api/v1/admin/questions/{id}/quarantine`: Immediately isolates question from all active tests.
- `POST /api/v1/admin/reports/{id}/resolve`: Resolves student issue reports.

---

## 8. Content Governance & Quality (`/admin/governance`)
- `GET /api/v1/admin/governance/dashboard`: Overall governance statistics (total, verified, pending, AI proposed, quarantined, outdated, pending reports).
- `GET /api/v1/admin/governance/coverage`: Topic-wise verified coverage matrix with gap identification.
- `POST /api/v1/admin/governance/validate/{question_id}`: Executes multi-pass automated medical validation pipeline.
- `POST /api/v1/admin/governance/review-decision`: Submits doctor review decision (`APPROVE`, `REJECT`, `REQUEST_REVISION`, `QUARANTINE`, `MARK_OUTDATED`).
- `POST /api/v1/admin/governance/sources`: Registers source citation in source registry.
- `POST /api/v1/admin/governance/evidence`: Links structured evidence reference.
- `POST /api/v1/admin/governance/pyq-verify`: Verifies PYQ provenance with verified reviewer stamp.
