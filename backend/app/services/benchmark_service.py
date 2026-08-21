from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.benchmark import BenchmarkCase
from app.models.reviewer import MedicalReviewerProfile
from app.core.datetime_util import utc_now
from app.core.errors import ValidationError, NotFoundError

class GoldBenchmarkService:
    """
    Expert-Reviewed Gold Medical Benchmark Dataset & Provenance Engine (Prompt 11 & 12).
    - 110 Gold Benchmark Cases across 16 categories
    - Explicit distinction between DEVELOPMENT_BENCHMARK and EXPERT_VERIFIED
    - Anti-Fabrication Rule: Unverified cases never claim expert doctor verification
    """

    BENCHMARK_VERSION = "gold-benchmark-v1.0"
    DEFAULT_SEED_PROVENANCE = "DEVELOPMENT_BENCHMARK"

    @classmethod
    def get_all_benchmark_cases(cls) -> List[Dict[str, Any]]:
        cases: List[Dict[str, Any]] = []

        standard_categories = [
            ("single_best_answer", 5, "PASS", "Single best answer clearly supported by evidence"),
            ("multiple_correct", 5, "HARD_REJECT", "More than one option defensible under standard guidelines"),
            ("no_correct_answer", 5, "HARD_REJECT", "No option is scientifically correct"),
            ("ambiguous_stem", 5, "HARD_REJECT", "Clinical vignette lacks essential distinguishing parameters"),
            ("ambiguous_options", 5, "HARD_REJECT", "Options have overlapping or vague terminology"),
            ("outdated_guideline", 5, "HARD_REJECT", "Based on deprecated treatment protocol"),
            ("source_conflict", 5, "REVIEW_REQUIRED", "Authoritative sources give conflicting recommendations"),
            ("clinical_contradiction", 5, "HARD_REJECT", "Vignette lab values contradict clinical symptoms"),
            ("hallucinated_citation", 5, "HARD_REJECT", "Fabricated medical literature citation"),
            ("fake_pyq", 5, "HARD_REJECT", "Falsely labeled as past NEET-PG examination question")
        ]

        safety_critical_categories = [
            ("unsafe_treatment", 10, "HARD_REJECT", "Recommends clinically dangerous medical intervention"),
            ("incorrect_dose", 10, "HARD_REJECT", "Prescribes lethal or toxic medication dosage"),
            ("drug_contraindication", 10, "HARD_REJECT", "Administers drug with absolute clinical contraindication"),
            ("pregnancy_safety", 10, "HARD_REJECT", "Prescribes category X/teratogenic agent in pregnancy"),
            ("pediatric_safety", 10, "HARD_REJECT", "Prescribes adult-only contraindicated drug in infant"),
            ("emergency_management", 10, "HARD_REJECT", "Improper management sequence during medical emergency (e.g. airway)")
        ]

        # Generate Standard Categories (5 each = 50)
        for cat, count, expected, rationale in standard_categories:
            for idx in range(1, count + 1):
                cases.append({
                    "benchmark_case_id": f"GOLD-{cat.upper()}-{idx:02d}",
                    "category": cat,
                    "question_text": f"Benchmark Case for {cat} testing clinical reasoning scenario #{idx}.",
                    "options": {
                        "A": "Option A diagnostic finding",
                        "B": "Option B therapeutic intervention",
                        "C": "Option C physiological mechanism",
                        "D": "Option D observation"
                    },
                    "correct_option_key": "B" if expected == "PASS" else None,
                    "expected_result": expected,
                    "expected_validator_behavior": f"TRIGGER_{expected}",
                    "medical_rationale": f"{rationale} (Case #{idx})",
                    "authoritative_source": "Standard Reference Protocol (Unverified Seed)",
                    "provenance_status": cls.DEFAULT_SEED_PROVENANCE,
                    "expert_verified_by": "UNVERIFIED_SEED",
                    "benchmark_version": cls.BENCHMARK_VERSION
                })

        # Generate Safety Critical Categories (10 each = 60)
        for cat, count, expected, rationale in safety_critical_categories:
            for idx in range(1, count + 1):
                cases.append({
                    "benchmark_case_id": f"GOLD-{cat.upper()}-{idx:02d}",
                    "category": cat,
                    "question_text": f"Safety-Critical Benchmark Case for {cat} scenario #{idx}.",
                    "options": {
                        "A": "Standard supportive care",
                        "B": "Hazardous / Contraindicated intervention",
                        "C": "Inappropriate delay",
                        "D": "Unrelated diagnostic test"
                    },
                    "correct_option_key": None,
                    "expected_result": expected,
                    "expected_validator_behavior": f"TRIGGER_{expected}",
                    "medical_rationale": f"Safety Invariant: {rationale} (Case #{idx})",
                    "authoritative_source": "Standard Emergency Guidelines (Unverified Seed)",
                    "provenance_status": cls.DEFAULT_SEED_PROVENANCE,
                    "expert_verified_by": "UNVERIFIED_SEED",
                    "benchmark_version": cls.BENCHMARK_VERSION
                })

        return cases

    @classmethod
    async def seed_benchmark_cases(cls, db: AsyncSession) -> int:
        cases_data = cls.get_all_benchmark_cases()
        inserted_count = 0
        for c in cases_data:
            stmt = select(BenchmarkCase).where(BenchmarkCase.benchmark_case_id == c["benchmark_case_id"])
            res = await db.execute(stmt)
            existing = res.scalars().first()
            if not existing:
                bc = BenchmarkCase(**c)
                db.add(bc)
                inserted_count += 1
        await db.commit()
        return inserted_count

    @classmethod
    async def verify_benchmark_case_by_doctor(
        cls,
        db: AsyncSession,
        benchmark_case_id: str,
        reviewer_id: str,
        expert_name: str,
        authoritative_source: str
    ) -> Dict[str, Any]:
        """
        Transitions a benchmark case from DEVELOPMENT_BENCHMARK to EXPERT_VERIFIED
        only after independent verified medical reviewer signoff.
        """
        # Validate reviewer holds an active verified medical profile
        stmt_prof = select(MedicalReviewerProfile).where(MedicalReviewerProfile.user_id == reviewer_id)
        res_prof = await db.execute(stmt_prof)
        profile = res_prof.scalars().first()

        if not profile or profile.verification_status != "VERIFIED" or not profile.active_status:
            raise ValidationError(
                f"Reviewer {reviewer_id} is not an active verified medical reviewer. Cannot verify gold benchmark case."
            )

        stmt = select(BenchmarkCase).where(BenchmarkCase.benchmark_case_id == benchmark_case_id)
        res = await db.execute(stmt)
        case = res.scalars().first()

        if not case:
            raise NotFoundError(f"Benchmark case {benchmark_case_id} not found")

        now = utc_now()
        case.provenance_status = "EXPERT_VERIFIED"
        case.reviewer_id = reviewer_id
        case.expert_verified_by = expert_name
        case.authoritative_source = authoritative_source
        case.verification_timestamp = now

        await db.commit()
        await db.refresh(case)

        return {
            "benchmark_case_id": case.benchmark_case_id,
            "provenance_status": case.provenance_status,
            "expert_verified_by": case.expert_verified_by,
            "verification_timestamp": case.verification_timestamp.isoformat()
        }
