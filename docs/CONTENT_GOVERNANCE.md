# Content Governance & Medical Question Quality System

## 1. Non-Negotiable Core Principle
> **AI MAY PROPOSE. AI MAY ANALYZE. AI MAY VALIDATE. AI MUST NOT UNILATERALLY DECLARE MEDICAL CONTENT TRUSTED.**

No AI-generated question can enter `VERIFIED_CORE_QUESTION` without passing human medical review and guideline verification.

---

## 2. Question Lifecycle State Machine
```
[PROPOSED]
    │
    ├─────────────► [AI_VALIDATED] ──┐
    │                                │
    ├─────────────► [AUTHOR_VALIDATED]
    │                                │
    ▼                                ▼
[REVIEW_REQUIRED] ─────────────► [MEDICAL_REVIEW]
                                     │
                                     ├──────────► [APPROVED] ──► [PUBLISHED] ──► [MONITORED]
                                     │                              │
                                     ├──────────► [REJECTED]        ├──────────► [QUARANTINED]
                                     │                              ├──────────► [OUTDATED]
                                     └──────────► [QUARANTINED]     ├──────────► [WITHDRAWN]
                                                                    └──────────► [RETIRED]
```

- **Legal State Transitions**:
  - `PROPOSED` $\rightarrow$ `AI_VALIDATED`, `AUTHOR_VALIDATED`, `REVIEW_REQUIRED`, `REJECTED`
  - `AI_VALIDATED` $\rightarrow$ `REVIEW_REQUIRED`, `MEDICAL_REVIEW`, `REJECTED`, `QUARANTINED`
  - `REVIEW_REQUIRED` $\rightarrow$ `MEDICAL_REVIEW`, `REJECTED`, `QUARANTINED`
  - `MEDICAL_REVIEW` $\rightarrow$ `APPROVED`, `REJECTED`, `REVIEW_REQUIRED`, `QUARANTINED`
  - `APPROVED` $\rightarrow$ `PUBLISHED`, `QUARANTINED`, `WITHDRAWN`
  - `PUBLISHED` $\rightarrow$ `MONITORED`, `QUARANTINED`, `OUTDATED`, `WITHDRAWN`, `RETIRED`
  - `MONITORED` $\rightarrow$ `QUARANTINED`, `OUTDATED`, `WITHDRAWN`, `RETIRED`, `REVIEW_REQUIRED`
  - `QUARANTINED` $\rightarrow$ `REVIEW_REQUIRED`, `MEDICAL_REVIEW`, `WITHDRAWN`, `RETIRED`, `PUBLISHED`

---

## 3. Trust Classes
1. `DEVELOPMENT_SEED`: Development-only bootstrap questions isolated from production test pool.
2. `AI_PROPOSED`: Raw candidate proposal from AI.
3. `AUTHOR_CREATED`: Raw candidate created by doctor author.
4. `REVIEW_PENDING`: In active automated validation or queued for review.
5. `MEDICALLY_REVIEWED`: Formally reviewed by licensed physician.
6. `VERIFIED_CORE_QUESTION`: Fully verified and published to the student practice pool.
7. `WITHDRAWN`: Revoked question preserved strictly for historical test reproducibility.

---

## 4. Multi-Pass Medical Validation Pipeline
1. **Pass 1 (Deterministic SBA Check)**: Verifies $\ge 4$ options, exactly one `is_correct == True`, unique option texts, and absence of giveaway phrasing.
2. **Pass 2 (Clinical Vignette Contradiction Check)**: Flags demographic, vital sign, and clinical pathology discrepancies (e.g. "hypotensive" with BP 150/90).
3. **Pass 3 (Primary AI Medical Validation)**: Strict Pydantic parsing of structured JSON (`clinical_accuracy`, `single_best_answer`, `ambiguity_risk`, `source_support`, `recommendation`).
4. **Pass 4 (Secondary Independent Cross-Check)**: Independent validation check.
5. **Pass 5 (Disagreement & Risk Classification)**: If Validator 1 and Validator 2 disagree $\rightarrow$ routes question to `REVIEW_REQUIRED` with elevated priority.
6. **Pass 6 (AI Call Logging)**: Immutable tracking of provider, model, prompt hash, tokens, latency, cost, and errors in `ai_call_logs`.

---

## 5. Provenance & Evidence Registry
- **Source Registry**: `title`, `source_type` (`STANDARD_TEXTBOOK`, `GUIDELINE`, `OFFICIAL_DOCUMENT`, `PEER_REVIEWED_ARTICLE`, etc.), `edition`, `publication_year`, `publisher`, `reference_identifier` (ISBN/DOI/PMID).
- **Evidence References**: Factual claims linked to sources without storing full-text copyrighted books.
- **PYQ Provenance**: Strictly isolates `REAL_PYQ` with exam name, exam year, session, and independent doctor reviewer stamp. Unverified questions default to `UNKNOWN`.

---

## 6. Immutable Versioning & Test Reproducibility
- Content changes increment `content_version` and create an immutable `QuestionVersion` record snapshotting question stem, options, correct answer, distractor explanations, and sources.
- Historical `TestAttempt` records remain permanently bound to the specific question version active at the time of the test attempt.

---

## 7. Auto-Quarantine Feedback Loop
- Question reports flagged with `is_serious_medical_error == True` immediately trigger an automated quarantine transaction, removing the question from new student tests while preserving all past attempt records.
