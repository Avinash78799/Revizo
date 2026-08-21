import re
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone
from app.core.datetime_util import utc_now, ensure_utc

class ContentValidationEngine:
    """
    Automated Medical Question Validation Engine (Prompt 6, Sec 8, 9, 10, 24).
    Validates:
    - Single-Best-Answer requirements
    - Internal clinical vignette consistency & contradictions
    - Outdated content guidelines
    - Duplicate & similarity detection
    """

    @classmethod
    def validate_single_best_answer(
        cls,
        options: List[Dict[str, Any]],
        question_text: str = ""
    ) -> Tuple[bool, List[str]]:
        errors = []

        if len(options) < 4:
            errors.append(f"Question must have at least 4 options, found {len(options)}.")

        correct_count = sum(1 for opt in options if opt.get("is_correct") is True)
        if correct_count == 0:
            errors.append("Validation Failure: Exactly one correct option is required, but none was marked correct.")
        elif correct_count > 1:
            errors.append(f"Validation Failure: Exactly one correct option is required, but {correct_count} options were marked correct.")

        # Check duplicate or overlapping option texts
        option_texts = [str(opt.get("option_text", "")).strip().lower() for opt in options]
        if len(set(option_texts)) < len(option_texts):
            errors.append("Validation Failure: Duplicate option texts detected within the same question.")

        # Check giveaway wording
        for opt in options:
            text = str(opt.get("option_text", "")).lower()
            if text in ("all of the above", "none of the above", "both a and b", "both b and c"):
                errors.append(f"Quality Warning: Discouraged non-clinical option phrasing '{opt.get('option_text')}'. Single best clinical answer preferred.")

        is_valid = len(errors) == 0
        return is_valid, errors

    @classmethod
    def validate_clinical_vignette(cls, question_text: str) -> Tuple[bool, List[str]]:
        contradictions = []
        text_lower = question_text.lower()

        # Contradiction Check 1: Hypotension vs Normal/High Blood Pressure
        if "hypotensive" in text_lower or "hypotension" in text_lower or "in shock" in text_lower:
            bp_match = re.search(r"bp\s*(?:is|of|:)?\s*(\d{2,3})[/](\d{2,3})", text_lower)
            if bp_match:
                systolic = int(bp_match.group(1))
                if systolic >= 110:
                    contradictions.append(f"Contradiction: Stem describes patient as hypotensive/in shock, but reported BP is {systolic}/{bp_match.group(2)} mmHg (normotensive/hypertensive).")

        # Contradiction Check 2: Pediatric vs Adult Age
        if "pediatric" in text_lower or "child" in text_lower or "infant" in text_lower:
            age_match = re.search(r"(\d{1,2})[- ]year[- ]old", text_lower)
            if age_match:
                age = int(age_match.group(1))
                if age > 18:
                    contradictions.append(f"Contradiction: Stem describes pediatric case but specifies patient age as {age} years.")

        # Contradiction Check 3: Male vs Obstetric/Uterine conditions
        if "male" in text_lower and not "female" in text_lower:
            if "pregnant" in text_lower or "uterine" in text_lower or "cervical cancer" in text_lower or "preeclampsia" in text_lower:
                contradictions.append("Contradiction: Male demographic assigned to obstetric/uterine clinical pathology.")

        is_valid = len(contradictions) == 0
        return is_valid, contradictions

    @classmethod
    def check_outdated_status(
        cls,
        last_verified_at: Optional[datetime],
        review_due_at: Optional[datetime] = None
    ) -> Tuple[bool, Optional[str]]:
        now = utc_now()
        due = ensure_utc(review_due_at)

        if due and now > due:
            return True, f"Review overdue since {due.isoformat()}. Clinical guideline re-verification required."

        last_v = ensure_utc(last_verified_at)
        if last_v:
            days_since = (now - last_v).days
            if days_since > 365:
                return True, f"Question last verified {days_since} days ago (>1 year). Scheduled re-review due."

        return False, None

    @classmethod
    def calculate_similarity_score(cls, text_a: str, text_b: str) -> float:
        """
        Calculates normalized word-level Jaccard similarity for duplicate detection.
        """
        def tokenize(s: str) -> set:
            return set(re.findall(r'\b\w{3,}\b', s.lower()))

        words_a = tokenize(text_a)
        words_b = tokenize(text_b)

        if not words_a or not words_b:
            return 0.0

        intersection = words_a.intersection(words_b)
        union = words_a.union(words_b)
        return float(len(intersection)) / float(len(union))
