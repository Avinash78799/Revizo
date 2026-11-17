"""
Authentic High-Yield NEET-PG Clinical Questions for General Medicine
References: Harrison's Principles of Internal Medicine (21st Ed)
"""

MEDICINE_QUESTIONS = [
    {
        "concept_name": "Core Principles: Acute Coronary Syndromes & Biomarkers",
        "stem": (
            "A 58-year-old male with long-standing hypertension and type 2 diabetes presents to the emergency casualty "
            "with severe, retrosternal, crushing chest pain radiating to his left shoulder and ulnar border of his left arm for the past 90 minutes. "
            "The pain is accompanied by nausea and cold diaphoresis, and was not relieved by sublingual nitroglycerin. "
            "His 12-lead ECG demonstrates 3 mm convex ST-segment elevation in leads V1, V2, V3, and V4, with reciprocal ST depression in leads II, III, and aVF. "
            "Which coronary artery is most likely acutely occluded, and what is the definitive reperfusion strategy of choice?"
        ),
        "options": [
            ("Left Anterior Descending Artery (LAD); Immediate Primary Percutaneous Coronary Intervention (PPCI) with door-to-balloon time <90 minutes", True, None),
            ("Right Coronary Artery (RCA); Immediate Intravenous Streptokinase infusion", False, "RCA occlusion produces Inferior wall MI (ST elevation in II, III, aVF), not anteroseptal MI."),
            ("Left Circumflex Artery (LCx); Oral Aspirin and Metoprolol alone without catheterization", False, "LCx occlusion causes lateral MI (ST elevation in I, aVL, V5, V6); medical therapy alone in STEMI is inappropriate."),
            ("Left Main Coronary Artery; Immediate surgical bypass without medical stabilization", False, "Emergent PPCI is the primary reperfusion modality for acute STEMI.")
        ],
        "pearl": "STEMI Localization & Coronary Anatomy: 1. Anteroseptal MI (V1-V4): Left Anterior Descending Artery (LAD) | 2. Inferior MI (II, III, aVF): Right Coronary Artery (RCA in 85-90% right-dominant circulation) | 3. Lateral MI (I, aVL, V5, V6): Left Circumflex Artery (LCx) or diagonal LAD | 4. Posterior MI (Tall R wave + ST depression in V1-V2): LCx or distal RCA (check V7-V9). Reperfusion Target: Primary PCI within 90 minutes of medical contact; if transfer time >120 min, IV Thrombolytic (Tenecteplase/Alteplase) within 30 minutes ('door-to-needle').",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 275 (STEMI), p. 2012-2028.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Acute Coronary Syndromes & Biomarkers",
        "stem": (
            "A 64-year-old male presents with acute substernal chest discomfort. High-sensitivity cardiac troponin I (hs-cTnI) "
            "is significantly elevated on admission and peaks at 18 hours. The patient is treated with coronary stenting. "
            "On the 5th postoperative day, he experiences a sudden recurrence of severe retrosternal chest pain. "
            "The cardiology fellow suspects acute recurrent myocardial infarction (reinfarction). "
            "Which cardiac biomarker is the most reliable and specific to detect acute REINFARCTION at day 5, "
            "because its levels return to baseline within 48 to 72 hours of an initial index event?"
        ),
        "options": [
            ("Creatine Kinase-MB (CK-MB)", True, None),
            ("Cardiac Troponin I (cTnI)", False, "Troponin I remains elevated in plasma for 7 to 10 days, making it difficult to detect early reinfarction at day 5."),
            ("Cardiac Troponin T (cTnT)", False, "Troponin T remains elevated for up to 10 to 14 days."),
            ("Lactate Dehydrogenase (LDH-1)", False, "LDH peaks at 3-6 days and remains elevated for 10-14 days; obsolete for acute triage.")
        ],
        "pearl": "Cardiac Biomarkers Kinetics: 1. Myoglobin: Rises in 1-2 hours, peaks at 6-8 hrs, returns to baseline in 24 hrs (earliest marker, but non-specific). 2. CK-MB: Rises in 4-6 hours, peaks at 18-24 hrs, RETURNS TO BASELINE IN 48-72 HOURS. BEST BIOMARKER FOR DETECTING EARLY REINFARCTION! 3. Cardiac Troponin (I and T): Rises in 3-4 hours, peaks at 24 hrs, REMAIN ELEVATED FOR 7-14 DAYS. Gold standard for initial acute MI diagnosis due to superior sensitivity and absolute myocardial specificity.",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 274 (NSTE-ACS), p. 2002-2010.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Heart Failure Guideline-Directed Therapy",
        "stem": (
            "A 62-year-old male with ischemic cardiomyopathy and chronic Heart Failure with Reduced Ejection Fraction (HFrEF, LVEF 28%) "
            "remains symptomatic with dyspnea on walking 100 meters (NYHA Class III) despite maximally tolerated doses of Ramipril (ACE inhibitor) "
            "and Carvedilol (beta-blocker). His serum potassium is 4.4 mEq/L and eGFR is 58 mL/min. "
            "According to the 2022 AHA/ACC/HFSA and ESC Heart Failure Guidelines, what is the single most effective medication modification "
            "to replace the ACE inhibitor and improve survival, and what mandatory washout period is required?"
        ),
        "options": [
            ("Switch Ramipril to an Angiotensin Receptor-Neprilysin Inhibitor (ARNI: Sacubitril/Valsartan) with a strict 36-hour washout period to prevent fatal angioedema", True, None),
            ("Add Digoxin 0.25 mg daily without stopping Ramipril", False, "Digoxin reduces hospitalizations but does NOT reduce all-cause mortality in HFrEF."),
            ("Switch to Amlodipine 10 mg daily", False, "Calcium channel blockers have zero mortality benefit in HFrEF and may worsen fluid retention."),
            ("Discontinue all neurohormonal blockers and maintain on high-dose loop diuretics alone", False, "Loop diuretics relieve congestive symptoms but do not improve survival; neurohormonal blockade is the foundation of GDMT.")
        ],
        "pearl": "HFrEF 4 Pillars of GDMT (Guideline-Directed Medical Therapy): 1. ARNI (Sacubitril/Valsartan preferred over ACEi/ARB; PARADIGM-HF showed 20% mortality reduction). MANDATORY 36-HOUR WASHOUT when switching from ACEi to ARNI to prevent life-threatening Angioedema! 2. Evidence-based Beta-blockers (Bisoprolol, Carvedilol, or Metoprolol Succinate). 3. Mineralocorticoid Receptor Antagonist (MRA: Spironolactone or Eplerenone). 4. SGLT2 Inhibitors (Dapagliflozin or Empagliflozin; DAPA-HF/EMPEROR-Reduced showed mortality benefit regardless of diabetes status).",
        "citation": "AHA/ACC/HFSA Heart Failure Guidelines 2022 / Harrison's, 21st Ed, Chapter 257 (Heart Failure), p. 1892-1910.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Valvular Heart Disease & Endocarditis",
        "stem": (
            "A 32-year-old intravenous drug user presents with high spiking fevers, chills, pleuritic chest pain, and cough productive of blood-tinged sputum. "
            "Physical examination reveals a soft pansystolic murmur at the lower left sternal border that characteristically increases in intensity "
            "during deep inspiration (Carvallo's sign). Transthoracic echocardiography demonstrates a 1.4 cm mobile, oscillating vegetation "
            "attached to the anterior leaflet of the tricuspid valve. What is the most common causative microbiological organism, "
            "and what do the pulmonary symptoms represent?"
        ),
        "options": [
            ("Staphylococcus aureus; Septic pulmonary emboli leading to wedge-shaped pulmonary infarctions / abscesses", True, None),
            ("Streptococcus viridans; Congestive left-sided pulmonary edema", False, "Strep viridans is typical of native subacute mitral/aortic endocarditis in non-IV drug users; S. aureus causes acute tricuspid endocarditis in IVDUs."),
            ("Enterococcus faecalis; Non-cardiogenic ARDS", False, "Enterococcus is associated with GU/GI manipulations in elderly patients."),
            ("Pseudomonas aeruginosa; Bilateral lobar pneumonia", False, "Pseudomonas occurs in IVDUs, but MSSA/MRSA is the overwhelmingly dominant causative organism (>60-70%).")
        ],
        "pearl": "Infective Endocarditis in IV Drug Users: Valve most commonly involved: TRICUSPID VALVE (Right-sided endocarditis). Causative organism: STAPHYLOCOCCUS AUREUS (>70%). Clinical features: Tricuspid regurgitation murmur that accentuates on INSPIRATION (Carvallo's Sign). Pulmonary complications: SEPTIC PULMONARY EMBOLISM (manifests as chest pain, hemoptysis, and multiple peripheral cavitating wedge-shaped lesions on chest CT). Contrast with native valve endocarditis (Mitral valve > Aortic valve, Strep viridans).",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 123 (Infective Endocarditis), p. 890-905.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Community-Acquired Pneumonia & CURB-65",
        "stem": (
            "A 72-year-old male presents with high fever, chills, pleuritic chest pain, and a productive cough with rust-colored sputum for 3 days. "
            "On physical examination, he is disoriented to time and place (Abbreviated Mental Test score 6/10). "
            "Vitals: respiratory rate 34 breaths/min, blood pressure 86/54 mmHg, pulse 110 bpm. "
            "Serum urea nitrogen (BUN) is 26 mg/dL (serum urea 9.2 mmol/L). Chest X-ray reveals right lower lobe consolidation with air bronchograms. "
            "According to the British Thoracic Society CURB-65 prognostic criteria, what is this patient's score and the recommended management setting?"
        ),
        "options": [
            ("CURB-65 score = 5; Urgent admission to Intensive Care Unit (ICU) for high-risk severe pneumonia", True, None),
            ("CURB-65 score = 1; Outpatient oral Amoxicillin therapy", False, "Score 1 is low risk; this patient has all 5 CURB-65 features positive (Confusion, Urea, RR, BP, Age)."),
            ("CURB-65 score = 2; Short stay hospital ward observation", False, "Score 2 represents moderate risk, but this patient scores 5, indicating high mortality."),
            ("CURB-65 score = 0; Home discharge with symptomatic antipyretics", False, "The patient has septic shock and severe respiratory compromise.")
        ],
        "pearl": "CURB-65 Score for Community-Acquired Pneumonia: 1 point for each: C: Confusion (AMT ≤8 or new disorientation) | U: Blood Urea Nitrogen >19 mg/dL (>7 mmol/L) | R: Respiratory rate ≥30 breaths/min | B: Blood pressure (SBP <90 mmHg or DBP ≤60 mmHg) | 65: Age ≥65 years. Stratification: 0-1: Low risk (30-day mortality <1.5%), Outpatient oral therapy. 2: Moderate risk (mortality 9%), Hospital ward admission. 3-5: High risk (mortality 15-40%), URGENT INPATIENT ADMISSION / ICU EVALUATION. Empiric ICU therapy: IV Beta-lactam (Ceftriaxone) + IV Macrolide (Azithromycin) or Respiratory Fluoroquinolone.",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 121 (Pneumonia), p. 870-884.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: COPD & Asthma Stepwise Management",
        "stem": (
            "A 64-year-old male with a 40 pack-year smoking history presents with progressive exertional dyspnea and chronic productive morning cough for 5 years. "
            "Spirometry reveals a post-bronchodilator FEV1/FVC ratio of 0.58 (normal >0.70) and post-bronchodilator FEV1 of 44% of predicted value, "
            "confirming severe persistent airflow limitation. Over the past 12 months, he has had 3 severe acute exacerbations requiring hospital admissions. "
            "Blood absolute eosinophil count is 380 cells/uL. According to the Global Initiative for Chronic Obstructive Lung Disease (GOLD 2023 update, Group E), "
            "what is the recommended maintenance inhaler pharmacotherapy?"
        ),
        "options": [
            ("Triple therapy combining Inhaled Corticosteroid (ICS) + Long-Acting Beta-Agonist (LABA) + Long-Acting Muscarinic Antagonist (LAMA)", True, None),
            ("Short-Acting Beta-Agonist (SABA) monotherapy on an as-needed basis only", False, "SABA monotherapy is inadequate for severe COPD with frequent exacerbations."),
            ("Long-term oral Prednisolone 40 mg daily", False, "Chronic maintenance oral steroids are not recommended in stable COPD due to steroid myopathy, osteoporosis, and opportunistic infections."),
            ("Inhaled Salbutamol plus Theophylline monotherapy", False, "Theophylline is obsolete as first-line maintenance due to narrow therapeutic index and lack of benefit compared to LAMA/LABA.")
        ],
        "pearl": "GOLD 2023 Guidelines Update (ABE Classification): Post-bronchodilator FEV1/FVC < 0.70 confirms fixed airflow obstruction. Groups: Group A (0-1 exacerbation, mMRC 0-1): Bronchodilator (LAMA or LABA). Group B (0-1 exacerbation, mMRC ≥2): LABA + LAMA combination. Group E (≥2 moderate exacerbations or ≥1 hospitalization): LABA + LAMA. ADD INHALED CORTICOSTEROID (Triple Therapy: ICS + LABA + LAMA) if Blood Eosinophils ≥ 300 cells/uL or history of asthma (significantly reduces exacerbation rate!).",
        "citation": "GOLD Executive Summary 2023 / Harrison's, 21st Ed, Chapter 286 (COPD), p. 2110-2125.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Diabetic Ketoacidosis & Hyperosmolar State",
        "stem": (
            "A 20-year-old female with Type 1 Diabetes Mellitus presents to the casualty with deep, rapid respirations (Kussmaul breathing), "
            "fruity acetone odor to her breath, abdominal pain, and recurrent vomiting after omitting her insulin injections for 2 days. "
            "Arterial blood gas (ABG) shows: pH 7.12, pCO2 20 mmHg, HCO3- 8 mEq/L. Plasma glucose is 480 mg/dL, serum sodium is 132 mEq/L, "
            "and serum potassium is 5.4 mEq/L. Urine ketones are strongly positive (4+). "
            "What is the single most critical immediate initial resuscitation intervention, and how should intravenous regular insulin and potassium be managed?"
        ),
        "options": [
            ("Immediate aggressive fluid resuscitation with 0.9% Normal Saline (1-1.5 L in the first hour), followed by low-dose IV Regular Insulin (0.1 U/kg/hr infusion); add Potassium to IV fluids once serum K+ falls below 5.2 mEq/L", True, None),
            ("Immediate intravenous bolus of 50 units of Regular Insulin before starting any IV fluids", False, "Insulin without fluid resuscitation worsens vascular collapse by driving fluid intracellularly with glucose!"),
            ("Immediate intravenous Sodium Bicarbonate rapid push", False, "Bicarbonate is indicated ONLY if arterial pH < 6.9; routine bicarbonate worsens intracellular acidosis and hypokalemia."),
            ("Immediate Subcutaneous Glargine injection and discharge home", False, "DKA is a life-threatening medical emergency requiring intensive inpatient IV insulin infusion.")
        ],
        "pearl": "Diabetic Ketoacidosis (DKA) Management Protocol: Triad: Hyperglycemia (>250 mg/dL) + High Anion Gap Metabolic Acidosis (pH <7.3, HCO3 <18) + Ketonemia (beta-hydroxybutyrate > acetoacetate). STEP 1: FLUID RESUSCITATION (Normal saline 1-1.5 L in 1st hour) is the most critical first step! STEP 2: IV REGULAR INSULIN (0.1 units/kg/hr continuous infusion). Target glucose fall: 50-70 mg/dL per hour. When glucose reaches 200-250 mg/dL, ADD 5% DEXTROSE to IV fluids to prevent hypoglycemia and cerebral edema while continuing insulin until ketoacidosis resolves (anion gap normalizes!). STEP 3: POTASSIUM: Even if serum K+ appears normal/high, total body potassium is severely depleted. Start IV KCl (20-30 mEq/L) as soon as serum K+ < 5.2 mEq/L and urine output is established. HOLD insulin if K+ < 3.3 mEq/L!",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 397 (Diabetes Mellitus), p. 2884-2900.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Acute Kidney Injury (KDIGO) & Dialysis Criteria",
        "stem": (
            "A 68-year-old male with severe septic shock from acute bacterial pyelonephritis has had anuria for the past 14 hours. "
            "Serum creatinine has spiked from a baseline of 1.0 mg/dL to 5.2 mg/dL. "
            "Laboratory investigations reveal: serum potassium 7.6 mEq/L, arterial pH 7.04, HCO3- 7 mEq/L. "
            "The ECG monitor reveals absent P waves, markedly widened QRS complexes, and tall, peaked, symmetrical T waves ('sine wave' pattern). "
            "What is the immediate, life-saving medication to membrane-stabilize the myocardium while preparing for emergent Hemodialysis?"
        ),
        "options": [
            ("Intravenous Calcium Gluconate (10 mL of 10% solution administered over 2 to 5 minutes)", True, None),
            ("Oral Sodium Polystyrene Sulfonate (Kayexalate) resin", False, "Kayexalate takes hours to days to lower potassium and has zero membrane-stabilizing effect during an acute cardiac emergency."),
            ("Subcutaneous Regular Insulin without Dextrose", False, "Insulin drives potassium intracellularly but takes 15-30 minutes and does NOT stabilize the cardiac membrane directly; causes severe hypoglycemia if given without dextrose!"),
            ("Immediate high-dose intravenous Spironolactone", False, "Spironolactone is a potassium-sparing diuretic that would worsen lethal hyperkalemia!")
        ],
        "pearl": "Hyperkalemia Emergency Management: ECG signs: Tall peaked T waves (earliest) -> PR prolongation -> Flattened P waves -> Widened QRS -> Sine-wave pattern -> Asystole/VF. STEP 1: MEMBRANE STABILIZATION (within 1-3 minutes): 10% CALCIUM GLUCONATE (10 mL IV over 2-5 min). Antagonizes hyperkalemic cardiotoxicity without changing serum K+ level. STEP 2: SHIFT K+ INTO CELLS (within 15-30 min): 10 units Regular Insulin + 50 mL 50% Dextrose IV, plus inhaled Salbutamol/Albuterol (10-20 mg nebulized), and IV Sodium Bicarbonate (if acidotic). STEP 3: ELIMINATE K+ FROM BODY: Furosemide, Patiromer, or EMERGENT HEMODIALYSIS. Indications for Emergency Dialysis (AEIOU): Acidosis (pH <7.1), Electrolytes (refractory K >6.5), Ingestion/Toxins, Overload (pulmonary edema), Uremia (pericarditis, encephalopathy).",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 304 (Acute Kidney Injury), p. 2235-2250.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Acute Stroke Syndromes & Reperfusion Windows",
        "stem": (
            "A 65-year-old right-handed female is brought to the emergency stroke unit by her daughter. "
            "One hour ago, while eating lunch, she suddenly dropped her fork, developed right facial weakness, right arm and leg paralysis, "
            "and was unable to speak or understand spoken commands (Global Aphasia). "
            "Non-contrast head CT rules out intracranial hemorrhage and shows early subtle loss of the left insular ribbon. "
            "Her blood pressure is 172/96 mmHg and blood glucose is 142 mg/dL. NIH Stroke Scale (NIHSS) is 18. "
            "What is the approved therapeutic time window for administering Intravenous Recombinant Tissue Plasminogen Activator (Alteplase / Tenecteplase) "
            "in acute ischemic stroke?"
        ),
        "options": [
            ("Within 4.5 hours of symptom onset (time of last known normal)", True, None),
            ("Within 12 hours of symptom onset", False, "IV thrombolysis beyond 4.5 hours carries high risk of fatal symptomatic intracranial hemorrhage without visual/functional recovery."),
            ("Within 24 hours in all stroke patients without neuroimaging", False, "IV tPA cannot be given at 24 hours; mechanical thrombectomy may be considered up to 24 hours in select large vessel occlusions."),
            ("Only within 60 minutes of symptom onset", False, "The window is up to 4.5 hours based on the ECASS-III trial.")
        ],
        "pearl": "Acute Ischemic Stroke Reperfusion Windows: 1. Intravenous Thrombolysis (Alteplase 0.9 mg/kg, max 90 mg; or Tenecteplase 0.25 mg/kg): Time window is strictly WITHIN 4.5 HOURS of last known well (ECASS-III criteria). Blood pressure MUST be lowered to <185/110 mmHg (using IV Labetalol or Nicardipine) before administering tPA. 2. Endovascular Mechanical Thrombectomy (EVT): Time window is WITHIN 6 HOURS for anterior circulation Large Vessel Occlusion (LVO) (can be extended up to 24 hours in selected patients with DAWN/DEFUSE-3 clinical-core mismatch).",
        "citation": "AHA/ASA Stroke Guidelines 2019 / Harrison's, 21st Ed, Chapter 420 (Ischemic Stroke), p. 3080-3098.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Acute Meningitis CSF Differentiation",
        "stem": (
            "A 21-year-old university student is brought to the casualty with high fever (103.6°F), severe throbbing headache, photophobia, "
            "vomiting, and progressive confusion for 18 hours. Physical examination reveals petechial purpuric lesions over his trunk and extremities, "
            "marked neck stiffness, and a positive Kernig's and Brudzinski's sign. Emergency lumbar puncture is performed after non-contrast CT. "
            "Which of the following CSF profiles is pathognomonic for Acute Pyogenic (Bacterial) Meningitis?"
        ),
        "options": [
            ("Markedly elevated opening pressure (>300 mm H2O), cloudy/turbid appearance, marked pleocytosis with >85% polymorphonuclear neutrophils (PMNs), markedly elevated protein (>150 mg/dL), and markedly reduced CSF-to-blood glucose ratio (<0.40)", True, None),
            ("Normal opening pressure, clear appearance, lymphocytic pleocytosis, normal protein, and normal CSF-to-blood glucose ratio (>0.60)", False, "Clear CSF with lymphocytes and normal glucose is characteristic of Acute Viral (Aseptic) Meningitis."),
            ("Moderately elevated pressure, clear/cobweb coagulum appearance, lymphocytic pleocytosis, very high protein (>300 mg/dL), and marked hypoglycorrhachia", False, "Cobweb coagulum with lymphocytes and high protein is typical of Tuberculous (TB) Meningitis."),
            ("Xanthochromic supernatant with uniform blood across 3 serial tubes and crenated RBCs", False, "Xanthochromia with uniform blood indicates Subarachnoid Hemorrhage (SAH), not acute bacterial meningitis.")
        ],
        "pearl": "CSF Profiles Comparison: 1. Acute Bacterial Meningitis: Turbid, PMN predominance (>1,000-10,000/uL), Protein markedly elevated (>100-500 mg/dL), Glucose SEVERELY REDUCED (CSF/plasma glucose <0.4). Gram stain positive. 2. Viral (Aseptic) Meningitis: Clear, Lymphocyte predominance, Protein normal or mildly elevated (<100 mg/dL), Glucose NORMAL (CSF/plasma >0.6). 3. Tuberculous Meningitis: Clear/Opalescent with Cobweb coagulum on standing (fibrin clot), Lymphocytic predominance, Protein VERY HIGH (>200-500 mg/dL), Glucose marked reduction (<0.3). Most common adult bacterial cause: Streptococcus pneumoniae, followed by Neisseria meningitidis.",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 133 (Meningitis), p. 982-998.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Cirrhosis, Ascites & Spontaneous Bacterial Peritonitis",
        "stem": (
            "A 54-year-old male with decompensated alcoholic cirrhosis and chronic ascites presents with low-grade fever, "
            "diffuse abdominal pain, and worsening confusion for 24 hours. Physical examination reveals shifting dullness, diffuse abdominal tenderness "
            "without rigid guarding, and flapping hand tremors (asterixis). Diagnostic paracentesis yields cloudy peritoneal fluid. "
            "Ascitic fluid analysis demonstrates: Total protein 1.1 g/dL, Serum Albumin 2.4 g/dL, Ascitic Albumin 0.6 g/dL (SAAG = 1.8 g/dL). "
            "Ascitic fluid Absolute Neutrophil Count (polymorphonuclear / PMN count) is 420 cells/uL. "
            "What is the diagnosis, and what is the definitive first-line empiric antibiotic of choice?"
        ),
        "options": [
            ("Spontaneous Bacterial Peritonitis (SBP); Intravenous Cefotaxime or Ceftriaxone (third-generation cephalosporin)", True, None),
            ("Secondary bacterial peritonitis from ruptured bowel; Intravenous Metronidazole monotherapy", False, "Secondary peritonitis has polymicrobial cultures, high protein (>1 g/dL), low glucose (<50), and high LDH, requiring laparotomy."),
            ("Tuberculous peritonitis; Four-drug anti-tubercular therapy (ATT)", False, "TB peritonitis has high protein (>2.5 g/dL), low SAAG (<1.1), and lymphocytic predominance."),
            ("Hepatorenal syndrome; Terlipressin and Albumin infusion without antibiotics", False, "Hepatorenal syndrome is functional renal failure in cirrhosis; PMN count >250/uL mandates immediate treatment for SBP.")
        ],
        "pearl": "Spontaneous Bacterial Peritonitis (SBP): Translocation of enteric bacteria (most common: E. coli, Klebsiella pneumoniae) across permeable edematous gut wall into ascitic fluid. DIAGNOSTIC CRITERION: Ascitic fluid Absolute Neutrophil Count (PMN count) ≥ 250 cells/uL (0.25 x 10^9/L). FIRST-LINE TREATMENT: IV Cefotaxime (2 g IV q8h) or Ceftriaxone (2 g IV q24h) for 5 days. INTRAVENOUS ALBUMIN (1.5 g/kg on day 1, 1.0 g/kg on day 3) reduces hepatorenal syndrome and mortality from 29% to 10%! Long-term secondary prophylaxis: Oral Norfloxacin (400 mg daily) or Ciprofloxacin.",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 337 (Cirrhosis and Its Complications), p. 2480-2495.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Cirrhosis, Ascites & Spontaneous Bacterial Peritonitis",
        "stem": (
            "In the diagnostic workup of a patient with new-onset ascites, peritoneal fluid paracentesis is performed. "
            "The Serum-Ascites Albumin Gradient (SAAG) is calculated by subtracting the ascitic albumin concentration from the serum albumin concentration "
            "(SAAG = Serum Albumin - Ascitic Albumin). Which of the following conditions characteristically produces a HIGH SAAG (≥1.1 g/dL) "
            "with a HIGH ascitic total protein (≥2.5 g/dL)?"
        ),
        "options": [
            ("Budd-Chiari Syndrome (Hepatic Venous Outflow Obstruction) or Congestive Heart Failure", True, None),
            ("Cirrhosis with uncomplicated portal hypertension", False, "Cirrhosis produces High SAAG (≥1.1) but LOW ascitic total protein (<2.5 g/dL) due to impaired hepatic synthetic function."),
            ("Peritoneal Carcinomatosis", False, "Peritoneal carcinomatosis produces Low SAAG (<1.1 g/dL) with high total protein."),
            ("Nephrotic Syndrome", False, "Nephrotic syndrome produces Low SAAG (<1.1 g/dL) and low total protein (<2.5 g/dL).")
        ],
        "pearl": "SAAG (Serum-Ascites Albumin Gradient) Classification: SAAG ≥ 1.1 g/dL (Portal Hypertension Present): 1. Low ascitic protein (<2.5 g/dL): Liver Cirrhosis (sinusoidal hypertension) | 2. High ascitic protein (≥2.5 g/dL): Cardiac Ascites / Congestive Heart Failure, Budd-Chiari syndrome (post-sinusoidal hypertension). SAAG < 1.1 g/dL (No Portal Hypertension): Peritoneal Carcinomatosis, Tuberculous Peritonitis, Pancreatic Ascites, Nephrotic Syndrome.",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 45 (Ascites), p. 320-326.",
        "difficulty": "hard"
    }
]
