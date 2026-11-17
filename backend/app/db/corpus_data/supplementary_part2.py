"""
Supplementary High-Yield NEET-PG Clinical Questions: Part 2
Covers: Psychiatry (6), General Surgery (6), General Medicine (4), Pharmacology (4).
"""

SUPPLEMENTARY_PART2 = [
    # =========================================================================
    # --- PSYCHIATRY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Psychiatry",
        "concept_name": "Bipolar Affective Disorder: Mania vs Hypomania & Mood Stabilizers",
        "stem": (
            "A 28-year-old software architect is brought to the outpatient clinic by his parents. For the past 10 days, he has slept only "
            "1 to 2 hours per night but feels intensely energetic and 'electrified'. He speaks at an unstoppable rapid cadence with abrupt "
            "shifts from one topic to another based on loose rhyming associations (clang associations and flight of ideas). "
            "He has maxed out his credit cards on impulsive speculative cryptocurrency investments and claims he has been chosen by the "
            "Ministry of Defense to launch an interplanetary defense grid. "
            "What is the formal DSM-5 diagnosis, and which mood stabilizer is recognized as the FIRST-LINE gold standard for acute mania and suicide prevention?"
        ),
        "options": [
            ("Bipolar I Disorder, Current Episode Manic with Psychotic Features; Lithium Carbonate", True, None),
            ("Bipolar II Disorder, Hypomanic Episode; Fluoxetine monotherapy", False, "Bipolar II requires hypomania (no psychosis, no marked social impairment) and major depression. Antidepressant monotherapy is contraindicated in bipolar mania as it precipitates rapid cycling."),
            ("Schizotypal Personality Disorder; Haloperidol depot injection", False, "This is an acute episodic mood state with grandiosity and sleep loss, not a chronic eccentric personality disorder."),
            ("Cyclothymic Disorder; Diazepam maintenance therapy", False, "Cyclothymia consists of at least 2 years of subthreshold hypomanic and depressive symptoms; full manic episodes with psychosis exclude it.")
        ],
        "pearl": "Bipolar Disorder Spectrum: 1. BIPOLAR I DISORDER: Requires at least ONE MANIC EPISODE in lifetime (depressive episodes common but not mandatory for diagnosis). Manic Episode DSM-5 Criteria: Abnormally elevated, expansive, or irritable mood + persistently increased activity/energy lasting &ge;1 week (or any duration if hospitalization required), with &ge;3 DIGFAST symptoms (Distractibility, Indiscretion/impulsive spending, Grandiosity, Flight of ideas, Activity increase, Sleep deficit [decreased need for sleep], Talkativeness/pressured speech). Psychosis (delusions/hallucinations) AUTOMATICALLY designates the episode as Mania (Bipolar I)! 2. BIPOLAR II: Hypomania (&ge;4 consecutive days, no psychosis, no hospitalization, no severe impairment) PLUS at least one Major Depressive Episode. 3. FIRST-LINE MOOD STABILIZER: LITHIUM CARBONATE. Reduces suicide risk by >80%! Therapeutic serum level: 0.8-1.2 mEq/L (acute mania); 0.6-0.8 mEq/L (maintenance). Toxicity occurs at >1.5 mEq/L (coarse tremors, ataxia, vomiting, seizures; hemodialysis indicated at >4.0 mEq/L or >2.5 with renal failure). Teratogenicity: Ebstein's anomaly (tricuspid valve downward displacement).",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 8 (Bipolar Disorders); Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Psychiatry",
        "concept_name": "Schizophrenia: Schneiderian First-Rank Symptoms & Dopamine Pathways",
        "stem": (
            "A 22-year-old engineering student is referred for psychiatric evaluation after failing his semester examinations and isolating "
            "himself in his hostel room for 7 months. He expresses an unshakeable conviction that the Central Intelligence Agency has implanted "
            "a microchip in his dental filling to extract his innermost thoughts and transmit them via the radio network (thought broadcast). "
            "He also hears two distinct male voices discussing his daily bathroom habits and mocking his gait in the third person. "
            "According to Kurt Schneider, these symptoms belong to which diagnostic category, and hyperdopaminergic activity in which cerebral pathway underlies their generation?"
        ),
        "options": [
            ("Schneider's First-Rank Symptoms (FRS); Mesolimbic Dopaminergic Pathway", True, None),
            ("Schneider's Second-Rank Symptoms; Tuberoinfundibular Dopaminergic Pathway", False, "Thought broadcast and third-person auditory hallucinations are classic First-Rank symptoms; the tuberoinfundibular pathway controls prolactin secretion."),
            ("Bleuler's Fundamental 4 A's; Nigrostriatal Dopaminergic Pathway", False, "Bleuler's 4 A's are Autism, Ambivalence, loose Associations, and inappropriate Affect. Nigrostriatal pathway mediates motor control/extrapyramidal symptoms."),
            ("Kraepelinian Affective Symptoms; Mesocortical Dopaminergic Pathway", False, "Kraepelin delineated dementia praecox from manic-depressive illness; mesocortical hypodopaminergia causes negative symptoms.")
        ],
        "pearl": "Schizophrenia Symptomatology & Dopamine Neuroanatomy: 1. SCHNEIDER'S FIRST-RANK SYMPTOMS (FRS): Kurt Schneider identified 11 symptoms of primary diagnostic significance: (A) Hallucinatory voices: Voices commenting on actions (running commentary), Voices arguing or discussing the patient in the 3rd person, Audible thoughts (Gedankenlautwerden / thought echo). (B) Thought interference: Thought insertion, Thought withdrawal, Thought broadcast. (C) Passivity / 'Made' phenomena: 'Made' affect, 'Made' impulses, 'Made' volitional acts, Somatic passivity. (D) Delusional perception (Wahnwahrnehmung: normal sensory percept interpreted with delusional significance). 2. DOPAMINE PATHWAYS IN SCHIZOPHRENIA: (A) Mesolimbic Pathway (VTA to nucleus accumbens): HYPERACTIVITY &rarr; POSITIVE SYMPTOMS (delusions, hallucinations) &mdash; blocked by D2 antagonists! (B) Mesocortical Pathway (VTA to prefrontal cortex): HYPOACTIVITY &rarr; NEGATIVE & COGNITIVE SYMPTOMS (apathy, avolition, alogia). (C) Nigrostriatal Pathway: D2 blockade &rarr; Extrapyramidal Symptoms (EPS: dystonia, parkinsonism, akathisia, tardive dyskinesia). (D) Tuberoinfundibular Pathway: D2 blockade &rarr; Hyperprolactinemia (galactorrhea, amenorrhea, gynecomastia).",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 5 (Schizophrenia Spectrum); Stahl's Essential Psychopharmacology, 5th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Psychiatry",
        "concept_name": "Obsessive-Compulsive Disorder (OCD): Neurocircuitry & First-Line Therapy",
        "stem": (
            "A 24-year-old laboratory technician spends 4 to 5 hours every evening repeatedly washing her hands with carbolic soap until "
            "her skin is raw, macerated, and bleeding. She acknowledges that her intense terror of microbial contamination from doorknobs is "
            "irrational, unreasonable, and originates entirely within her own mind (ego-dystonic), yet she experiences unbearable anxiety "
            "unless she executes exactly 12 cycles of washing. "
            "Dysregulation of which neural circuit underlies this disorder, and what constitutes the evidence-based FIRST-LINE pharmacotherapy?"
        ),
        "options": [
            ("Cortico-Striato-Thalamo-Cortical (CSTC) loop / Orbitofrontal cortex-caudate hyperactivity; High-dose Selective Serotonin Reuptake Inhibitor (SSRI) for at least 10-12 weeks", True, None),
            ("Nigrostriatal dopaminergic tract; Low-dose typical antipsychotic (Haloperidol 2 mg)", False, "Dopamine antagonists alone are not first-line for OCD; high-dose serotonergic therapy is required."),
            ("Locus coeruleus noradrenergic hyper-responsiveness; Oral Clonidine monotherapy", False, "Noradrenergic pathways mediate PTSD and opioid withdrawal, not the obsessive-compulsive CSTC loop."),
            ("Mesocortical reward pathway; Bupropion (NDRI) extended-release tablets", False, "Bupropion inhibits dopamine and norepinephrine reuptake; it has zero efficacy in OCD and lowers seizure threshold.")
        ],
        "pearl": "Obsessive-Compulsive Disorder (OCD): Neurobiology: Hyperactivity in the Cortico-Striato-Thalamo-Cortical (CSTC) loop (orbitofrontal cortex, anterior cingulate cortex, and head of the caudate nucleus). Core definitions: 1. Obsessions: Recurrent, intrusive, persistent unwanted thoughts, urges, or images that provoke marked anxiety. EGO-DYSTONIC (recognized as product of own mind, distinguishing from thought insertion in schizophrenia!). 2. Compulsions: Repetitive behavioral or mental acts driven by rigid rules to neutralize obsession-induced anxiety. FIRST-LINE TREATMENT: 1. Pharmacotherapy: High-dose SSRIs (Fluoxetine 60-80 mg, Sertraline 200 mg, Fluvoxamine 300 mg, Escitalopram 20-40 mg). Key trial note: OCD requires HIGHER DOSES and LONGER DURATION (10-12 weeks) of SSRI treatment compared to Major Depression! 2. Psychotherapy: Cognitive Behavioral Therapy (CBT) with Exposure and Response Prevention (ERP) is the gold standard psychological treatment. Refractory cases: Clomipramine (potent serotonergic TCA) or SSRI augmentation with Aripiprazole/Risperidone.",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 10 (OCD); Stahl's Essential Psychopharmacology, 5th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Psychiatry",
        "concept_name": "Organic Psychiatry: Delirium vs Dementia & Acute Agitation Management",
        "stem": (
            "An 78-year-old postoperative male on day 2 following total hip arthroplasty suddenly becomes acutely agitated, disoriented to time "
            "and place, and pulls out his Foley catheter and peripheral IV line at 2:00 AM. His mental status fluctuates wildly: he was lucid "
            "and calm during morning rounds yesterday, but now sees 'spiders crawling on the bedsheets' (visual illusions/hallucinations). "
            "His attention span is severely impaired, and sleep-wake cycle is reversed. Baseline cognitive function was normal prior to surgery. "
            "What is the diagnosis, and what is the preferred pharmacological agent if severe behavioral agitation threatens physical safety?"
        ),
        "options": [
            ("Delirium (Acute Encephalopathy); Low-dose Haloperidol (0.5 to 1 mg orally or parenterally)", True, None),
            ("Alzheimer's Dementia; High-dose Donepezil 23 mg daily", False, "Dementia is a chronic, insidious, progressive decline with clear sensorium until end-stage, not an acute fluctuating delirium."),
            ("Late-onset Schizophrenia; Olanzapine 20 mg intramuscularly", False, "Schizophrenia presents with auditory hallucinations and persecutory delusions in clear consciousness, not fluctuating orientation and visual illusions."),
            ("Hypoactive delirium; Intravenous Midazolam 5 mg bolus", False, "Benzodiazepines worsen delirium and prolong hospital stay; they are contraindicated in non-alcohol/sedative-induced delirium.")
        ],
        "pearl": "Delirium vs Dementia Master Comparison: 1. DELIRIUM (Acute Confusional State): Onset: ACUTE (hours to days). Course: FLUCTUATING (worse at night, 'sundowning'). Consciousness / Sensorium: CLOUDED / IMPAIRED. Attention: SEVERELY IMPAIRED (cannot sustain, shift, or focus attention). Hallucinations: VISUAL and tactile illusions/hallucinations common. EEG: Generalized diffuse background slowing (except in delirium tremens where fast activity occurs). Reversibility: HIGHLY REVERSIBLE once underlying trigger treated (infection/UTI, hypoxia, electrolyte imbalance, anticholinergic drugs). PHARMACOTHERAPY FOR SEVERE AGITATION: LOW-DOSE HALOPERIDOL (0.5-1.0 mg PO/IM) or atypical antipsychotics (Quetiapine, Risperidone). CRITICAL CONTRAINDICATION: NEVER give Benzodiazepines in delirium unless caused by ALCOHOL or SEDATIVE-HYPNOTIC WITHDRAWAL (benzodiazepines cause paradoxical worsening and delirium prolongation!).",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 14 (Neurocognitive Disorders); Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Psychiatry",
        "concept_name": "Substance Use: Alcohol Withdrawal Spectrum & Delirium Tremens",
        "stem": (
            "A 46-year-old chronic heavy alcoholic is admitted to the surgical ward with an ankle fracture. Exactly 72 hours after his last drink, "
            "he becomes severely disoriented, terrified, and drenched in sweat. Physical examination reveals coarse tremors of both hands, "
            "extreme diaphoresis, marked tachycardia (pulse 138 bpm), blood pressure 178/104 mmHg, and body temperature of 38.6°C (101.5°F). "
            "He points to the ceiling, screaming that giant black scorpions and snakes are crawling toward him (zoopsia). "
            "What life-threatening condition has developed, and what is the mandatory immediate treatment regimen?"
        ),
        "options": [
            ("Delirium Tremens (DT); Intravenous Benzodiazepines (e.g., Diazepam or Lorazepam) titrated to sedation, plus high-dose IV Thiamine prior to any glucose infusion", True, None),
            ("Alcoholic Hallucinosis; Oral Haloperidol 5 mg without benzodiazepines", False, "Alcoholic hallucinosis occurs earlier (12-24h), features auditory hallucinations, and has CLEAR sensorium and normal vital signs without autonomic storm."),
            ("Wernicke's Encephalopathy; IV 5% Dextrose infusion followed 4 hours later by oral thiamine", False, "Administering glucose BEFORE thiamine precipitates irreversible acute Wernicke encephalopathy and Korsakoff psychosis by exhausting thiamine stores!"),
            ("Serotonin Syndrome; Immediate administration of Cyproheptadine and Dantrolene", False, "This is alcohol withdrawal in a chronic drinker with sympathetic hyperactivity, not serotonergic drug toxicity.")
        ],
        "pearl": "Alcohol Withdrawal Timeline & Delirium Tremens: 1. Minor Withdrawal (6-12 hrs): Tremulousness ('the shakes'), insomnia, anxiety, mild tachycardia. 2. Alcoholic Hallucinosis (12-24 hrs): Auditory and visual hallucinations with PRESERVED / CLEAR SENSORIUM and stable vitals. 3. Withdrawal Seizures ('Rum Fits', 12-48 hrs): Generalized tonic-clonic seizures, brief, non-focal. 4. DELIRIUM TREMENS (DT, 48-96 hrs): Medical emergency! Mortality 5-15% if untreated. Features: Fluctuating delirium + Severe autonomic storm (marked tachycardia, hypertension, fever, diaphoresis) + Vivid visual hallucinations (ZO जुड़े microzoopsia: small animals, insects) + Coarse tremors. TREATMENT PROTOCOL: 1. Benzodiazepines: Drug of choice (Long-acting: Diazepam or Chlordiazepoxide; or Lorazepam/Oxazepam in patients with hepatic failure/cirrhosis because they undergo direct glucuronidation without CYP metabolism). 2. IV THIAMINE (Vitamin B1): MUST BE GIVEN BEFORE ANY GLUCOSE INFUSION! (Thiamine is a cofactor for pyruvate dehydrogenase and alpha-ketoglutarate dehydrogenase; giving glucose first causes acute neuronal death).",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 20 (Substance-Related Disorders); Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Psychiatry",
        "concept_name": "Child & Adolescent Psychiatry: Autism Spectrum Disorder vs ADHD",
        "stem": (
            "A 3-year-old boy is brought to the pediatric development clinic by his mother because he has not yet developed intelligible "
            "speech and fails to respond when his name is called, prompting concerns about deafness. Audiometry confirms normal hearing. "
            "In the observation playroom, he avoids eye contact, does not engage in pretend play or joint attention, and ignores other children. "
            "He exhibits rhythmic, repetitive hand-flapping whenever excited, insists on lining up his toy cars by color in an exact straight line, "
            "and throws violent tantrums if his daily routine or furniture arrangement is altered by even an inch. "
            "What is the most likely diagnosis under DSM-5 classification?"
        ),
        "options": [
            ("Autism Spectrum Disorder (ASD)", True, None),
            ("Attention-Deficit / Hyperactivity Disorder (ADHD)", False, "ADHD presents with inattention, hyperactivity, and impulsivity without profound deficits in joint attention, socio-emotional reciprocity, or stereotypies."),
            ("Social (Pragmatic) Communication Disorder", False, "Social communication disorder lacks the restricted, repetitive patterns of behavior, insistence on sameness, and stereotypies required for ASD."),
            ("Rett Syndrome with MECP2 mutation", False, "Rett syndrome occurs almost exclusively in girls, featuring normal early development followed by deceleration of head growth and loss of purposeful hand skills.")
        ],
        "pearl": "Autism Spectrum Disorder (ASD) - DSM-5 Diagnostic Dyad: 1. Persistent deficits in Social Communication and Social Interaction across multiple contexts: (A) Deficits in socio-emotional reciprocity (failure of normal back-and-forth conversation, lack of shared enjoyment) | (B) Deficits in nonverbal communicative behaviors (poor eye-to-eye contact, lack of facial expressions, lack of pointing/gestures) | (C) Deficits in developing and maintaining peer relationships. 2. Restricted, Repetitive Patterns of Behavior, Interests, or Activities (&ge;2 of 4): (A) Stereotyped or repetitive motor movements (hand-flapping, body rocking, toe-walking) | (B) Insistence on sameness, inflexible adherence to routines | (C) Highly restricted, fixated abnormal interests (lining up objects) | (D) Hyper- or hyporeactivity to sensory input. Core clinical pearls: Lack of 'JOINT ATTENTION' (not looking where parent points) by 12-18 months is the earliest red-flag warning! First-line intervention: Intensive Early Behavioral Intervention (Applied Behavior Analysis, ABA).",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 32 (Autism Spectrum Disorder); Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed.",
        "difficulty": "easy"
    },

    # =========================================================================
    # --- GENERAL SURGERY (6 Questions) ---
    # =========================================================================
    {
        "subject": "General Surgery",
        "concept_name": "Acute Pancreatitis: Revised Atlanta Classification & Contrast CT Timing",
        "stem": (
            "A 48-year-old male presents with severe, unrelenting epigastric pain that radiates directly through to the mid-back and is "
            "partially alleviated by sitting upright and leaning forward. He has had persistent non-bilious vomiting for 12 hours. "
            "Serum amylase is 1420 U/L (normal <100 U/L) and serum lipase is 3890 U/L. His pulse is 112 bpm, BP is 100/64 mmHg, and respiratory rate is 22/min. "
            "A junior resident suggests ordering an immediate emergency Contrast-Enhanced Computed Tomography (CECT) scan of the abdomen at hour 6 of admission. "
            "Why is performing CECT at hour 6 inappropriate, and what is the optimal guideline-recommended timing for staging pancreatic necrosis?"
        ),
        "options": [
            ("Early CECT within the first 48 hours underestimates the true extent of pancreatic parenchymal necrosis; optimal CECT timing is 72 to 96 hours after symptom onset", True, None),
            ("CECT is completely contraindicated in acute pancreatitis because iodinated contrast converts mild pancreatitis into necrotizing pancreatitis", False, "Iodinated contrast does not cause necrosis; the issue is that early scans underestimate ischemia before perfusion demarcation settles."),
            ("CECT should only be performed after 4 weeks when a mature walled-off pancreatic necrosis (WOPN) has formed", False, "CECT is indicated at 72-96 hours to assess severity and guide early ICU/step-up management; waiting 4 weeks is only for pseudocyst/WOPN drainage."),
            ("Ultrasonography is the definitive gold standard for quantifying pancreatic parenchymal and peripancreatic necrosis", False, "Ultrasound is obscured by overlying bowel gas (ileus) and cannot quantify parenchymal necrosis; its primary role is detecting gallstones.")
        ],
        "pearl": "Acute Pancreatitis - Revised Atlanta Consensus: Diagnostic Criteria (requires 2 of 3): 1. Characteristic abdominal pain (epigastric radiating to back, relieved by leaning forward) | 2. Serum Lipase or Amylase &ge;3 times the upper limit of normal (Lipase is more sensitive, specific, and stays elevated longer for 8-14 days) | 3. Characteristic imaging findings on CECT, MRI, or US. CONTRAST-ENHANCED CT (CECT) TIMING RULE: In patients without diagnostic uncertainty, CECT IS NOT INDICATED AT ADMISSION! Microvascular thrombosis and parenchymal demarcation require 72 to 96 hours to fully establish. Scans performed earlier (<48-72 hrs) significantly underestimate the true extent of pancreatic necrosis. OPTIMAL TIMING: 72 to 96 hours (3-4 days) after symptom onset. INITIAL MANAGEMENT: Aggressive fluid resuscitation with RINGER'S LACTATE (250-500 mL/hr) within the first 12-24 hours; target urine output &ge;0.5 mL/kg/hr. Routine prophylactic antibiotics are NOT recommended for sterile necrosis.",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 65 (Pancreas), p. 1150-1165; Schwartz's Principles of Surgery, 11th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "General Surgery",
        "concept_name": "Thyroid Malignancies: Papillary vs Follicular vs Medullary & Histopathology",
        "stem": (
            "A 32-year-old female presents with a painless, solitary, firm thyroid nodule measuring 2.2 cm in the right lobe with enlarged "
            "ipsilateral level III cervical lymph nodes. High-resolution ultrasound shows a solid, hypoechoic nodule with irregular, infiltrative "
            "margins, taller-than-wide dimensions, and multiple punctate internal microcalcifications. Fine-needle aspiration cytology (FNAC) "
            "demonstrates papillae lined by cells with ground-glass, pale, optically clear empty nuclei resembling cartoon eyes, prominent "
            "longitudinal nuclear grooves ('coffee-bean nuclei'), and concentric laminated calcospherites (Psammoma bodies). "
            "What is the diagnosis, and which genetic mutation is most strongly associated with this neoplasm?"
        ),
        "options": [
            ("Papillary Thyroid Carcinoma (PTC); BRAF V600E point mutation", True, None),
            ("Follicular Thyroid Carcinoma; Germline RET proto-oncogene point mutation", False, "Follicular carcinoma is associated with RAS mutations or PAX8-PPARgamma fusions, while RET mutations cause Medullary Thyroid Carcinoma."),
            ("Medullary Thyroid Carcinoma; APC tumor suppressor gene inactivation", False, "MTC arises from calcitonin-secreting parafollicular C cells, characterized by amyloid stroma and RET mutations."),
            ("Anaplastic Thyroid Carcinoma; RET/PTC chromosomal translocation", False, "Anaplastic carcinoma is driven by TP53 and TERT promoter mutations, presenting as a rapidly expanding fatal mass in the elderly.")
        ],
        "pearl": "Thyroid Carcinoma Master Comparison: 1. PAPILLARY THYROID CARCINOMA (PTC, ~80-85% of all thyroid cancers): Epidemiology: Females 3:1, prior ionizing radiation exposure. Spread: LYMPHATIC to regional cervical lymph nodes (hematogenous spread is rare). Microscopic Hallmarks: 'ORPHAN ANNIE EYE' nuclei (optically clear, ground-glass nuclei) + Nuclear pseudo-inclusions + Longitudinal Nuclear Grooves ('coffee-bean' appearance) + PSAMMOMA BODIES (laminated concentric microcalcifications formed by necrotic papillae tips). Molecular Driver: BRAF V600E mutation (~60%, associated with lymph node metastases) and RET/PTC translocations. Prognosis: Excellent (>95% 10-year survival). 2. FOLLICULAR THYROID CARCINOMA (~10-15%): Spread: HEMATOGENOUS to bones (osteolytic) and lungs. FNAC CANNOT distinguish follicular adenoma from carcinoma (requires surgical excision showing Capsular or Vascular Invasion!). 3. MEDULLARY THYROID CARCINOMA (MTC, ~5%): Origin: Parafollicular C cells (neuroendocrine, secretes CALCITONIN). Amyloid stroma on Congo red (apple-green birefringence under polarized light). Genetic driver: Germline RET proto-oncogene (screen all patients for MEN 2A and 2B!).",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 54 (Thyroid Gland), p. 815-832; Robbins & Cotran Pathologic Basis of Disease, 10th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "General Surgery",
        "concept_name": "Burn Resuscitation: Wallace Rule of Nines & Parkland Formula Calculation",
        "stem": (
            "A 70-kg adult male sustains extensive thermal flame burns in an industrial boiler explosion at 10:00 AM. He arrives at the burn "
            "resuscitation unit at 12:00 PM (noon). Assessment reveals full-thickness burns involving the entire anterior torso (chest and abdomen, 18%), "
            "the entire right upper extremity (9%), and the entire right lower extremity (circumferential, 18%). "
            "Using the Baxter / Parkland formula, what is the TOTAL volume of Ringer's Lactate required in the first 24 hours, and at what rate "
            "must the first portion be infused over the remaining 6 hours of the initial 8-hour window?"
        ),
        "options": [
            ("Total 24-hr fluid: 12,600 mL; Infuse 6,300 mL over the next 6 hours (1,050 mL/hr) so that the first half is completed by 6:00 PM (8 hours post-injury)", True, None),
            ("Total 24-hr fluid: 12,600 mL; Infuse 6,300 mL over the next 8 hours (787.5 mL/hr) calculated from the time of hospital admission", False, "Parkland timing is STRICTLY CALCULATED from the time of the burn injury (10:00 AM), NOT from hospital arrival (12:00 PM)!"),
            ("Total 24-hr fluid: 6,300 mL; Infuse 3,150 mL over 6 hours (525 mL/hr) using normal 0.9% saline", False, "Calculates using 2 mL/kg/% instead of standard Parkland 4 mL/kg/%, and normal saline causes hyperchloremic metabolic acidosis; Ringer's lactate is preferred."),
            ("Total 24-hr fluid: 18,900 mL; Infuse 9,450 mL over 8 hours using 5% Dextrose with albumin colloids", False, "Colloids are not recommended in the first 8-24 hours because capillary leak allows albumin into the interstitium, worsening pulmonary edema.")
        ],
        "pearl": "Burns Resuscitation - Rule of Nines & Parkland Protocol: 1. WALLACE RULE OF NINES (Adult): Head and Neck = 9% | Each Upper Limb = 9% (both = 18%) | Anterior Trunk = 18% | Posterior Trunk = 18% | Each Lower Limb = 18% (both = 36%) | Perineum/Genitalia = 1%. Patient calculation: Anterior torso (18%) + Right arm (9%) + Right leg (18%) = 45% TBSA. 2. BAXTER / PARKLAND FORMULA: Total fluid in first 24 hours = 4 mL x Weight (kg) x % TBSA (2nd and 3rd degree burns). For 70 kg and 45% TBSA: 4 x 70 x 45 = 12,600 mL of RINGER'S LACTATE. 3. SCHEDULE OF FLUID DELIVERY: First half (50% = 6,300 mL) administered in the FIRST 8 HOURS CALCULATED FROM THE MOMENT OF BURN INJURY (not admission!). Since 2 hours elapsed before arrival, 6,300 mL must be infused in the remaining 6 hours (6,300 / 6 = 1,050 mL/hr). Second half (50% = 6,300 mL) infused over the remaining 16 hours (393.75 mL/hr). 4. CLINICAL ENDPOINT OF RESUSCITATION: Adult hourly urine output = 0.5 to 1.0 mL/kg/hr (30-50 mL/hr). In electrical burns with myoglobinuria: target 1.0-1.5 mL/kg/hr (75-100 mL/hr).",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 5 (Burns), p. 55-68; Sabiston Textbook of Surgery, 21st Ed.",
        "difficulty": "hard"
    },
    {
        "subject": "General Surgery",
        "concept_name": "Breast Oncology: Triple-Negative Biology & Sentinel Node Biopsy",
        "stem": (
            "A 42-year-old premenopausal woman presents with a firm, ill-defined 2.8 cm mass in the upper outer quadrant of her left breast. "
            "Ultrasound-guided core needle biopsy confirms high-grade Invasive Ductal Carcinoma (No Special Type). "
            "Immunohistochemistry (IHC) reveals: Estrogen Receptor (ER) 0% (negative), Progesterone Receptor (PR) 0% (negative), "
            "and HER2/neu score 0 (negative), categorizing the tumor as Triple-Negative Breast Cancer (TNBC). "
            "Which germline genetic mutation is most strongly associated with this specific molecular subtype, and why are hormonal agents "
            "(Tamoxifen / Letrozole) and Trastuzumab completely ineffective?"
        ),
        "options": [
            ("BRCA1 mutation; TNBC lacks estrogen/progesterone receptors and lacks HER2 gene amplification, having zero pharmacological target for endocrine therapy or anti-HER2 antibodies", True, None),
            ("BRCA2 mutation; TNBC overexpression of aromatase enzyme inactivates Tamoxifen", False, "BRCA2 mutations are more strongly associated with ER-positive breast cancers and male breast cancer, not basal-like TNBC."),
            ("TP53 (Li-Fraumeni); TNBC downregulates thymidylate synthase causing primary endocrine resistance", False, "TP53 is mutated in Li-Fraumeni, but BRCA1 is the classic germline mutation in up to 70-80% of hereditary TNBC."),
            ("PTEN (Cowden syndrome); TNBC possesses hyperphosphorylated HER2 receptors that evade Trastuzumab binding", False, "HER2 is negative (not amplified/expressed) in TNBC, so Trastuzumab has no receptor to bind to.")
        ],
        "pearl": "Breast Cancer Molecular Subtypes & TNBC: 1. LUMINAL A: ER+, PR+, HER2-, low Ki-67 (<14%). Best prognosis, highly responsive to endocrine therapy. 2. LUMINAL B: ER+, PR+ (or -), HER2+ (or -), high Ki-67 (&ge;14%). 3. HER2-ENRICHED: ER-, PR-, HER2+ (amplified). Responsive to Trastuzumab, Pertuzumab, T-DM1. 4. TRIPLE-NEGATIVE BREAST CANCER (TNBC, ~15-20%): ER-, PR-, and HER2-negative. Highly aggressive, high histological grade, early visceral and brain metastases, younger women. Strongly associated with germline BRCA1 mutations (up to 70-80% of BRCA1-associated breast cancers are TNBC). Treatment: Since hormonal therapy (Tamoxifen, Letrozole) and anti-HER2 therapy (Trastuzumab) have NO TARGET, systemic CHEMOTHERAPY (Anthracyclines + Taxanes + Carboplatin) + Immunotherapy (Pembrolizumab / anti-PD-1) is the standard backbone! PARP inhibitors (Olaparib, Talazoparib) are effective in BRCA-mutated TNBC via synthetic lethality.",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 57 (The Breast), p. 870-900; NCCN Guidelines for Breast Cancer 2023.",
        "difficulty": "medium"
    },
    {
        "subject": "General Surgery",
        "concept_name": "Colorectal Oncology: Left vs Right Colon Cancer & Lynch Syndrome",
        "stem": (
            "A 36-year-old male presents with fatigue and dyspnea on exertion. Routine labs reveal microcytic hypochromic anemia "
            "(Hemoglobin 7.2 g/dL, serum ferritin 8 ng/mL). Stool occult blood is positive. Colonoscopy reveals a friable, exophytic mass in "
            "the cecum; biopsy confirms adenocarcinoma. Family history is notable: his father died of colorectal cancer at age 42, his paternal "
            "aunt had endometrial cancer at age 40, and his brother was recently diagnosed with colon cancer at age 35. "
            "Deficiency in which cellular DNA repair system causes this hereditary syndrome (Lynch Syndrome / HNPCC)?"
        ),
        "options": [
            ("DNA Mismatch Repair (MMR) system (MLH1, MSH2, MSH6, PMS2) leading to Microsatellite Instability (MSI-High)", True, None),
            ("Nucleotide Excision Repair (NER) pathway leading to pyrimidine dimer accumulation", False, "NER pathway deficiency causes Xeroderma Pigmentosum, leading to severe UV light sensitivity and cutaneous neoplasms."),
            ("Adenomatous Polyposis Coli (APC) tumor suppressor gene deletion causing widespread polyposis (>100 polyps)", False, "APC mutations cause Familial Adenomatous Polyposis (FAP) with thousands of adenomatous polyps, unlike Lynch syndrome which is non-polyposis."),
            ("Homologous Recombination Double-Strand Break Repair (HRD) mediated by ATM and CHEK2", False, "HRD deficiency is characteristic of BRCA1/2 and Fanconi anemia pathways, not Lynch syndrome.")
        ],
        "pearl": "Colorectal Cancer - Right vs Left Colon & Lynch Syndrome: 1. RIGHT-SIDED (Proximal / Cecal) CANCER: Large lumen + liquid feces &rarr; DOES NOT OBSTRUCT EARLY! Presents with: Occult blood loss, severe iron-deficiency anemia, unexplained fatigue, palpable right iliac fossa mass, exophytic fungating tumor. 2. LEFT-SIDED (Distal / Rectosigmoid) CANCER: Narrow lumen + solid feces &rarr; OBSTRUCTION! Presents with: Altered bowel habits (constipation alternating with diarrhea), pencil-thin stools, fresh rectal bleeding (hematochezia), annular 'napkin-ring' / 'apple-core' constriction on barium enema. 3. HEREDITARY NON-POLYPOSIS COLORECTAL CANCER (HNPCC / LYNCH SYNDROME): Autosomal dominant. Etiology: Germline mutations in DNA MISMATCH REPAIR (MMR) genes: MSH2 (~40%), MLH1 (~40%), MSH6 (~10%), PMS2 (~5%). Leads to MICROSATELLITE INSTABILITY (MSI-H). Associated extracolonic malignancies: ENDOMETRIAL CANCER (most common extracolonic cancer in females!), ovarian, stomach, small bowel, and transitional cell urothelial carcinoma. AMSTERDAM II CRITERIA (3-2-1 rule): At least 3 relatives with Lynch-associated cancers + Across 2 successive generations + 1 diagnosed before age 50.",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 73 (Colorectal Cancer), p. 1320-1345; Robbins Basic Pathology, 10th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "General Surgery",
        "concept_name": "Lower Extremity Ulcerations: Arterial vs Venous Stasis vs Neuropathic",
        "stem": (
            "A 58-year-old female with long-standing varicose veins and chronic ankle edema presents with a 3-month history of a persistent, "
            "shallow ulcer over the medial malleolus of her right lower leg. The ulcer bed has healthy red granulation tissue with irregular margins "
            "and copious serous exudate. The surrounding skin exhibits hyperpigmentation, brawny induration, and woody fibrosis ('champagne-bottle' leg). "
            "Both dorsalis pedis and posterior tibial pulses are easily palpable with normal capillary refill time. "
            "What is the underlying pathophysiology of this ulcer, and what is the definitive gold-standard conservative therapy?"
        ),
        "options": [
            ("Venous Hypertension secondary to valvular incompetence of deep or perforator veins; Multi-layer Graduated Compression Bandaging (30-40 mmHg at the ankle)", True, None),
            ("Atherosclerotic arterial insufficiency; Immediate balloon angioplasty and complete avoidance of compression", False, "Normal distal pulses, medial malleolar location, and surrounding hemosiderin rule out arterial ischemia. Compression is the gold standard for venous ulcers."),
            ("Diabetic peripheral sensory neuropathy; Total Contact Casting (TCC) to offload plantar pressure", False, "Neuropathic ulcers occur on the pressure-bearing plantar aspects of the metatarsal heads or heel, not the medial malleolar gaiter zone."),
            ("Necrotizing vasculitis; High-dose systemic corticosteroids and cyclophosphamide", False, "Vasculitic ulcers (e.g. pyoderma gangrenosum) present as painful violaceous undermined borders, not classical stasis dermatitis.")
        ],
        "pearl": "Lower Extremity Ulcer Differential Table: 1. VENOUS STASIS ULCER (Most common, ~70-80%): Location: GAITER ZONE (medial malleolus). Morphology: Large, shallow, irregular edges, healthy pink-red granulation tissue base, EXUDATIVE. Surrounding skin: Stasis dermatitis, HEMOSIDERIN HYPERPIGMENTATION (extravasated RBC breakdown), lipodermatosclerosis (inverted champagne-bottle leg), corona phlebectatica. Pain: Mild to moderate dull ache, RELIEVED BY LEG ELEVATION! Distal pulses: NORMAL. GOLD STANDARD TREATMENT: MULTI-LAYER GRADUATED COMPRESSION BANDAGING (30-40 mmHg). 2. ARTERIAL ULCER (~10-15%): Location: Distal extremities (tips of toes, interdigital spaces, heel, lateral malleolus). Morphology: 'PUNCHED-OUT' deep circular margins, pale necrotic gray base, dry, minimal exudate. Surrounding skin: Shiny, hairless, cold, atrophic, thickened nails. Pain: EXCRUCIATING, worse with elevation (hanging foot over bed relieves pain!). Distal pulses: ABSENT OR DIMINISHED. ABI <0.8 (critical ischemia <0.5). CONTRAINDICATION: NEVER APPLY COMPRESSION IN ARTERIAL INSUFFICIENCY (causes gangrene!).",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 60 (Vascular Disorders), p. 970-985; Rutherford's Vascular Surgery, 10th Ed.",
        "difficulty": "easy"
    },

    # =========================================================================
    # --- GENERAL MEDICINE (4 Questions) ---
    # =========================================================================
    {
        "subject": "General Medicine",
        "concept_name": "Acute Kidney Injury: KDIGO Staging & Pre-Renal vs ATN Differentiation",
        "stem": (
            "A 64-year-old male with septic shock secondary to pneumonia receives broad-spectrum antibiotics and resuscitation in the ICU. "
            "Over 48 hours, his urine output drops to 15 mL/hour (oliguria) and serum creatinine rises from a baseline of 1.0 mg/dL to 3.4 mg/dL. "
            "Urine microscopy reveals dirty-brown granular casts and renal tubular epithelial cell casts. "
            "Urinary sodium is 56 mEq/L, fractional excretion of sodium (FENa) is 2.8%, and urine osmolality is 280 mOsm/kg H2O. "
            "What form of renal injury does this clinical and laboratory profile indicate?"
        ),
        "options": [
            ("Intrinsic Acute Kidney Injury secondary to Ischemic Acute Tubular Necrosis (ATN)", True, None),
            ("Pre-renal azotemia from persistent hypovolemia", False, "Pre-renal azotemia is characterized by avid tubular sodium retention: FENa <1%, urine sodium <20 mEq/L, urine osmolality >500 mOsm/kg, and bland hyaline casts."),
            ("Post-renal acute obstructive uropathy", False, "Obstructive uropathy shows hydronephrosis on ultrasound without granular tubular casts or FENa >2%."),
            ("Acute interstitial nephritis (AIN) secondary to beta-lactam antibiotics", False, "AIN classically presents with fever, rash, eosinophilia, sterile pyuria, and urinary eosinophil / WBC casts, not muddy-brown ATN casts.")
        ],
        "pearl": "Pre-Renal Azotemia vs Intrinsic ATN Differentiation: 1. PRE-RENAL AZOTEMIA: Pathophysiology: Renal hypoperfusion with INTACT, functionally normal tubular machinery that avidity retains sodium and water to preserve circulating intravascular volume. Laboratory parameters: BUN-to-Creatinine ratio > 20:1 | Fractional Excretion of Sodium (FENa) < 1% (Fractional excretion of urea FEUrea <35% if on diuretics) | Urine Sodium < 20 mEq/L | Urine Osmolality > 500 mOsm/kg | Urine sediment: BLAND, normal, or transparent HYALINE CASTS. Responsive to fluid resuscitation. 2. ACUTE TUBULAR NECROSIS (Intrinsic AKI): Pathophysiology: Ischemic or nephrotoxic injury leading to tubular cell necrosis and sloughing into lumens. Tubules LOSE concentrating and sodium-reabsorbing capacity! Laboratory parameters: BUN-to-Creatinine ratio < 15:1 | FENa > 2% | Urine Sodium > 40 mEq/L | Urine Osmolality < 350 mOsm/kg (isosthenuric, identical to plasma ~300) | Urine sediment: PATHOGNOMONIC MUDDY-BROWN GRANULAR CASTS & Renal Tubular Epithelial (RTE) cells.",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 304 (Acute Kidney Injury), p. 2295-2310; KDIGO AKI Guidelines.",
        "difficulty": "medium"
    },
    {
        "subject": "General Medicine",
        "concept_name": "Secondary Hypertension: Primary Hyperaldosteronism (Conn Syndrome)",
        "stem": (
            "A 44-year-old male is referred for evaluation of persistent hypertension (BP 168/104 mmHg) that remains uncontrolled despite "
            "adherent treatment with three antihypertensive agents of different classes (Amlodipine 10 mg, Telmisartan 80 mg, and Indapamide 2.5 mg). "
            "He complains of occasional muscle cramps and fatigue. Routine metabolic panel reveals: Serum Sodium 144 mEq/L, Serum Potassium 2.9 mEq/L "
            "(hypokalemia), and Serum Bicarbonate 31 mEq/L (metabolic alkalosis). "
            "What is the recommended initial screening test to confirm or exclude Primary Hyperaldosteronism?"
        ),
        "options": [
            ("Morning paired Plasma Aldosterone Concentration to Plasma Renin Activity ratio (ARR)", True, None),
            ("24-hour urinary free cortisol and overnight 1 mg dexamethasone suppression test", False, "Dexamethasone suppression evaluates Cushing's syndrome, not primary hyperaldosteronism."),
            ("Contrast-enhanced CT scan of the adrenal glands as initial screening", False, "Biochemical screening with ARR must precede imaging; non-functioning adrenal incidentalomas are common (~5% of population) and cause misdiagnosis."),
            ("24-hour urinary fractionated metanephrines and catecholamines", False, "Urinary metanephrines screen for pheochromocytoma, which presents with paroxysmal headache, sweating, and palpitations.")
        ],
        "pearl": "Primary Hyperaldosteronism (Conn's Syndrome): Most common surgically curable cause of secondary hypertension (found in 5-10% of all hypertensive patients and up to 20% of resistant hypertension!). Clinical Hallmarks: Resistant Hypertension + Spontaneous (or diuretic-induced) Hypokalemia + Metabolic Alkalosis (Aldosterone acts on principal cells in cortical collecting duct to reabsorb Na+ in exchange for K+ and H+ secretion). Note: >50% of patients with confirmed hyperaldosteronism have normal potassium on presentation! SCREENING TEST OF CHOICE: Morning Paired Plasma Aldosterone Concentration (PAC in ng/dL) to Plasma Renin Activity (PRA in ng/mL/hr) ratio &mdash; ARR. An ARR > 20 to 30 with PAC &ge; 15 ng/dL is a POSITIVE SCREEN. CONFIRMATORY TESTING: Oral sodium loading test or IV normal saline infusion test (failure to suppress aldosterone <5 ng/dL confirms autonomous hyperaldosteronism). SUBTYPE LOCALIZATION: Adrenal CT followed by ADRENAL VEIN SAMPLING (AVS, gold standard to distinguish unilateral aldosterone-producing adenoma [treated by laparoscopic adrenalectomy] from bilateral adrenal hyperplasia [treated with Spironolactone / Eplerenone]).",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 379 (Endocrine Hypertension); Endocrine Society Clinical Guidelines 2016.",
        "difficulty": "medium"
    },
    {
        "subject": "General Medicine",
        "concept_name": "Rheumatology: Systemic Lupus Erythematosus & Lupus Nephritis Classes",
        "stem": (
            "A 26-year-old female presents with a 4-month history of fatigue, inflammatory polyarthritis of the PIP and MCP joints of both hands, "
            "malar rash sparing the nasolabial folds, and photosensitivity. Urinalysis reveals 3+ proteinuria, 15-20 RBCs/hpf with dysmorphic red cells, "
            "and cellular casts. Serum ANA is positive at 1:640 (speckled pattern) and anti-dsDNA is strongly positive at 180 IU/mL. Serum complement C3 and C4 are severely depressed. "
            "Renal biopsy demonstrates extensive subendothelial immune complex deposits ('wire-loop' lesions on light microscopy), endocapillary "
            "hypercellularity involving 75% of glomeruli, and full-house immunofluorescence (IgG, IgA, IgM, C3, C1q). "
            "According to the ISN/RPS classification, what class of lupus nephritis does this biopsy represent, and what is the standard induction regimen?"
        ),
        "options": [
            ("Class IV: Diffuse Proliferative Lupus Nephritis; High-dose IV Corticosteroids combined with either Mycophenolate Mofetil (MMF) or IV Cyclophosphamide (Eurolupus regimen)", True, None),
            ("Class II: Mesangial Proliferative Lupus Nephritis; Hydroxychloroquine monotherapy without immunosuppression", False, "Class II is restricted to mesangial proliferation with normal renal function and minimal proteinuria; wire-loop lesions and >50% glomerular necrosis define Class IV."),
            ("Class V: Membranous Lupus Nephritis; ACE inhibitor monotherapy and observation", False, "Class V features subepithelial immune deposits with nephrotic syndrome; diffuse endocapillary hypercellularity and wire loops define Class IV."),
            ("Class I: Minimal Mesangial Nephritis; Low-dose non-steroidal anti-inflammatory drugs", False, "Class I shows normal light microscopy with mesangial deposits visible on IF only; this patient has active diffuse glomerulonephritis.")
        ],
        "pearl": "Systemic Lupus Erythematosus (SLE) & Lupus Nephritis: Diagnostic Criteria (2019 EULAR/ACR): Mandatory entry criterion: Antinuclear Antibodies (ANA) titer &ge; 1:80 on HEp-2 cells. Autoantibody specificity: 1. Anti-dsDNA: Highly specific (~95%), CORRELATES CLOSELY WITH DISEASE ACTIVITY AND RENAL FLARES! 2. Anti-Smith (Sm): Most specific antibody for SLE (~99%), but does NOT correlate with disease activity. 3. Anti-Ro (SSA) / Anti-La (SSB): Associated with Subacute Cutaneous Lupus, neonatal lupus, and congenital complete heart block! ISN/RPS LUPUS NEPHRITIS CLASSIFICATION: Class I: Minimal mesangial | Class II: Mesangial proliferative | Class III: Focal proliferative (<50% of glomeruli) | Class IV: DIFFUSE PROLIFERATIVE (&ge;50% glomeruli, most common and most aggressive, pathognomonic WIRE-LOOP LESIONS from subendothelial immune deposits, subendothelial electron-dense deposits on EM, low C3/C4) | Class V: Membranous (subepithelial deposits, nephrotic range proteinuria) | Class VI: Advanced sclerosing (&ge;90% sclerosed glomeruli). INDUCTION FOR CLASS III/IV: IV Pulse Methylprednisolone + Oral Prednisone PLUS Mycophenolate Mofetil (MMF) or IV Cyclophosphamide (Eurolupus trial).",
        "citation": "Harrison's Principles of Internal Medicine, 21st Ed, Chapter 356 (SLE), p. 2730-2745; KDIGO Glomerular Diseases Guideline 2021.",
        "difficulty": "hard"
    },
    {
        "subject": "General Medicine",
        "concept_name": "Critical Care: Sepsis-3 Consensus Definitions & Septic Shock Resuscitation",
        "stem": (
            "A 62-year-old diabetic female is admitted with high fever, chills, and productive purulent cough. In the emergency ward, "
            "her respiratory rate is 28 breaths/min, blood pressure is 82/50 mmHg, Glasgow Coma Scale (GCS) is 13, and heart rate is 122 bpm. "
            "Arterial blood gas reveals metabolic lactic acidosis with a serum lactate of 4.2 mmol/L. "
            "Despite rapid intravenous infusion of 30 mL/kg of balanced crystalloid (Ringer's lactate) over 60 minutes, her mean arterial pressure "
            "(MAP) remains 54 mmHg and serum lactate remains elevated at 3.8 mmol/L. "
            "Under Sepsis-3 criteria, what is the diagnosis, and what is the FIRST-LINE vasopressor of choice to restore perfusion pressure?"
        ),
        "options": [
            ("Septic Shock; Intravenous Norepinephrine infusion titrated to target Mean Arterial Pressure (MAP) &ge; 65 mmHg", True, None),
            ("Uncomplicated Sepsis; Intravenous Dopamine infusion at inotropic doses (5-10 mcg/kg/min)", False, "Dopamine is associated with significantly higher tachyarrhythmias and increased mortality compared to Norepinephrine in the SOAP II trial."),
            ("Systemic Inflammatory Response Syndrome (SIRS); Intravenous Epinephrine boluses", False, "Sepsis-3 eliminated SIRS criteria in favor of SOFA score; septic shock requires continuous titratable norepinephrine infusion, not epinephrine boluses."),
            ("Refractory Hypovolemic Shock; Infuse an additional 6 liters of normal saline prior to considering vasopressors", False, "Continuing massive fluid loading without vasopressors causes lethal tissue edema, abdominal compartment syndrome, and pulmonary capillary leak.")
        ],
        "pearl": "Sepsis-3 International Consensus Definitions: 1. SEPSIS: Life-threatening organ dysfunction caused by a dysregulated host response to infection. Organ dysfunction is quantified clinically by an acute change in TOTAL SOFA SCORE &ge; 2 points (associated with in-hospital mortality >10%). Bedside screening tool: quickSOFA (qSOFA, 1 point each: Respiratory rate &ge; 22/min, Altered mental status GCS < 15, Systolic blood pressure &le; 100 mmHg; score &ge;2 indicates high risk). 2. SEPTIC SHOCK: A subset of sepsis in which underlying circulatory and cellular/metabolic abnormalities are profound enough to substantially increase mortality (>40%). CLINICAL CRITERIA FOR SEPTIC SHOCK: Sepsis with PERSISTING HYPOTENSION requiring VASOPRESSORS to maintain MAP &ge; 65 mmHg AND Serum Lactate > 2 mmol/L (18 mg/dL) DESPITE ADEQUATE VOLUME RESUSCITATION (30 mL/kg crystalloids within 3 hours). FIRST-LINE VASOPRESSOR: NOREPINEPHRINE (Levophed: potent alpha-1 vasoconstriction with modest beta-1 inotropy; superior to dopamine). Second-line add-on: Vasopressin (at fixed dose 0.03 U/min). Target MAP: &ge;65 mmHg.",
        "citation": "Surviving Sepsis Campaign International Guidelines 2021; Harrison's Principles of Internal Medicine, 21st Ed, Chapter 297.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- PHARMACOLOGY (4 Questions) ---
    # =========================================================================
    {
        "subject": "Pharmacology",
        "concept_name": "Antidiabetic Pharmacology: SGLT-2 Inhibitors & GLP-1 Receptor Agonists",
        "stem": (
            "A 56-year-old male with type 2 diabetes mellitus, established coronary artery disease (post-CABG), and heart failure with "
            "reduced ejection fraction (HFrEF, EF 32%) has an HbA1c of 8.4% on Metformin 1000 mg twice daily. "
            "His eGFR is 48 mL/min/1.73m² and BMI is 31 kg/m². "
            "Which class of oral antidiabetic agents provides proven reduction in cardiovascular mortality and heart failure hospitalizations "
            "while delaying the progression of chronic kidney disease, but carries a unique risk of Euglycemic Diabetic Ketoacidosis (euDKA)?"
        ),
        "options": [
            ("Sodium-Glucose Cotransporter-2 (SGLT-2) Inhibitors (e.g., Empagliflozin, Dapagliflozin)", True, None),
            ("Sulfonylureas (e.g., Glimepiride, Gliclazide)", False, "Sulfonylureas cause hypoglycemia and weight gain; they lack heart failure and nephroprotective benefits and do not cause euglycemic DKA."),
            ("Thiazolidinediones (e.g., Pioglitazone)", False, "Pioglitazone causes fluid retention and sodium reabsorption via PPAR-gamma; it is STRICTLY CONTRAINDICATED in NYHA Class III/IV heart failure."),
            ("Dipeptidyl Peptidase-4 (DPP-4) Inhibitors (e.g., Saxagliptin, Sitagliptin)", False, "DPP-4 inhibitors are cardiovascularly neutral (Saxagliptin actually increases heart failure hospitalizations in the SAVOR-TIMI trial).")
        ],
        "pearl": "SGLT-2 Inhibitors ('Gliflozins' - Empagliflozin, Dapagliflozin, Canagliflozin): Mechanism: Reversibly inhibit SGLT-2 cotransporters in the S1/S2 segments of the PROXIMAL CONVOLUTED TUBULE (PCT), blocking reabsorption of ~90% of filtered glucose and sodium. Clinical benefits: 1. Glucosuria &rarr; Lowers blood glucose, HbA1c (0.5-1%), and promotes weight loss (2-3 kg). 2. Natriuresis & Osmotic Diuresis &rarr; Lowers blood pressure and cardiac preload. 3. Renoprotection: Restores Tubuloglomerular Feedback (TGF) by delivering sodium to macula densa, constricting afferent arteriole, reducing intraglomerular hypertension. Landmark trials (EMPA-REG, DAPA-HF, EMPEROR-Reduced) proved substantial reduction in Heart Failure Hospitalizations and Cardiovascular Mortality (now a core pillar of Guideline-Directed Medical Therapy for HFrEF and HFpEF even in NON-DIABETICS!). ADVERSE EFFECTS & WARNINGS: 1. Mycotic genital infections (candidal balanitis/vulvovaginitis, most common) | 2. EUGLYCEMIC DIABETIC KETOACIDOSIS (euDKA: blood glucose <250 mg/dL with severe ketoacidosis due to glucagon rise and volume loss) | 3. Fournier's gangrene (perineal necrotizing fasciitis).",
        "citation": "Goodman & Gilman's The Pharmacological Basis of Therapeutics, 14th Ed, Chapter 47; KDIGO 2022 Diabetes in CKD Guidelines.",
        "difficulty": "medium"
    },
    {
        "subject": "Pharmacology",
        "concept_name": "Anticoagulants: Direct Oral Anticoagulants (DOACs) & Specific Antidotes",
        "stem": (
            "A 72-year-old female with non-valvular atrial fibrillation has been maintained on the direct thrombin inhibitor Dabigatran etexilate "
            "(150 mg twice daily). Following a major motor vehicle collision, she sustains severe blunt abdominal trauma with active intra-abdominal "
            "bleeding and splenic laceration. Immediate emergency splenectomy is required. Her thrombin time (TT) and ecarin clotting time (ECT) are markedly prolonged. "
            "Which of the following represents the SPECIFIC, rapid-acting monoclonal antibody reversal agent for Dabigatran?"
        ),
        "options": [
            ("Idarucizumab (Praxbind)", True, None),
            ("Andexanet Alfa (Andexxa)", False, "Andexanet alfa is a recombinant modified decoy Factor Xa protein used to reverse oral Factor Xa inhibitors (Rivaroxaban and Apixaban), not Dabigatran."),
            ("Protamine Sulfate", False, "Protamine sulfate is the specific antidote for unfractionated heparin (and partially low-molecular-weight heparin), ineffective against Dabigatran."),
            ("Vitamin K1 (Phytonadione) combined with 4-Factor Prothrombin Complex Concentrate", False, "Vitamin K is the reversal agent for Warfarin (coumarin derivatives) by restoring gamma-carboxylation of factors II, VII, IX, and X; it has no effect on direct thrombin inhibitors.")
        ],
        "pearl": "DOACs & Specific Reversal Agents Master Table: 1. DIRECT THROMBIN (FACTOR IIa) INHIBITOR: DABIGATRAN ETEXILATE (oral prodrug directly binding active site of free and clot-bound thrombin). SPECIFIC REVERSAL AGENT: IDARUCIZUMAB (Praxbind). Chemistry: Humanized monoclonal antibody fragment (Fab). Mechanism: Binds free and thrombin-bound dabigatran with 350-fold higher affinity than thrombin, neutralizing anticoagulant effect within minutes of IV injection! 2. DIRECT FACTOR Xa INHIBITORS: RIVAROXABAN, APIXABAN, EDOXABAN. SPECIFIC REVERSAL AGENT: ANDEXANET ALFA (Andexxa). Chemistry: Recombinant catalytically inactive decoy form of human Factor Xa. Mechanism: Acts as a high-affinity 'molecular sponge' that sequesters circulating Xa inhibitors away from native factor Xa. 3. WARFARIN (Vitamin K antagonist): Reversal: 4-Factor Prothrombin Complex Concentrate (4F-PCC: contains factors II, VII, IX, X, Protein C & S) + IV Vitamin K1 (Phytonadione).",
        "citation": "Goodman & Gilman's The Pharmacological Basis of Therapeutics, 14th Ed, Chapter 32 (Blood Coagulation); Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Pharmacology",
        "concept_name": "Antimicrobial Pharmacology: Glycopeptide Resistance (VRE) & Treatment",
        "stem": (
            "A 58-year-old liver transplant recipient in the surgical ICU develops a catheter-associated bloodstream infection with Enterococcus faecium. "
            "Minimum inhibitory concentration (MIC) testing reveals resistance to Ampicillin and high-level resistance to Vancomycin (MIC > 64 mcg/mL). "
            "Genetic sequencing identifies the VanA resistance operon. "
            "What specific molecular biochemical modification in the cell wall peptidoglycan precursor confers this Vancomycin resistance?"
        ),
        "options": [
            ("Substitution of the terminal D-Alanyl-D-Alanine dipeptide with D-Alanyl-D-Lactate, causing the loss of a critical hydrogen bond and a 1,000-fold reduction in vancomycin binding affinity", True, None),
            ("Plasmid-mediated production of beta-lactamase enzyme that hydrolyzes the cyclic heptapeptide core of vancomycin", False, "Beta-lactamases hydrolyze the four-membered beta-lactam ring of penicillins/cephalosporins; glycopeptides lack a beta-lactam ring."),
            ("Methylation of the 23S rRNA at the 50S ribosomal subunit by Erm methyltransferase", False, "Erm methylation of 23S rRNA confers MLSb resistance (Macrolides, Lincosamides, Streptogramin B), not glycopeptide resistance."),
            ("Mutation in DNA gyrase (gyrA) and topoisomerase IV (parC) preventing drug intercalation", False, "GyrA and ParC mutations confer high-level resistance to Fluoroquinolones (Ciprofloxacin, Levofloxacin).")
        ],
        "pearl": "Vancomycin Mechanism & Resistance (VRE): Mechanism of Action: Vancomycin (bactericidal glycopeptide) binds with high affinity to the terminal D-Ala-D-Ala pentapeptide termini of peptidoglycan cell-wall monomers via 5 hydrogen bonds. This sterically blocks transglycosylase (chain elongation) and transpeptidase (cross-linking), weakening the bacterial cell wall and causing osmotic lysis. MECHANISM OF VRE (VanA and VanB phenotypes in Enterococcus faecium & E. faecalis): Plasmid/transposon-mediated acquisition of enzymes (VanA ligase) that replace the normal terminal D-Alanyl-D-Alanine with D-ALANYL-D-LACTATE (or D-Ala-D-Ser in VanC). Because oxygen replaces nitrogen in an ester linkage, ONE CRITICAL HYDROGEN BOND IS LOST, reducing Vancomycin binding affinity by 1,000-fold! TREATMENT OF VANCOMYCIN-RESISTANT ENTEROCOCCI (VRE): 1. Linezolid (oxazolidinone, inhibits 50S ribosomal initiation) | 2. Daptomycin (cyclic lipopeptide, calcium-dependent membrane depolarization; inactive in pneumonia due to surfactant binding) | 3. Quinupristin-Dalfopristin (effective against E. faecium, NOT E. faecalis!).",
        "citation": "Goodman & Gilman's The Pharmacological Basis of Therapeutics, 14th Ed, Chapter 57; Kucers' The Use of Antibiotics, 7th Ed.",
        "difficulty": "hard"
    },
    {
        "subject": "Pharmacology",
        "concept_name": "Antiepileptic Drugs: Broad vs Narrow Spectrum & Absence Seizures",
        "stem": (
            "An 8-year-old schoolgirl is brought for evaluation because her teacher reports frequent 5- to 10-second episodes during class "
            "where she abruptly stops speaking mid-sentence, stares blankly into space with subtle fluttering of the eyelids, and fails to respond. "
            "Immediately after the episode, she resumes her conversation with full alertness and zero post-ictal confusion. "
            "Electroencephalography (EEG) during hyperventilation reveals paroxysmal, synchronous, bilateral 3-Hz generalized spike-and-wave discharges. "
            "What is the DRUG OF CHOICE for this condition, and what is its specific molecular mechanism of action?"
        ),
        "options": [
            ("Ethosuximide; Selective blockade of low-threshold T-type voltage-gated calcium channels in thalamocortical relay neurons", True, None),
            ("Carbamazepine; Prolongation of sodium channel inactivation state", False, "Carbamazepine is a narrow-spectrum AED for focal seizures that PARADOXICALLY EXACERBATES absence and myoclonic seizures!"),
            ("Phenytoin; Post-tetanic potentiation inhibition and zero-order kinetics", False, "Phenytoin worsens absence seizures and carries severe long-term toxicities (gingival hyperplasia, hirsutism)."),
            ("Diazepam; Positive allosteric modulation of GABA-A receptor chloride conductance", False, "Benzodiazepines are used for acute abortive management of status epilepticus, not chronic first-line monotherapy for childhood absence epilepsy.")
        ],
        "pearl": "Absence (Petit Mal) Seizures & Antiepileptic Pharmacology: Clinical Triad: Abrupt loss of consciousness (5-15 sec) + Preservation of postural tone (no fall) + Immediate recovery WITHOUT post-ictal confusion. EEG Hallmark: SYNCHRONOUS BILATERAL 3-Hz SPIKE-AND-WAVE DISCHARGES triggered reliably by hyperventilation or photic stimulation. Pathophysiology: Hyper-synchronous rhythmic oscillatory bursting between thalamic relay neurons and cortex, mediated by Low-Threshold T-Type Calcium Channels. DRUGS OF CHOICE: 1. ETHOSUXIMIDE: First-line drug of choice for PURE absence seizures! Molecular mechanism: Selectively blocks T-type Ca2+ channels in the thalamus, dampening the pacemaker circuit. Highly effective with minimal behavioral/cognitive side effects. 2. SODIUM VALPROATE: Broad-spectrum drug of choice if absence seizures COEXIST WITH GENERALIZED TONIC-CLONIC OR MYOCLONIC SEIZURES (Ethosuximide only covers absence). DANGEROUS CONTRAINDICATION: Narrow-spectrum sodium channel blockers (Carbamazepine, Oxcarbazepine, Phenytoin, Vigabatrin) MUST NEVER BE GIVEN IN ABSENCE OR MYOCLONIC EPILEPSIES &mdash; they precipitate status epilepticus and worsen seizure frequency!",
        "citation": "Goodman & Gilman's The Pharmacological Basis of Therapeutics, 14th Ed, Chapter 17; Nelson Textbook of Pediatrics, 21st Ed.",
        "difficulty": "easy"
    }
]
