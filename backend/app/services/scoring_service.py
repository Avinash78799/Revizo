from typing import List, Dict, Any
from app.models.test import TestAttempt

class ScoringService:
    """
    Dedicated deterministic scoring calculation engine.
    Calculates correct, incorrect, unanswered, NEET-PG scaled score,
    accuracy, time, and confidence breakdown.
    """

    @staticmethod
    def calculate_session_score(
        total_questions: int,
        attempts: List[TestAttempt]
    ) -> Dict[str, Any]:
        correct_count = sum(1 for a in attempts if a.is_correct)
        incorrect_count = sum(1 for a in attempts if not a.is_correct)
        unanswered_count = max(0, total_questions - len(attempts))
        
        # NEET-PG Scoring Convention: +4 for correct, -1 for incorrect, 0 for unattempted
        neet_pg_score = (correct_count * 4) - (incorrect_count * 1)
        max_possible_score = total_questions * 4
        
        accuracy_percentage = (
            round((correct_count / len(attempts)) * 100.0, 1)
            if len(attempts) > 0
            else 0.0
        )
        
        total_time_seconds = sum(a.time_spent_seconds for a in attempts)
        avg_time_per_question = (
            round(total_time_seconds / len(attempts), 1)
            if len(attempts) > 0
            else 0.0
        )
        
        # Confidence breakdown
        conf_stats: Dict[str, Dict[str, int]] = {
            "DEFINITELY_KNOW": {"total": 0, "correct": 0, "incorrect": 0},
            "SOMEWHAT_CONFIDENT": {"total": 0, "correct": 0, "incorrect": 0},
            "GUESSING": {"total": 0, "correct": 0, "incorrect": 0}
        }
        
        danger_zone_count = 0
        for a in attempts:
            conf_key = a.confidence.upper() if a.confidence else "SOMEWHAT_CONFIDENT"
            if conf_key not in conf_stats:
                conf_key = "SOMEWHAT_CONFIDENT"
                
            conf_stats[conf_key]["total"] += 1
            if a.is_correct:
                conf_stats[conf_key]["correct"] += 1
            else:
                conf_stats[conf_key]["incorrect"] += 1
                if conf_key == "DEFINITELY_KNOW":
                    danger_zone_count += 1

        # Calibration Calculation: how often stated confidence matched actual correctness
        calibrated_points = 0.0
        for a in attempts:
            conf = (a.confidence or "SOMEWHAT_CONFIDENT").upper()
            if conf == "DEFINITELY_KNOW":
                if a.is_correct:
                    calibrated_points += 1.0
            elif conf in ["GUESSING", "LOW", "UNSURE"]:
                if not a.is_correct:
                    calibrated_points += 1.0
                else:
                    calibrated_points += 0.3
            else:  # SOMEWHAT_CONFIDENT
                if a.is_correct:
                    calibrated_points += 0.8
                else:
                    calibrated_points += 0.5

        calibration_percentage = (
            round((calibrated_points / len(attempts)) * 100.0, 1)
            if len(attempts) > 0
            else 0.0
        )

        return {
            "total_questions": total_questions,
            "attempted_count": len(attempts),
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "unanswered_count": unanswered_count,
            "score": neet_pg_score,
            "max_possible_score": max_possible_score,
            "accuracy_percentage": accuracy_percentage,
            "calibration_percentage": calibration_percentage,
            "total_time_seconds": total_time_seconds,
            "avg_time_per_question_seconds": avg_time_per_question,
            "danger_zone_count": danger_zone_count,
            "confidence_breakdown": conf_stats
        }
