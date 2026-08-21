# AI Question Intelligence Engine Architecture

## 1. Core Operating Principle
> **AI GENERATES POSSIBILITIES. EVIDENCE SUPPORTS CLAIMS. VALIDATORS FIND PROBLEMS. HUMANS APPROVE MEDICAL CONTENT. THE TRUSTED QUESTION BANK IS NEVER AI-OWNED.**

AI serves strictly as an intelligent assistant to the medical content pipeline. It has zero authority to unilaterally publish questions into the student pool.

---

## 2. End-to-End Pipeline
```
SYLLABUS (Taxonomy)
   │
   ▼
CONCEPT PRIORITY ENGINE (Calculates High-Yield & Diagnostic Priority)
   │
   ▼
EVIDENCE RETRIEVAL (Loads verified textbooks, pearls & guideline notes)
   │ (If insufficient -> Refuses generation: INSUFFICIENT_EVIDENCE)
   ▼
PROMPT BUILDER (Versioned guardrails: single best answer, 4 distractors, no giveaway cues)
   │
   ▼
AI PROVIDER ABSTRACTION (Mock / OpenAI / Anthropic / Local models)
   │
   ▼
STRUCTURED OUTPUT PARSER (Pydantic schema validation)
   │
   ▼
MULTI-STAGE MEDICAL VALIDATION
   ├── Deterministic SBA Validator (Exactly 1 correct, 4 distinct options)
   ├── Clinical Vignette Validator (Vitals vs symptoms contradiction check)
   ├── Primary AI Medical Validator (Clinical accuracy & guideline check)
   ├── Adversarial Validator (Actively attempts to refute the question)
   └── Distractor Validator (Checks plausibility, eliminates absurd options)
   │
   ▼
DEDUPLICATION ENGINE (Jaccard similarity & text hash comparison)
   │ (If similarity > 0.85 -> Refused: DUPLICATE_REJECTED)
   ▼
QUALITY SCORECARD & GOVERNANCE DECISION
   │ (Saved in 'AI_VALIDATED' / 'REVIEW_REQUIRED' with 'REVIEW_PENDING' trust class)
   ▼
HUMAN MEDICAL REVIEW QUEUE (Licensed physician review & sign-off)
   │
   ▼
VERIFIED QUESTION POOL (`VERIFIED_CORE_QUESTION` / `PUBLISHED`)
   │
   ▼
STUDENT PRACTICE ENGINE
```

---

## 3. High-Yield Concept Priority Engine
Calculates transparent priority metrics:
- **Curriculum Importance** (30% weight): Core syllabus weight and exam frequency.
- **PYQ Recurrence** (25% weight): Historical frequency in verified NEET-PG/INI-CET archives.
- **Student Misconceptions** (25% weight): Aggregate frequency of `WRONG + DEFINITELY_KNOW` (Danger Zone) failures.
- **Content Coverage Gap** (20% weight): Inverse of verified question count ($< 2$ questions = high generation priority).

---

## 4. Adversarial & Multi-Stage Validation
- **Medical Validator**: Evaluates clinical reasoning, single best answer quality, and guideline compliance.
- **Adversarial Validator**: Challenges the proposed question:
  - *Could another option be reasonably defended?*
  - *Is there an unstated assumption?*
  - *Is there a clinical contradiction?*
- **Consensus & Disagreement Handling**: If Validator A passes and Validator B rejects, the pipeline records a validator disagreement and routes the question to `REVIEW_REQUIRED`.

---

## 5. Evaluation Benchmark Framework
- Includes a permanent benchmark dataset (`NEETPG-GOLD-VALIDATION-BENCHMARK-v1`) with known clinical facts, intentional ambiguities, and vignette contradictions.
- Automatically calculates:
  - `accuracy_score`
  - `false_positive_rate`
  - `false_negative_rate`
- Benchmarks new prompt versions and AI models before deployment to prevent regressions.

---

## 6. AI Observability & Cost Control
- Every AI request logs token usage, latency, prompt hash, and estimated cost to `AICallLog`.
- Caching prevents redundant LLM calls on unchanged question text hashes.
- Daily generation quotas prevent accidental runaway generation loops.
