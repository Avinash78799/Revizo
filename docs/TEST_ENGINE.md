# NEET-PG Test & Learning Engine Architecture

## 1. Test Session State Machine
```
[NOT_STARTED]
      │
      ▼
[IN_PROGRESS] ──────► [SUBMITTED]
      │
      ├─────────────► [EXPIRED] (Server-authoritative timer exceeds expires_at)
      │
      └─────────────► [CANCELLED]
```
- **Legal Transitions**:
  - `NOT_STARTED` $\rightarrow$ `IN_PROGRESS`
  - `IN_PROGRESS` $\rightarrow$ `SUBMITTED`, `EXPIRED`, `CANCELLED`
- **Illegal Transitions**:
  - `SUBMITTED` $\rightarrow$ `IN_PROGRESS` (Strictly rejected with 400 Bad Request).

## 2. Server-Authoritative Timer
- Backend computes `started_at = utc_now()` and `expires_at = started_at + timedelta(minutes=limit)`.
- The browser timer is strictly for UX presentation.
- When an answer submission arrives at `/tests/{attempt_id}/answers`:
  - If `now > expires_at`, the test session transitions to `EXPIRED`, and the submission is rejected with HTTP 422.

## 3. Idempotent Answer Evaluation
- If a client double-clicks, reconnects, or re-sends an answer for an already answered question within the session, the engine detects the existing record and returns the evaluation without creating duplicate attempts or incrementing the score twice.

## 4. Confidence Tracking & Danger Zone Engine
- **Confidence Tiers**: `DEFINITELY_KNOW`, `SOMEWHAT_CONFIDENT`, `GUESSING`.
- **Danger Zone**: Triggered when a student answers **Incorrectly** while choosing **`DEFINITELY_KNOW`**.
- This indicates an active clinical misconception rather than an unknown fact, which receives highest priority for corrective explanations and retesting.

## 5. Spaced Repetition (Modified SM-2)
- Correct answer $\rightarrow$ interval increases by ease factor $\times$ confidence multiplier.
- Incorrect answer $\rightarrow$ interval resets to 1 day; ease factor decreases.
- High-confidence error $\rightarrow$ extra ease penalty applied.
