from typing import List, Dict, Any
from app.models.test import TestAttempt

class ScoringService:
    """
    Dedicated deterministic scoring calculation engine.
    Calculates correct, incorrect, unanswered, NEET-PG scaled score,
    accuracy, time, confidence breakdown, 4-Quadrant Cognitive Diagnostics,
    and subject-wise performance breakdown.
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

        # 4-Quadrant Cognitive Diagnostic Breakdown (Exclusive to Revizo)
        # Zone 1: Concept Mastery / Genius Instinct (Correct & <45s)
        # Zone 2: Overthinking / Inefficient (Correct & >=45s)
        # Zone 3: Silly Mistake / Rash Guess (Incorrect & <30s) -> 5 marks swing (+4 lost + -1 penalty)
        # Zone 4: Knowledge Sinkhole / Time Trap (Incorrect & >=45s)
        genius_count = sum(1 for a in attempts if a.is_correct and (a.time_spent_seconds or 0) < 45)
        slow_correct_count = sum(1 for a in attempts if a.is_correct and (a.time_spent_seconds or 0) >= 45)
        silly_mistake_count = sum(1 for a in attempts if not a.is_correct and (a.time_spent_seconds or 0) < 30)
        sinkhole_count = sum(1 for a in attempts if not a.is_correct and (a.time_spent_seconds or 0) >= 45)
        moderate_mistake_count = incorrect_count - silly_mistake_count - sinkhole_count

        cognitive_quadrants = {
            "genius_count": genius_count,
            "slow_correct_count": slow_correct_count,
            "silly_mistake_count": silly_mistake_count,
            "sinkhole_count": sinkhole_count,
            "moderate_mistake_count": max(0, moderate_mistake_count),
            "silly_marks_lost": silly_mistake_count * 5  # Each silly mistake costs 4 marks missed + 1 negative mark
        }

        # Subject-Wise Performance Breakdown
        subject_stats: Dict[str, Dict[str, Any]] = {}
        for a in attempts:
            subj_name = "General Medical Science"
            subj_code = "GEN"
            try:
                if a.concept and a.concept.topic and a.concept.topic.chapter and a.concept.topic.chapter.subject:
                    subj_name = a.concept.topic.chapter.subject.name
                    subj_code = a.concept.topic.chapter.subject.code
                elif a.question and a.question.concept and a.question.concept.topic and a.question.concept.topic.chapter and a.question.concept.topic.chapter.subject:
                    subj_name = a.question.concept.topic.chapter.subject.name
                    subj_code = a.question.concept.topic.chapter.subject.code
            except Exception:
                pass

            if subj_name not in subject_stats:
                subject_stats[subj_name] = {
                    "subject_name": subj_name,
                    "subject_code": subj_code,
                    "total_questions": 0,
                    "correct_count": 0,
                    "incorrect_count": 0,
                    "time_spent_seconds": 0,
                    "score": 0,
                    "negative_marks": 0,
                    "accuracy_percentage": 0.0
                }
            stat = subject_stats[subj_name]
            stat["total_questions"] += 1
            stat["time_spent_seconds"] += (a.time_spent_seconds or 0)
            if a.is_correct:
                stat["correct_count"] += 1
                stat["score"] += 4
            else:
                stat["incorrect_count"] += 1
                stat["negative_marks"] += 1
                stat["score"] -= 1

        for stat in subject_stats.values():
            if stat["total_questions"] > 0:
                stat["accuracy_percentage"] = round((stat["correct_count"] / stat["total_questions"]) * 100.0, 1)

        # Sort subjects by net score ascending (weakest subjects first)
        sorted_subject_breakdown = sorted(subject_stats.values(), key=lambda s: s["score"])

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
            "confidence_breakdown": conf_stats,
            "cognitive_quadrants": cognitive_quadrants,
            "subject_breakdown": sorted_subject_breakdown
        }

