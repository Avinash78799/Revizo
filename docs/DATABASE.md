# NEET-PG AI Practice Platform: Database Schema & Entity Documentation

## Core Invariants
1. **Medical Truth & Provenance**: Questions are linked to `concepts`, `sources`, and `pyq_references`. No question can be labeled as a verified core question or a real PYQ without documented reference.
2. **Relational Integrity**: Deletion of a user cascades to attempts and mastery records, but question deletions are restricted if historical attempts exist.
3. **Structured Explanation Anatomy**: Every question maintains separate columns for:
   - `correct_explanation` (concise "Why")
   - `why_wrong_explanation` (per distractor in `question_options`)
   - `remember_takeaway` (high-yield pearl)
   - `exam_connection` (objective relevance context)
   - `detailed_explanation` (in-depth textbook context)

## Table Registry
- `users`: Core authentication and role records (`student`, `medical_reviewer`, `admin`).
- `profiles`: Student exam goals, target year, and practice targets.
- `subjects`: Medical disciplines (e.g., Pharmacology, Pathology, Anatomy).
- `chapters`: Major sections within subjects (e.g., Autonomic Nervous System).
- `topics`: Specific areas within chapters (e.g., Cholinergic System & Anticholinesterases).
- `concepts`: Atomic learning units with high-yield notes and clinical pearls.
- `sources`: Authoritative textbooks, clinical guidelines, and exam archives.
- `source_versions`: Version history and guideline updates for sources.
- `pyq_references`: Dedicated registry strictly distinguishing `real_pyq`, `pyq_derived_concept`, and `ai_generated_exam_style`.
- `questions`: Core question items with status, difficulty, trust class, and structured explanations.
- `question_options`: Strictly 4 options per question with distractor-specific explanations.
- `question_versions`: Immutable audit snapshots of question text, options, and explanations upon edits.
- `question_reviews`: Medical educator review decisions and audit notes.
- `question_quality_scorecards`: Automated & human validation criteria pass/fail ratings.
- `question_quarantine_registry`: Immediate isolation records for disputed or failed questions.
- `question_reports`: Student issue and error report queue.
- `test_templates`: Reusable blueprints for Quick Tests, Topic Tests, and Revision Sprints.
- `test_sessions`: Active and completed test instances with server-authoritative timer.
- `test_questions`: Order-preserved question manifest for each test session.
- `test_attempts`: Student answers, correctness, confidence (`definitely_know`, `somewhat_confident`, `guessing`), and time spent.
- `student_concept_mastery`: Concept-level mastery matrix, Danger Zone indicators, and adaptive spaced repetition schedules.
- `student_question_history`: Frequency of encounters and retention tracking per question.
- `revision_schedule`: Scheduled revision dates and completion statuses.
- `integrity_events`: Non-punitive browser event logging (tab switches, focus loss).
- `ai_generations`: AI prompt, model, token usage, and cost tracking.
- `ai_validation_results`: Multi-stage automated validation outcomes.
- `audit_logs`: Administrative actions and state change history.
