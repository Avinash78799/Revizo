"""
Seed rich, realistic Live Weekly Grand Tests and Subject-Wise Tests into test_templates.
"""
import uuid
import json
import sqlite3
from datetime import datetime, timedelta, timezone

def utc_now():
    return datetime.now(timezone.utc)

def main():
    conn = sqlite3.connect("backend/neet_pg.db")
    c = conn.cursor()

    # Clear old basic templates to populate the full professional suite
    c.execute("DELETE FROM test_templates")

    now = utc_now()
    # Live Grand Test active this weekend
    live_start = (now - timedelta(days=1)).isoformat()
    live_end = (now + timedelta(days=3)).isoformat()

    # Upcoming Grand Test next weekend
    upcoming_start = (now + timedelta(days=6)).isoformat()
    upcoming_end = (now + timedelta(days=9)).isoformat()

    templates = [
        # 1. LIVE All-India Weekly Grand Test
        (
            str(uuid.uuid4()),
            "All-India Weekly Grand Test #12 (2026 Season)",
            "weekly_grand_test",
            json.dumps({
                "question_count": 50,
                "time_limit_minutes": 60,
                "is_live": True,
                "live_window_start": live_start,
                "live_window_end": live_end,
                "syllabus_tag": "All 19 Subjects • Clinical Vignette NBE Pattern",
                "total_registered": 4820,
                "difficulty": "all",
                "badge": "LIVE NOW"
            }),
            now.isoformat()
        ),
        # 2. UPCOMING All-India Weekly Grand Test
        (
            str(uuid.uuid4()),
            "All-India Weekly Grand Test #13 (Upcoming)",
            "weekly_grand_test",
            json.dumps({
                "question_count": 50,
                "time_limit_minutes": 60,
                "is_live": False,
                "live_window_start": upcoming_start,
                "live_window_end": upcoming_end,
                "syllabus_tag": "Full Syllabus Simulation • All India Benchmarking",
                "total_registered": 2310,
                "difficulty": "all",
                "badge": "STARTS FRIDAY"
            }),
            now.isoformat()
        ),
        # 3. Clinical Block Mini Mock
        (
            str(uuid.uuid4()),
            "Clinical Block Mini Mock (Med + Surg + OBG + Peds)",
            "grand_test",
            json.dumps({
                "question_count": 30,
                "time_limit_minutes": 40,
                "is_live": True,
                "live_window_start": live_start,
                "live_window_end": live_end,
                "syllabus_tag": "High-Yield Clinical Vignettes & Next-Step Management",
                "total_registered": 1940,
                "difficulty": "all",
                "badge": "POPULAR"
            }),
            now.isoformat()
        ),
        # 4. Pre & Para Clinical High-Yield Drill
        (
            str(uuid.uuid4()),
            "Pre & Para-Clinical Rapid Recall Drill",
            "grand_test",
            json.dumps({
                "question_count": 25,
                "time_limit_minutes": 30,
                "is_live": True,
                "live_window_start": live_start,
                "live_window_end": live_end,
                "syllabus_tag": "Anatomy, Physio, Biochem, Path, Pharma, Micro",
                "total_registered": 1560,
                "difficulty": "all",
                "badge": "HIGH YIELD"
            }),
            now.isoformat()
        ),
        # 5. Daily Quick Test (10 MCQs)
        (
            str(uuid.uuid4()),
            "Daily Clinical Quick Test (10 Questions)",
            "quick_test",
            json.dumps({
                "question_count": 10,
                "time_limit_minutes": 12,
                "is_live": False,
                "syllabus_tag": "Daily 10-MCQ Rapid Sprint",
                "total_registered": 8900,
                "difficulty": "all",
                "badge": "DAILY SPRINT"
            }),
            now.isoformat()
        ),
        # 6. 5-Minute Spaced Rapid Revision
        (
            str(uuid.uuid4()),
            "5-Minute High-Yield Rapid Revision",
            "five_minute_revision",
            json.dumps({
                "question_count": 5,
                "time_limit_minutes": 5,
                "is_live": False,
                "syllabus_tag": "Due Spaced Repetition + Danger Zone Overconfidence Items",
                "total_registered": 6700,
                "difficulty": "all",
                "badge": "SM-2 REVISION"
            }),
            now.isoformat()
        ),
        # 7. PYQ Pattern & Recurrence Test
        (
            str(uuid.uuid4()),
            "NEET-PG PYQ Recurring Pattern Test",
            "pyq_pattern_test",
            json.dumps({
                "question_count": 20,
                "time_limit_minutes": 25,
                "is_live": False,
                "syllabus_tag": "2018–2025 Multi-Year High-Yield Recalls",
                "total_registered": 3400,
                "difficulty": "all",
                "badge": "PYQ PATTERN"
            }),
            now.isoformat()
        )
    ]

    # Now also create Subject-Wise Tests for all 19 NMC subjects
    c.execute("SELECT id, name, code FROM subjects ORDER BY order_index")
    subjects = c.fetchall()

    for s_id, s_name, s_code in subjects:
        templates.append((
            str(uuid.uuid4()),
            f"{s_name} Subject-Wise Test (SWT)",
            "subject_test",
            json.dumps({
                "question_count": 20,
                "time_limit_minutes": 25,
                "is_live": False,
                "subject_id": s_id,
                "subject_name": s_name,
                "subject_code": s_code,
                "syllabus_tag": f"Comprehensive {s_name} Core Clinical Practice",
                "total_registered": 1200,
                "difficulty": "all",
                "badge": f"{s_code} CORE"
            }),
            now.isoformat()
        ))

    c.executemany(
        "INSERT INTO test_templates (id, title, mode, config, created_at) VALUES (?, ?, ?, ?, ?)",
        templates
    )
    conn.commit()
    print(f"Successfully seeded {len(templates)} rich test templates into test_templates!")
    conn.close()

if __name__ == "__main__":
    main()
