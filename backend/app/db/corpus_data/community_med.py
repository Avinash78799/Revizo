"""
Authentic High-Yield NEET-PG Clinical Questions for Community Medicine (PSM)
References: Park's Textbook of Preventive and Social Medicine (26th Ed)
"""

COMMUNITY_MED_QUESTIONS = [
    {
        "concept_name": "Core Principles: Cohort vs Case-Control Studies & Odds Ratio",
        "stem": (
            "An epidemiological investigation is launched to assess the association between maternal exposure to a rare agricultural herbicide "
            "during the first trimester of pregnancy and the subsequent occurrence of congenital microtia (an extremely rare ear deformity, incidence 1 in 10,000 births). "
            "Which of the following observational epidemiological study designs is the most efficient, cost-effective, and methodologically appropriate "
            "to investigate the etiology of this RARE DISEASE, and what is its primary measure of association?"
        ),
        "options": [
            ("Case-Control Study; Odds Ratio (OR)", True, None),
            ("Prospective Cohort Study; Relative Risk (RR)", False, "A cohort study for a rare disease (1 in 10,000) would require following hundreds of thousands of pregnant women for years, proving prohibitively expensive, inefficient, and impractical."),
            ("Cross-Sectional Prevalence Study; Prevalence Ratio", False, "Cross-sectional studies cannot determine temporal sequence or incidence of rare congenital anomalies."),
            ("Randomized Controlled Trial; Absolute Risk Reduction (ARR)", False, "Exposing pregnant women to a potentially teratogenic herbicide in an RCT is grossly unethical.")
        ],
        "pearl": "Case-Control vs Cohort Study Designs: 1. CASE-CONTROL STUDY: Starts with DISEASE (Cases with disease vs Controls without disease) -> looks BACKWARD in time for EXPOSURE (Retrospective). BEST FOR RARE DISEASES. Measures: ODDS RATIO (OR). Prone to: Recall Bias and Selection Bias. 2. COHORT STUDY: Starts with EXPOSURE (Exposed cohort vs Unexposed cohort) -> looks FORWARD in time for DISEASE incidence (Prospective/Retrospective). BEST FOR RARE EXPOSURES. Measures: RELATIVE RISK (Risk Ratio, RR) and Incidence Rate. Prone to: Loss to Follow-up (Attrition Bias).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 3 (Epidemiology), p. 64-82.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Cohort vs Case-Control Studies & Odds Ratio",
        "stem": (
            "In a prospective cohort study of 1,000 heavy cigarette smokers and 1,000 non-smokers followed for 10 years, "
            "80 smokers and 10 non-smokers develop coronary artery disease. "
            "Incidence of disease in exposed (Ie) is 80/1000 = 0.08 (8%), and incidence in non-exposed (Io) is 10/1000 = 0.01 (1%). "
            "What is the Relative Risk (Risk Ratio) and the Attributable Risk Percent (Etiologic Fraction) of coronary disease due to smoking in this cohort?"
        ),
        "options": [
            ("Relative Risk = 8.0; Attributable Risk Percent = 87.5%", True, None),
            ("Relative Risk = 0.8; Attributable Risk Percent = 12.5%", False, "Relative risk is Ie / Io = 80/10 = 8.0, not 0.8."),
            ("Relative Risk = 80; Attributable Risk Percent = 99%", False, "Incorrect calculation."),
            ("Relative Risk = 1.8; Attributable Risk Percent = 50%", False, "Incorrect calculation.")
        ],
        "pearl": "Epidemiological Risk Formulas: 1. RELATIVE RISK (RR) = Incidence in exposed (Ie) / Incidence in unexposed (Io) = 80/10 = 8.0. (Smokers have an 8-fold higher risk of CAD compared to non-smokers; measures strength of association!). 2. ATTRIBUTABLE RISK (AR / Risk Difference) = Ie - Io = 0.08 - 0.01 = 0.07 (7%). 3. ATTRIBUTABLE RISK PERCENT (Etiologic Fraction) = [(Ie - Io) / Ie] x 100 = [(0.08 - 0.01) / 0.08] x 100 = 87.5%! (Indicates that 87.5% of CAD in smokers is attributable directly to smoking and could be eliminated if smoking ceased).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 3, p. 76-80.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Sensitivity, Specificity & Predictive Value",
        "stem": (
            "A new rapid antigen screening test for early detection of cervical dysplasia is evaluated in 10,000 women. "
            "Gold standard colposcopic biopsy confirms disease in 1,000 women (true prevalence 10%). "
            "The rapid screening test correctly identifies 900 of the 1,000 diseased women as positive (True Positives = 900), "
            "and correctly identifies 8,100 of the 9,000 healthy women as negative (True Negatives = 8,100). "
            "What is the Sensitivity and Positive Predictive Value (PPV) of this screening test?"
        ),
        "options": [
            ("Sensitivity = 90%; Positive Predictive Value (PPV) = 50%", True, None),
            ("Sensitivity = 90%; Positive Predictive Value (PPV) = 90%", False, "PPV depends on disease prevalence; here PPV = TP / (TP + FP) = 900 / (900 + 900) = 50%."),
            ("Sensitivity = 50%; Positive Predictive Value (PPV) = 90%", False, "Sensitivity = TP / (TP + FN) = 900 / 1000 = 90%."),
            ("Sensitivity = 81%; Positive Predictive Value (PPV) = 81%", False, "81% is specificity (8100/9000 = 90%).")
        ],
        "pearl": "Screening Metrics Calculation: 1. SENSITIVITY = TP / (TP + FN) = 900 / (900 + 100) = 90%. (Ability of a test to correctly identify those with disease; SnNOut: High sensitivity rules OUT disease when negative). 2. SPECIFICITY = TN / (TN + FP) = 8100 / (8100 + 900) = 90%. (SpPIn: High specificity rules IN disease when positive). 3. POSITIVE PREDICTIVE VALUE (PPV) = TP / Total Test Positives = TP / (TP + FP) = 900 / (900 + 900) = 900 / 1800 = 50%! GOLDEN RULE: PPV is directly dependent on PREVALENCE: as disease prevalence falls, PPV falls dramatically and False Positives increase!",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 4 (Screening for Disease), p. 138-150.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Sensitivity, Specificity & Predictive Value",
        "stem": (
            "In a clinical laboratory, the cutoff value for a diagnostic biomarker is shifted to the LEFT on the receiver operating characteristic (ROC) curve, "
            "thereby capturing more true cases of disease. How does shifting the cutoff to maximize SENSITIVITY affect the SPECIFICITY "
            "and False Positive rate of the screening test?"
        ),
        "options": [
            ("Increases Sensitivity, but Decreases Specificity (increases False Positives)", True, None),
            ("Increases both Sensitivity and Specificity simultaneously", False, "Sensitivity and specificity are inversely related when shifting a single cutoff point on an ROC curve."),
            ("Increases Specificity, but Decreases Sensitivity", False, "Shifting the cutoff to capture more diseased cases increases sensitivity, not specificity."),
            ("Has zero effect on Specificity or False Positives", False, "A lower threshold inevitably misclassifies more healthy individuals as false positives.")
        ],
        "pearl": "Cutoff Threshold Shifts in Screening Tests: Moving threshold to INCREASE SENSITIVITY (Screening mode, e.g. blood bank screening for HIV): Captures all true positives, minimizes False Negatives, but INCREASES FALSE POSITIVES and DECREASES SPECIFICITY. Moving threshold to INCREASE SPECIFICITY (Confirmatory mode, e.g. before aggressive chemotherapy): Minimizes False Positives, rules in disease, but DECREASES SENSITIVITY and increases False Negatives.",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 4, p. 144-148.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Levels of Prevention (Primordial to Tertiary)",
        "stem": (
            "A national health education campaign is launched in primary schools to teach children healthy dietary habits, regular physical sports, "
            "and avoidance of smoking and junk food, with the explicit goal of PREVENTING THE EMERGENCE OF RISK FACTORS for coronary artery disease "
            "and adult-onset obesity in future generations. According to the epidemiological levels of prevention, what level of prevention does this represent?"
        ),
        "options": [
            ("Primordial Prevention", True, None),
            ("Primary Prevention", False, "Primary prevention acts in the pre-pathogenesis phase when risk factors ALREADY EXIST (e.g. wearing condoms, immunization, helmet use)."),
            ("Secondary Prevention", False, "Secondary prevention involves early diagnosis and prompt treatment in the early pathogenesis phase (e.g. Pap smear, screening mammography, treating early hypertension)."),
            ("Tertiary Prevention", False, "Tertiary prevention involves disability limitation and rehabilitation in late disease (e.g. physiotherapy after stroke).")
        ],
        "pearl": "Levels of Prevention Master Framework: 1. PRIMORDIAL: Prevention of the EMERGENCE OR DEVELOPMENT OF RISK FACTORS in populations where they have not yet appeared (e.g., teaching healthy lifestyles to children before smoking/junk food habits develop). Mode: Individual & Mass health education. 2. PRIMARY: Prevention before onset of disease when RISK FACTORS ARE ALREADY PRESENT. Modes: Health Promotion (sanitation, nutrition) & Specific Protection (Vaccines/Immunization, Chemoprophylaxis, Helmets/Seatbelts). 3. SECONDARY: Early diagnosis and prompt treatment (HALTS DISEASE PROGRESSION; Screening tests: Pap smear, sputum microscopy for TB, breast self-exam). 4. TERTIARY: Disability limitation & Rehabilitation (Physiotherapy, prosthesis, occupational therapy).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 2 (Concept of Health and Disease), p. 44-52.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Levels of Prevention (Primordial to Tertiary)",
        "stem": (
            "A 50-year-old female undergoes a routine community screening Mammography that detects an asymptomatic, impalpable 6 mm microcalcification cluster "
            "in her left breast. Stereotactic core needle biopsy reveals localized Stage I invasive ductal carcinoma. "
            "She undergoes successful breast-conserving surgery followed by curative local radiation. "
            "What level of prevention is exemplified by screening mammography?"
        ),
        "options": [
            ("Secondary Prevention (Early Diagnosis and Prompt Treatment)", True, None),
            ("Primary Prevention (Specific Protection)", False, "Primary prevention prevents disease occurrence; mammography detects existing disease at an early curable stage."),
            ("Primordial Prevention", False, "Primordial prevention stops risk factor emergence."),
            ("Tertiary Prevention (Disability Limitation)", False, "Tertiary prevention is rehabilitation after established disability.")
        ],
        "pearl": "Screening is ALWAYS Secondary Prevention: The golden rule in PSM exams: ALL SCREENING TESTS (Mammography, Pap smear, Sputum examination for AFB in NTEP, Blood pressure screening camps, Fasting blood glucose screening, Stool occult blood test) represent SECONDARY PREVENTION because their explicit epidemiological objective is: EARLY DETECTION (DIAGNOSIS) AND PROMPT TREATMENT before irreversible tissue damage occurs!",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 2, p. 48-50.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Universal Immunization Programme (UIP) & Cold Chain",
        "stem": (
            "Under the Government of India's Universal Immunization Programme (UIP), vaccines are stored and transported "
            "within a strict temperature-controlled cold chain from manufacturer to the peripheral session site. "
            "What is the mandatory storage temperature range maintained in Ice-Lined Refrigerators (ILRs) at Primary Health Centres (PHCs), "
            "and which vaccines are stored in the deep freezer (-15°C to -25°C) at district vaccine stores?"
        ),
        "options": [
            ("+2°C to +8°C in ILR; Oral Polio Vaccine (bOPV) and Rotavirus vaccine in deep freezers (-15°C to -25°C)", True, None),
            ("-10°C to -20°C in ILR; Hepatitis B and Td vaccines in deep freezers", False, "Hepatitis B, Td, and Pentavalent vaccines are FREEZE-SENSITIVE and must NEVER be frozen! Freezing destroys their aluminum adjuvant."),
            ("+15°C to +25°C in ILR; BCG vaccine in deep freezer", False, "ILRs must maintain +2 to +8°C, not room temperature."),
            ("0°C to -5°C in ILR; All vaccines must be frozen solid", False, "Freezing damages all DTP, Td, HepB, and Pentavalent vaccines.")
        ],
        "pearl": "Universal Immunization Programme (UIP) Cold Chain: Storage Temperature at PHC: +2°C to +8°C (maintained in Ice-Lined Refrigerators / ILRs). Most Heat-Sensitive Vaccine: Oral Polio Vaccine (OPV) (stored at -20°C at district level; top shelf in ILR). Most Freeze-Sensitive Vaccine: Hepatitis B, Td, DPT, Pentavalent (stored at bottom of ILR; NEVER FREEZE! Shake Test confirms if freeze-sensitive vaccine was damaged by freezing). Equipment: ILR (holds vaccines at +2 to +8°C) | Deep Freezer (prepares ice packs at -15 to -25°C) | Cold Box & Vaccine Carriers (transport with 4 conditioned ice packs).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 5 (Immunization & Cold Chain), p. 182-198.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Universal Immunization Programme (UIP) & Cold Chain",
        "stem": (
            "A community health officer is inspecting a vial of bivalent Oral Polio Vaccine (bOPV) at an immunization booth. "
            "The vaccine vial is equipped with a Vaccine Vial Monitor (VVM). "
            "On inspection, the inner square of the VVM is distinctly LIGHTER in color than the outer purple reference ring. "
            "According to the WHO / UIP guidelines on VVM stages, how should this vaccine vial be managed?"
        ),
        "options": [
            ("Stage 1 or 2: The vaccine has not reached its heat exposure discard point and CAN BE SAFELY ADMINISTERED to children (provided expiry date has not passed)", True, None),
            ("Stage 3: Discard immediately because the inner square matches the outer ring", False, "Discard point is reached when inner square matches or is darker than outer circle (Stage 3 and 4)."),
            ("Stage 4: Boil the vial for 10 minutes before administration", False, "Boiling destroys vaccines; damaged vials are discarded, never boiled."),
            ("Return the vial to the manufacturer for re-titration", False, "Peripheral staff discard unusable vials following biomedical waste guidelines.")
        ],
        "pearl": "Vaccine Vial Monitor (VVM) Stages: Stage 1: Inner square is lighter than outer circle (USE vaccine). Stage 2: Inner square is still lighter than outer circle, but darker than Stage 1 (USE vaccine first!). Stage 3 (DISCARD POINT): Inner square MATCHES the color of the outer circle (DO NOT USE! DISCARD!). Stage 4: Inner square is DARKER than the outer circle (DO NOT USE! DISCARD!). Rule of thumb: If the inner square is lighter, use it; if the inner square matches or is darker, discard it!",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 5, p. 192-196.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: National Tuberculosis Elimination Program (NTEP)",
        "stem": (
            "Under the National Tuberculosis Elimination Program (NTEP) in India, what is the approved, frontline, "
            "rapid molecular cartridge-based nucleic acid amplification test (CBNAAT) used for upfront universal drug-susceptibility testing "
            "that simultaneously detects Mycobacterium tuberculosis and resistance to Rifampicin within 2 hours?"
        ),
        "options": [
            ("GeneXpert MTB/RIF assay (detects rpoB gene mutations conferring Rifampicin resistance)", True, None),
            ("Line Probe Assay (LPA) for KatG gene alone", False, "Line probe assay takes 48-72 hours and requires specialized biosafety level equipment, whereas GeneXpert is the point-of-care CBNAAT."),
            ("Mantoux tuberculin skin test (PPD)", False, "Mantoux test detects immunological sensitization, cannot detect active TB or drug resistance."),
            ("Liquid culture in Middlebrook 7H9 broth", False, "Liquid culture takes 1-3 weeks.")
        ],
        "pearl": "NTEP Diagnostic Algorithms: Upfront diagnostic test for all presumptive TB cases: CBNAAT (GeneXpert MTB/RIF) or Truenat. Simultaneously detects M. tuberculosis DNA and RIFAMPICIN RESISTANCE (rpoB gene mutation) within 2 hours. Rifampicin resistance serves as a surrogate marker for Multi-Drug Resistant TB (MDR-TB). MDR-TB Definition: Resistance to at least ISONIAZID and RIFAMPICIN simultaneously. XDR-TB (Pre-XDR): MDR-TB + resistance to any Fluoroquinolone (Levofloxacin/Moxifloxacin).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 6 (Epidemiology of Communicable Diseases), p. 210-228.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: National Tuberculosis Elimination Program (NTEP)",
        "stem": (
            "Under the revised NTEP guidelines, what is the daily fixed-dose combination (FDC) regimen "
            "and duration for a patient with newly diagnosed, microbiologically confirmed, drug-sensitive pulmonary tuberculosis?"
        ),
        "options": [
            ("2 months of daily HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol) Intensive Phase + 4 months of daily HRE (Isoniazid, Rifampicin, Ethambutol) Continuation Phase", True, None),
            ("6 months of daily Rifampicin and Isoniazid without Pyrazinamide", False, "Pyrazinamide is mandatory in the 2-month intensive phase for its unique sterilizing activity against dormant bacilli."),
            ("2 months of alternate-day HRZ + 4 months of HR", False, "Intermittent (alternate-day / thrice-weekly) therapy has been completely ABOLISHED by NTEP in favor of DAILY FDCs."),
            ("9 months of Streptomycin and Isoniazid", False, "Streptomycin is an injectable no longer used in standard first-line DS-TB regimens.")
        ],
        "pearl": "NTEP Drug-Sensitive TB (DS-TB) Regimen: Daily Fixed-Dose Combinations (FDCs) based on weight bands: Intensive Phase (IP): 2 MONTHS of daily HRZE (Isoniazid, Rifampicin, Pyrazinamide, Ethambutol). Continuation Phase (CP): 4 MONTHS of daily HRE (Isoniazid, Rifampicin, Ethambutol). Total duration = 6 MONTHS. (Note: Ethambutol is continued in CP to prevent emergence of resistance if INH resistance is present). Nikshay Portal: Centralized digital notification and monitoring system. Nikshay Poshan Yojana: Rs. 500/month direct benefit transfer for nutritional support.",
        "citation": "NTEP National Strategic Plan / Park, 26th Ed, Chapter 6, p. 220-226.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Demography & Maternal Mortality Ratio (MMR)",
        "stem": (
            "In public health statistics, Maternal Mortality is a critical indicator of maternal healthcare delivery. "
            "How is the Maternal Mortality Ratio (MMR) mathematically defined and reported in national demographic surveys (SRS India)?"
        ),
        "options": [
            ("Number of maternal deaths due to obstetric causes per 100,000 live births in a given year", True, None),
            ("Number of maternal deaths per 1,000 live births in a given year", False, "Infant mortality is per 1,000; Maternal Mortality RATIO is expressed per 100,000 live births."),
            ("Number of maternal deaths per 100,000 women of reproductive age (15-49 years)", False, "This is the Maternal Mortality RATE, not Ratio."),
            ("Number of maternal deaths per 1,000 total pregnancies", False, "The denominator is live births, not total pregnancies.")
        ],
        "pearl": "Maternal Mortality Indices (Crucial Distinction): 1. MATERNAL MORTALITY RATIO (MMR): Number of maternal deaths due to obstetric causes during pregnancy, delivery, or within 42 days of termination / per 100,000 LIVE BIRTHS. Measures obstetric risk per pregnancy. 2. MATERNAL MORTALITY RATE: Number of maternal deaths per 100,000 WOMEN OF REPRODUCTIVE AGE (15-49 years). Measures fertility rate + obstetric risk. Leading causes of maternal mortality in India: 1. Postpartum Hemorrhage (PPH, ~38%) | 2. Sepsis | 3. Hypertensive disorders (Eclampsia) | 4. Unsafe Abortion.",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 10 (Demography and Family Planning), p. 520-532.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Demography & Maternal Mortality Ratio (MMR)",
        "stem": (
            "According to the established population norms in India under the National Health Mission (NHM), "
            "what is the recommended population covered by a Primary Health Centre (PHC) in plain areas versus hilly / tribal / difficult areas?"
        ),
        "options": [
            ("30,000 population in plain areas; 20,000 population in hilly/tribal areas", True, None),
            ("5,000 in plain areas; 3,000 in hilly/tribal areas", False, "5,000 (plain) and 3,000 (tribal) is the population norm for a SUB-CENTRE (now Ayushman Bharat Health & Wellness Centre)."),
            ("120,000 in plain areas; 80,000 in hilly/tribal areas", False, "120,000 (plain) and 80,000 (tribal) is the population norm for a COMMUNITY HEALTH CENTRE (CHC)."),
            ("50,000 in plain areas; 35,000 in hilly/tribal areas", False, "Incorrect population norms.")
        ],
        "pearl": "Indian Public Health Standards (IPHS) Population Norms: 1. SUB-CENTRE / Health & Wellness Centre (Arogya Mandir): 5,000 (Plain) | 3,000 (Hilly/Tribal). Manned by: 1 Female Health Worker (ANM) + 1 Male Health Worker (MPW) + Community Health Officer (CHO). 2. PRIMARY HEALTH CENTRE (PHC): 30,000 (Plain) | 20,000 (Hilly/Tribal). Has 4-6 indoor beds, 1 Medical Officer (MBBS). 3. COMMUNITY HEALTH CENTRE (CHC / First Referral Unit): 120,000 (Plain) | 80,000 (Hilly/Tribal). Has 30 beds, 4 Specialists (Surgeon, Physician, Gynecologist, Pediatrician), OT, X-ray, Labor room.",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 20 (Health Care of the Community), p. 940-955.",
        "difficulty": "easy"
    }
]
