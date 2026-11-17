import sqlite3
import json
import uuid
import os

def seed_test_series():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neet_pg.db")
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Fetch all subjects for mapping
    c.execute("SELECT id, name, code FROM subjects")
    subjects_map = {row[1]: (row[0], row[2]) for row in c.fetchall()}

    def get_subj_id(name):
        return subjects_map.get(name, (None, None))[0]

    # Pre-calculate subject bundles
    clinical_quad = [get_subj_id("General Medicine"), get_subj_id("General Surgery"), get_subj_id("Obstetrics & Gynecology"), get_subj_id("Pediatrics")]
    pre_para_block = [get_subj_id("Anatomy"), get_subj_id("Physiology"), get_subj_id("Biochemistry"), get_subj_id("Pathology"), get_subj_id("Pharmacology"), get_subj_id("Microbiology"), get_subj_id("Forensic Medicine"), get_subj_id("Community Medicine")]
    emergency_block = [get_subj_id("General Medicine"), get_subj_id("Anesthesiology"), get_subj_id("General Surgery"), get_subj_id("Radiodiagnosis")]
    neuro_block = [get_subj_id("General Medicine"), get_subj_id("Anatomy"), get_subj_id("Psychiatry")]
    nephro_block = [get_subj_id("General Medicine"), get_subj_id("Pathology"), get_subj_id("Physiology")]
    endo_block = [get_subj_id("General Medicine"), get_subj_id("Biochemistry"), get_subj_id("Pharmacology")]
    pulm_infectious = [get_subj_id("General Medicine"), get_subj_id("Microbiology"), get_subj_id("Radiodiagnosis")]
    pharma_toxic = [get_subj_id("Pharmacology"), get_subj_id("Forensic Medicine"), get_subj_id("Anesthesiology")]
    screening_block = [get_subj_id("Community Medicine"), get_subj_id("Obstetrics & Gynecology"), get_subj_id("Pediatrics"), get_subj_id("Dermatology")]
    derm_path = [get_subj_id("Dermatology"), get_subj_id("Pathology")]
    cardio_rhythm = [get_subj_id("Physiology"), get_subj_id("General Medicine")]

    SERIES_TEMPLATES = [
        # =====================================================================
        # 1. NEET-PG PRO SERIES (Flagship All-India Mocks)
        # =====================================================================
        {
            "id": "neet-pg-pro-gt-01",
            "title": "NEET-PG Pro Grand Test #1: All-India NBE 4-Section Mock",
            "mode": "weekly_grand_test",
            "config": {
                "series_category": "neet_pg_pro",
                "test_type": "NBE 4-SECTION SIMULATION",
                "question_count": 50,
                "time_limit_minutes": 60,
                "is_live": True,
                "badge": "LIVE NOW",
                "syllabus_tag": "All 19 NMC Disciplines • Sections A, B, C & D • Cutoff Predictor",
                "target_audience": "All NEET-PG Aspirants",
                "total_registered": 5420,
                "difficulty": "all",
                "clinical_focus": "Balanced 19-Subject Clinical Vignette Simulation"
            }
        },
        {
            "id": "neet-pg-pro-gt-02",
            "title": "NEET-PG Pro Grand Test #2: High-Yield Re-Test (Upcoming)",
            "mode": "weekly_grand_test",
            "config": {
                "series_category": "neet_pg_pro",
                "test_type": "NBE 4-SECTION SIMULATION",
                "question_count": 50,
                "time_limit_minutes": 60,
                "is_live": False,
                "badge": "OPENS SUNDAY",
                "syllabus_tag": "Full 19 Subjects • NBE Negative Marking Defense Simulation",
                "target_audience": "NEET-PG & INI-CET Aspirants",
                "total_registered": 2890,
                "difficulty": "all",
                "clinical_focus": "Core Clinical & Diagnostic Reasoning"
            }
        },
        {
            "id": "neet-pg-pro-clinical-quad",
            "title": "NEET-PG Pro Mini-Mock: Clinical Quad (Med + Surg + OBG + Peds)",
            "mode": "grand_test",
            "config": {
                "series_category": "neet_pg_pro",
                "test_type": "CLINICAL VIGNETTE",
                "question_count": 30,
                "time_limit_minutes": 40,
                "is_live": True,
                "badge": "BIG 4 CLINICAL",
                "syllabus_tag": "General Medicine, General Surgery, OBGYN & Pediatrics",
                "subject_ids": clinical_quad,
                "total_registered": 3840,
                "difficulty": "moderate",
                "clinical_focus": "The 4 Major Disciplines Accounting for 55%+ of NEET-PG Weightage"
            }
        },
        {
            "id": "neet-pg-pro-pre-para-foundations",
            "title": "NEET-PG Pro Pre & Para-Clinical Foundations Mock",
            "mode": "grand_test",
            "config": {
                "series_category": "neet_pg_pro",
                "test_type": "CONCEPTUAL INTEGRATION",
                "question_count": 30,
                "time_limit_minutes": 40,
                "is_live": True,
                "badge": "FOUNDATION 8",
                "syllabus_tag": "Anat, Physio, Biochem, Path, Micro, Pharma, FMT, PSM",
                "subject_ids": pre_para_block,
                "total_registered": 2980,
                "difficulty": "moderate",
                "clinical_focus": "Foundational Science Applied to Clinical Scenarios"
            }
        },
        {
            "id": "neet-pg-pro-emergency-critical-care",
            "title": "NEET-PG Pro Emergency & Critical Care Simulation",
            "mode": "grand_test",
            "config": {
                "series_category": "neet_pg_pro",
                "test_type": "TWO-STEP MANAGEMENT",
                "question_count": 25,
                "time_limit_minutes": 30,
                "is_live": True,
                "badge": "EMERGENCY ICU",
                "syllabus_tag": "Shock Resuscitation, Toxic Ingestion, Airway & Trauma Triage",
                "subject_ids": emergency_block,
                "total_registered": 2410,
                "difficulty": "hard",
                "clinical_focus": "Rapid-Response Acute Care & Pharmacological Antidotes"
            }
        },

        # =====================================================================
        # 2. NEET MEDICINE EXAMS PREP SERIES (Internal Medicine Specialty Rounds)
        # =====================================================================
        {
            "id": "med-prep-cardiology",
            "title": "NEET Medicine Clinical Rounds: Cardiology & Hemodynamics",
            "mode": "subject_test",
            "config": {
                "series_category": "medicine_prep",
                "test_type": "CLINICAL VIGNETTE",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "CARDIOLOGY",
                "syllabus_tag": "ACS Pathways, JVP Waves, Valvular Murmurs, Heart Failure & Arrhythmias",
                "subject_id": get_subj_id("General Medicine"),
                "total_registered": 3150,
                "difficulty": "moderate",
                "clinical_focus": "Harrison 21st Ed Cardiovascular Protocols"
            }
        },
        {
            "id": "med-prep-neurology",
            "title": "NEET Medicine Clinical Rounds: Neurology & Localizing Syndromes",
            "mode": "subject_test",
            "config": {
                "series_category": "medicine_prep",
                "test_type": "TWO-STEP MANAGEMENT",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "NEUROLOGY",
                "syllabus_tag": "Acute Stroke Windows, Cavernous Sinus, Epilepsy & Spinal Cord Syndromes",
                "subject_ids": neuro_block,
                "total_registered": 2890,
                "difficulty": "hard",
                "clinical_focus": "Neurovascular & Neuro-Anatomical Localization"
            }
        },
        {
            "id": "med-prep-nephrology",
            "title": "NEET Medicine Clinical Rounds: Nephrology & Acid-Base Disorders",
            "mode": "subject_test",
            "config": {
                "series_category": "medicine_prep",
                "test_type": "CLINICAL VIGNETTE",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "NEPHROLOGY",
                "syllabus_tag": "KDIGO AKI, Muddy Casts vs Hyaline, Lupus Nephritis & Hyperaldosteronism",
                "subject_ids": nephro_block,
                "total_registered": 2640,
                "difficulty": "hard",
                "clinical_focus": "Renal Biopsy Correlation & Electrolyte Balance"
            }
        },
        {
            "id": "med-prep-endocrinology",
            "title": "NEET Medicine Clinical Rounds: Endocrinology & Diabetology",
            "mode": "subject_test",
            "config": {
                "series_category": "medicine_prep",
                "test_type": "TWO-STEP MANAGEMENT",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "ENDOCRINOLOGY",
                "syllabus_tag": "SGLT-2i & GLP-1 RA, Euglycemic DKA, Thyroid Storm & Adrenal Crises",
                "subject_ids": endo_block,
                "total_registered": 2520,
                "difficulty": "moderate",
                "clinical_focus": "ADA 2024/2026 Guidelines & Endocrine Pharmacology"
            }
        },
        {
            "id": "med-prep-pulm-infectious",
            "title": "NEET Medicine Clinical Rounds: Pulmonology & Infectious Diseases",
            "mode": "subject_test",
            "config": {
                "series_category": "medicine_prep",
                "test_type": "CLINICAL VIGNETTE",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "INFECTIOUS & PULM",
                "syllabus_tag": "Sepsis-3 Guidelines, HRCT Tree-in-Bud, HIV Prophylaxis & Resistant Superbugs",
                "subject_ids": pulm_infectious,
                "total_registered": 2770,
                "difficulty": "moderate",
                "clinical_focus": "Antimicrobial Stewardship & Critical Respiratory Care"
            }
        },

        # =====================================================================
        # 3. INI-CET SUPER SPECIALTY SERIES (AIIMS / PGI / JIPMER Pattern)
        # =====================================================================
        {
            "id": "inicet-apex-mock-01",
            "title": "INI-CET Apex Mock: Two-Step Clinical Diagnostic Challenge",
            "mode": "grand_test",
            "config": {
                "series_category": "inicet",
                "test_type": "AIIMS APEX",
                "question_count": 30,
                "time_limit_minutes": 40,
                "is_live": True,
                "badge": "AIIMS ELITE",
                "syllabus_tag": "Complex High-Difficulty Clinical Vignettes with Rigorous Distractors",
                "total_registered": 4120,
                "difficulty": "hard",
                "clinical_focus": "AIIMS New Delhi & PGI Chandigarh Pattern Benchmarks"
            }
        },
        {
            "id": "inicet-molecular-oncology",
            "title": "INI-CET Molecular Oncology & Histopathology Masterclass",
            "mode": "grand_test",
            "config": {
                "series_category": "inicet",
                "test_type": "TWO-STEP MANAGEMENT",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "MOLECULAR ONCO",
                "syllabus_tag": "PML-RARA Translocations, IHC Profiling & Targeted Biologicals",
                "subject_ids": [get_subj_id("Pathology"), get_subj_id("Pharmacology"), get_subj_id("General Surgery")],
                "total_registered": 3310,
                "difficulty": "hard",
                "clinical_focus": "Genetics, Cytogenetics & Cancer Therapeutics"
            }
        },
        {
            "id": "inicet-toxic-critical",
            "title": "INI-CET Advanced Clinical Pharmacology & Toxic Emergencies",
            "mode": "grand_test",
            "config": {
                "series_category": "inicet",
                "test_type": "TWO-STEP MANAGEMENT",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "TOX & PHARMA",
                "syllabus_tag": "Idarucizumab/Andexanet Reversals, VRE Resistance & Nerve Aging",
                "subject_ids": pharma_toxic,
                "total_registered": 2860,
                "difficulty": "hard",
                "clinical_focus": "Advanced Receptor Pharmacology & Poisoning Antidotes"
            }
        },

        # =====================================================================
        # 4. FMGE / NEXT CLINICAL VIGNETTE SERIES
        # =====================================================================
        {
            "id": "next-clinical-vignette-mock",
            "title": "NExT Pattern Clinical Vignette Diagnostic Mock",
            "mode": "grand_test",
            "config": {
                "series_category": "fmge_next",
                "test_type": "NEXT PATTERN",
                "question_count": 30,
                "time_limit_minutes": 40,
                "is_live": True,
                "badge": "NEXT CLINICAL",
                "syllabus_tag": "Outpatient Case Presentations, Primary Care & Stepwise Management",
                "total_registered": 3650,
                "difficulty": "moderate",
                "clinical_focus": "National Exit Test (NExT) Problem-Solving Standard"
            }
        },
        {
            "id": "fmge-screening-booster",
            "title": "FMGE / NExT High-Frequency Screening Simulator",
            "mode": "grand_test",
            "config": {
                "series_category": "fmge_next",
                "test_type": "CLINICAL VIGNETTE",
                "question_count": 25,
                "time_limit_minutes": 30,
                "badge": "FMGE BOOSTER",
                "syllabus_tag": "High-Yield Screening Concepts: PSM, OBGYN, Pediatrics & Derm",
                "subject_ids": screening_block,
                "total_registered": 3220,
                "difficulty": "moderate",
                "clinical_focus": "MCI / FMGE Screening Exam High-Recurrence Concepts"
            }
        },

        # =====================================================================
        # 5. HIGH-YIELD IMAGE-BASED QUESTION (IBQ) SERIES
        # =====================================================================
        {
            "id": "ibq-radiology-spotter",
            "title": "Radiodiagnosis & Imaging Spotter Test (IBQ)",
            "mode": "subject_test",
            "config": {
                "series_category": "image_based",
                "test_type": "IMAGE-BASED SPOTTER",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "RAD SPOTTER",
                "syllabus_tag": "CT Brain Bleeds, FAST Ultrasound Windows, Coffee-Bean & HRCT Signs",
                "subject_id": get_subj_id("Radiodiagnosis"),
                "total_registered": 4210,
                "difficulty": "moderate",
                "clinical_focus": "Visual Radiographic & Sonographic Diagnostics"
            }
        },
        {
            "id": "ibq-derm-histopath-spotter",
            "title": "Dermatology & Histopathology Spotter Test (IBQ)",
            "mode": "subject_test",
            "config": {
                "series_category": "image_based",
                "test_type": "IMAGE-BASED SPOTTER",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "DERM SPOTTER",
                "syllabus_tag": "Auspitz Phenomenon, Flaccid/Tense Blister DIF, Leprosy & Scabies Sign",
                "subject_ids": derm_path,
                "total_registered": 3890,
                "difficulty": "moderate",
                "clinical_focus": "Clinical Morphology & Direct Immunofluorescence Patterns"
            }
        },
        {
            "id": "ibq-cardiovascular-ecg-spotter",
            "title": "Cardiovascular & ECG Rhythm Diagnostic Spotter (IBQ)",
            "mode": "subject_test",
            "config": {
                "series_category": "image_based",
                "test_type": "IMAGE-BASED SPOTTER",
                "question_count": 15,
                "time_limit_minutes": 20,
                "badge": "ECG SPOTTER",
                "syllabus_tag": "Cannon A-Waves, Complete Heart Block, 3-Hz Spike Discharges & MI Tracings",
                "subject_ids": cardio_rhythm,
                "total_registered": 3450,
                "difficulty": "moderate",
                "clinical_focus": "Electrophysiological & Hemodynamic Tracing Diagnostics"
            }
        },

        # =====================================================================
        # 6. RAPID PRACTICE DRILLS
        # =====================================================================
        {
            "id": "drill-daily-clinical-10",
            "title": "Daily Clinical Quick Test (10 Questions)",
            "mode": "quick_test",
            "config": {
                "series_category": "quick_drills",
                "test_type": "RAPID SPRINT",
                "question_count": 10,
                "time_limit_minutes": 12,
                "badge": "DAILY 10",
                "syllabus_tag": "Daily 10-MCQ Rapid Sprint with Instant Tutor Explanations",
                "total_registered": 9800,
                "difficulty": "moderate"
            }
        },
        {
            "id": "drill-5min-spaced-revision",
            "title": "5-Minute High-Yield Spaced Revision",
            "mode": "five_minute_revision",
            "config": {
                "series_category": "quick_drills",
                "test_type": "SM-2 REVISION",
                "question_count": 5,
                "time_limit_minutes": 5,
                "badge": "SM-2 DRILL",
                "syllabus_tag": "Due Spaced Repetition + Overconfidence Danger Zone Items",
                "total_registered": 7600,
                "difficulty": "all"
            }
        },
        {
            "id": "drill-pyq-recurring-patterns",
            "title": "NEET-PG PYQ Recurring Pattern Test",
            "mode": "pyq_pattern_test",
            "config": {
                "series_category": "quick_drills",
                "test_type": "PYQ PATTERN",
                "question_count": 20,
                "time_limit_minutes": 25,
                "badge": "PYQ RECALL",
                "syllabus_tag": "Multi-Year High-Yield Recalls & Core Repeating Concepts",
                "total_registered": 5200,
                "difficulty": "all"
            }
        }
    ]

    # Clean existing non-SWT templates to avoid duplicates
    print("\n--- Seeding Specialized Test Series Templates ---")
    c.execute("DELETE FROM test_templates WHERE id NOT LIKE 'swt-%'")
    
    seeded_count = 0
    for t in SERIES_TEMPLATES:
        t_id = t["id"]
        title = t["title"]
        mode = t["mode"]
        cfg_json = json.dumps(t["config"])

        # Check if exists
        c.execute("INSERT OR REPLACE INTO test_templates (id, title, mode, config, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                  (t_id, title, mode, cfg_json))
        seeded_count += 1
        print(f"  + Seeded: [{t['config'].get('series_category').upper()}] {title}")

    # Ensure all 19 Subject-Wise Tests exist in test_templates
    print("\n--- Verifying 19 Subject-Wise Test Templates ---")
    c.execute("SELECT id, name, code FROM subjects ORDER BY order_index")
    subjects = c.execute("SELECT id, name, code FROM subjects ORDER BY name").fetchall()
    swt_count = 0
    for sid, sname, scode in subjects:
        swt_id = f"swt-{sid}"
        cfg = {
            "series_category": "subject_wise",
            "test_type": "SUBJECT MASTERY",
            "question_count": 20,
            "time_limit_minutes": 25,
            "subject_id": sid,
            "subject_name": sname,
            "subject_code": scode,
            "badge": f"{scode} CORE",
            "syllabus_tag": f"Comprehensive {sname} Core Clinical Practice (20 MCQs)",
            "target_audience": f"{sname} Revision",
            "total_registered": 1450,
            "difficulty": "all"
        }
        c.execute("""
            INSERT OR REPLACE INTO test_templates (id, title, mode, config, created_at)
            VALUES (?, ?, 'subject_test', ?, CURRENT_TIMESTAMP)
        """, (swt_id, f"{sname} Subject-Wise Test (SWT)", json.dumps(cfg)))
        swt_count += 1

    conn.commit()
    print(f"\nSuccessfully seeded {seeded_count} specialized test series templates + {swt_count} Subject-Wise Tests.")

    # Audit count by category
    all_t = c.execute("SELECT config FROM test_templates").fetchall()
    categories = {}
    for row in all_t:
        cfg = json.loads(row[0]) if row[0] else {}
        cat = cfg.get("series_category", "other")
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n--- Test Series Distribution in DB ---")
    for cat, count in categories.items():
        print(f"  {cat:20s}: {count:2d} test templates")

    conn.close()

if __name__ == "__main__":
    seed_test_series()
