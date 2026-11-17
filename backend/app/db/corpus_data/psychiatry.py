"""
Authentic High-Yield NEET-PG Clinical Questions for Psychiatry
References: Niraj Ahuja's A Short Textbook of Psychiatry (8th Ed), Kaplan & Sadock's Synopsis of Psychiatry (12th Ed)
"""

PSYCHIATRY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Alcohol Withdrawal & Delirium Tremens",
        "stem": (
            "A 46-year-old chronic heavy alcoholic male is admitted to the surgical ward for an elective inguinal hernia repair. "
            "Forty-eight hours after admission, he becomes severely agitated, disoriented to time and place, and tremulous, "
            "complaining that small insects and snakes are crawling all over his bedsheets (lilliputian visual hallucinations). "
            "Physical examination reveals marked autonomic instability: pulse 128 bpm, blood pressure 168/104 mmHg, "
            "coarse intention tremors of the outstretched hands, and profuse diaphoresis. "
            "What is the diagnosis and the single most critical, life-saving pharmacotherapeutic drug of choice?"
        ),
        "options": [
            ("Delirium Tremens; Intravenous Diazepam or Lorazepam (Benzodiazepines)", True, None),
            ("Wernicke Encephalopathy; Immediate high-dose intravenous Glucose infusion alone", False, "Administering glucose without Thiamine can precipitate irreversible Wernicke encephalopathy and Korsakoff psychosis! Thiamine must always be given BEFORE glucose."),
            ("Alcoholic Hallucinosis; Oral Disulfiram 250 mg daily", False, "Disulfiram is a deterrent agent used in abstinent patients; given during acute withdrawal, it causes fatal acetaldehyde syndrome!"),
            ("Acute Psychosis; Intravenous Haloperidol monotherapy", False, "Antipsychotics like Haloperidol lower the seizure threshold and lack cross-tolerance with alcohol; Benzodiazepines are mandatory.")
        ],
        "pearl": "Alcohol Withdrawal Timeline & Management: 6-12 hours: Minor withdrawal (tremors, insomnia, anxiety). 12-48 hours: Withdrawal seizures ('rum fits', generalized tonic-clonic) & Alcoholic Hallucinosis (auditory hallucinations, CLEAR sensorium). 48-72 hours (peaks day 3-4): DELIRIUM TREMENS (altered sensorium, autonomic hyperactivity, visual hallucinations). DRUG OF CHOICE: Benzodiazepines (Diazepam 10-20 mg or Lorazepam 2-4 mg). Lorazepam is preferred in liver disease (LOT: Lorazepam, Oxazepam, Temazepam undergo glucuronidation, no active metabolites). Wernicke's triad: Confusion + Ataxia + Ophthalmoplegia (Give THIAMINE BEFORE GLUCOSE!).",
        "citation": "Niraj Ahuja's A Short Textbook of Psychiatry, 8th Ed, Chapter 4 (Substance-Related Disorders), p. 48-62.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Alcohol Withdrawal & Delirium Tremens",
        "stem": (
            "In patients with chronic alcohol dependence presenting with severe hepatic cirrhosis (Child-Pugh Class C) "
            "and acute alcohol withdrawal syndrome, which group of benzodiazepines is safest to administer because they undergo direct "
            "glucuronidation without requiring hepatic cytochrome P450 oxidation?"
        ),
        "options": [
            ("Lorazepam, Oxazepam, and Temazepam ('LOT' drugs)", True, None),
            ("Diazepam and Chlordiazepoxide", False, "Diazepam and Chlordiazepoxide have long half-lives and active metabolites that accumulate dangerously in liver cirrhosis, causing prolonged sedation and hepatic coma."),
            ("Clonazepam and Alprazolam", False, "Both require extensive hepatic microsomal oxidative metabolism."),
            ("Midazolam and Flurazepam", False, "Both are metabolized via CYP3A4 and undergo impaired clearance in liver failure.")
        ],
        "pearl": "Benzodiazepines in Liver Disease: 'LOT' Mnemonic: Lorazepam, Oxazepam, Temazepam. These three BZDs undergo direct Phase II Glucuronide conjugation and have NO active oxidative metabolites. They do not accumulate in hepatic failure or in the elderly, making them the safest agents for alcohol withdrawal in cirrhotic patients.",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 28 (Psychopharmacology), p. 1120-1135.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Schizophrenia First-Rank Symptoms & Management",
        "stem": (
            "A 23-year-old engineering student is brought to the psychiatric clinic by his parents because of progressive social withdrawal, "
            "deteriorating academic performance, and bizarre behavior over the past 8 months. "
            "During the interview, the patient states that his thoughts are being sucked out of his head by an extraterrestrial radio antenna (thought withdrawal) "
            "and that he hears two distinct male voices discussing his private actions and arguing in the third person ('He is worthless, he should kill himself'). "
            "He firmly believes his arm movements are being physically controlled by an outside satellite beam (somatic passivity). "
            "Which of the following classical symptom groups described by Kurt Schneider are demonstrated in this clinical presentation?"
        ),
        "options": [
            ("Schneider's First-Rank Symptoms (FRS) of Schizophrenia", True, None),
            ("Bleuler's Fundamental 4 A's of Schizophrenia", False, "Bleuler's 4 A's are: Autism, Ambivalence, loosening of Associations, and Inappropriate/flat Affect."),
            ("Schneider's Second-Rank Symptoms", False, "Second-rank symptoms include other hallucinations, emotional blunting, and perplexity."),
            ("Catatonic stupor symptoms", False, "Catatonic symptoms include waxy flexibility, negativism, mutism, and echolalia.")
        ],
        "pearl": "Schneider's First-Rank Symptoms (FRS) of Schizophrenia: 11 Symptoms divided into: 1. Auditory Hallucinations: Voices discussing/arguing (3rd person) | Voices commenting on actions (running commentary) | Thought echo (Gedankenlautwerden). 2. Thought Interference: Thought insertion | Thought withdrawal | Thought broadcasting. 3. Passivity Phenomena: 'Made' feelings | 'Made' impulses | 'Made' volitional acts | Somatic passivity. 4. Delusional Perception: Normal perception interpreted with sudden private delusional meaning. Bleuler's 4 A's: Association loosening, Affective blunting, Autism, Ambivalence.",
        "citation": "Niraj Ahuja's A Short Textbook of Psychiatry, 8th Ed, Chapter 5 (Schizophrenia), p. 64-80.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Schizophrenia First-Rank Symptoms & Management",
        "stem": (
            "A 32-year-old male with treatment-resistant schizophrenia has failed sequential adequate therapeutic trials of Olanzapine and Risperidone. "
            "The psychiatrist decides to initiate Clozapine. What is the most catastrophic, potentially fatal hematological adverse effect of Clozapine "
            "that necessitates mandatory, regular baseline and ongoing monitoring of the Absolute Neutrophil Count (ANC)?"
        ),
        "options": [
            ("Agranulocytosis (severe neutropenia with ANC <500/uL)", True, None),
            ("Immune thrombocytopenic purpura (ITP)", False, "Clozapine does not typically cause isolated autoimmune destruction of platelets."),
            ("Aplastic anemia affecting all three cell lines simultaneously", False, "Clozapine selectively arrests neutrophil maturation in the bone marrow, producing agranulocytosis rather than pan-marrow aplasia."),
            ("Methemoglobinemia with chocolate-colored blood", False, "Methemoglobinemia is seen with Dapsone, Nitrites, and Prilocaine, not Clozapine.")
        ],
        "pearl": "Clozapine (Atypical Antipsychotic): Gold standard for TREATMENT-RESISTANT SCHIZOPHRENIA (failure of ≥2 antipsychotics) and suicidal behavior in schizophrenia. Unique features: Almost NO extrapyramidal symptoms (EPS) or tardive dyskinesia; DOES NOT raise prolactin. CRITICAL ADVERSE EFFECTS: 1. Agranulocytosis (1-2% risk; mandatory weekly ANC monitoring for 6 months, then biweekly for 6 months, then monthly) | 2. Myocarditis / Cardiomyopathy | 3. Severe weight gain, metabolic syndrome, and diabetes | 4. Lowers seizure threshold (highest dose-dependent seizure risk among antipsychotics) | 5. Sialorrhea (excessive drooling).",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 28, p. 1145-1156.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Bipolar Disorder & Lithium Therapy",
        "stem": (
            "A 28-year-old male is brought to the casualty by his family. For the past 10 days, he has been sleeping only 2 hours a night, "
            "talking incessantly in a loud, pressured voice, spending lavish amounts of borrowed money on luxury sports cars, "
            "and declaring that he has been appointed the secret Prime Minister of economic affairs (grandiose delusions). "
            "He is pacing restlessly and becomes irritable and belligerent when contradicted. "
            "What is the diagnosis, and what is the target therapeutic serum concentration range for Lithium Carbonate during acute manic stabilization?"
        ),
        "options": [
            ("Bipolar I Disorder, Current Episode Manic; 0.8 to 1.2 mEq/L", True, None),
            ("Major Depressive Disorder with psychotic features; 0.4 to 0.6 mEq/L", False, "This is acute mania with grandiosity and decreased need for sleep, not depression."),
            ("Cyclothymic disorder; 1.5 to 2.0 mEq/L", False, "1.5-2.0 mEq/L is in the toxic range for Lithium!"),
            ("Attention-Deficit Hyperactivity Disorder (ADHD); 0.2 to 0.4 mEq/L", False, "Acute episodic grandiosity, decreased need for sleep, and reckless spending in an adult indicate mania.")
        ],
        "pearl": "Lithium Carbonate in Bipolar Disorder: Gold standard mood stabilizer, reduces suicide risk. Therapeutic Serum Levels: ACUTE MANIA: 0.8 - 1.2 mEq/L | MAINTENANCE PROPHYLAXIS: 0.6 - 0.8 mEq/L | TOXICITY THRESHOLD: > 1.5 mEq/L (coarse tremors, ataxia, vomiting, confusion). Blood drawn 12 hours after the last bedtime dose (12-hour trough level). Long-term monitoring: Renal function (Nephrogenic Diabetes Insipidus) and Thyroid function (Hypothyroidism with goiter). Cardiac teratogenic effect: Ebstein's Anomaly (tricuspid valve downward displacement).",
        "citation": "Niraj Ahuja's A Short Textbook of Psychiatry, 8th Ed, Chapter 6 (Mood Disorders), p. 88-104.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Bipolar Disorder & Lithium Therapy",
        "stem": (
            "A 32-year-old female taking Lithium Carbonate for Bipolar Disorder is prescribed Hydrochlorothiazide and Indomethacin "
            "by her primary physician for hypertension and osteoarthritis. Three days later, she develops nausea, vomiting, coarse hand tremors, "
            "dysarthria, ataxia, and generalized drowsiness. What is the mechanism of this drug-drug interaction?"
        ),
        "options": [
            ("Thiazide diuretics and NSAIDs decrease renal clearance of Lithium in the proximal tubule, triggering acute Lithium toxicity", True, None),
            ("Indomethacin displaces Lithium from plasma albumin binding sites", False, "Lithium is NOT bound to plasma proteins at all (0% protein bound) and is excreted 100% unchanged in urine."),
            ("Hydrochlorothiazide directly stimulates dopamine receptors in the basal ganglia", False, "Hydrochlorothiazide acts on the Na+/Cl- cotransporter in the renal distal convoluted tubule."),
            ("Lithium accelerates hepatic breakdown of thiazides", False, "Lithium is not metabolized in the liver.")
        ],
        "pearl": "Lithium Drug Interactions: Drugs that INCREASE Lithium levels (cause toxicity): 1. Thiazide diuretics (decrease GFR and stimulate proximal tubular Na+ and Li+ reabsorption) | 2. NSAIDs (inhibit renal prostaglandins, decreasing renal clearance) | 3. ACE inhibitors / ARBs. Safe alternative for analgesia: Paracetamol / Acetaminophen (does NOT affect lithium excretion). Safe diuretic: Acetazolamide or Amiloride (used specifically to treat lithium-induced nephrogenic DI).",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 28, p. 1160-1172.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Major Depressive Disorder & SSRIs",
        "stem": (
            "A 36-year-old female presents with pervasive sadness of mood, crying spells, inability to experience pleasure in any activities (anhedonia), "
            "early morning awakening (2 hours before her alarm), marked loss of appetite with 5 kg weight loss, and recurrent feelings of worthlessness for the past 6 weeks. "
            "She expresses passive suicidal thoughts ('My family would be better off without me'). Physical and laboratory evaluations are normal. "
            "What is the first-line antidepressant class of choice, and what is the typical latency period before clinical therapeutic antidepressant improvement begins?"
        ),
        "options": [
            ("Selective Serotonin Reuptake Inhibitors (SSRIs, e.g., Escitalopram, Sertraline); 2 to 4 weeks", True, None),
            ("Tricyclic Antidepressants (TCAs, e.g., Amitriptyline); 24 to 48 hours", False, "TCAs have high anticholinergic and cardiac toxicity in overdose; no antidepressant works in 24-48 hours."),
            ("Monoamine Oxidase Inhibitors (MAOIs, e.g., Tranylcypromine); immediately within 6 hours", False, "MAOIs require strict dietary tyramine restriction to prevent hypertensive crisis and have a multi-week lag."),
            ("Electroconvulsive Therapy (ECT) as primary outpatient maintenance", False, "ECT is indicated for depression with acute suicidal intent, catatonia, or psychotic depression, not mild/moderate outpatient first-line.")
        ],
        "pearl": "Major Depressive Disorder (MDD): Diagnostic criteria (SIG E CAPS for ≥2 weeks): Sleep disturbances, Interest lost (Anhedonia), Guilt/Worthlessness, Energy loss/Fatigue, Concentration poor, Appetite/Weight changes, Psychomotor agitation/retardation, Suicidal ideation. FIRST-LINE DRUGS: SSRIs (Escitalopram, Sertraline, Fluoxetine). All antidepressants require a therapeutic lag of 2 to 4 WEEKS for down-regulation of inhibitory somatodendritic 5-HT1A autoreceptors to occur.",
        "citation": "Niraj Ahuja's A Short Textbook of Psychiatry, 8th Ed, Chapter 6, p. 94-102.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Obsessive-Compulsive Disorder",
        "stem": (
            "A 25-year-old software engineer presents with severe distress because he spends 4 hours every day repeatedly washing his hands with carbolic soap. "
            "He experiences recurrent, intrusive, distressing thoughts that his hands are contaminated with lethal microbes from touching doorknobs (obsession), "
            "which generates intense anxiety. The anxiety is temporarily relieved only after washing his hands exactly 12 times in a rigid ritual (compulsion). "
            "He recognizes that these thoughts originate from his own mind and are excessive and irrational (ego-dystonic with preserved insight). "
            "What is the first-line cognitive-behavioral psychotherapy and the first-line pharmacotherapy of choice for Obsessive-Compulsive Disorder (OCD)?"
        ),
        "options": [
            ("Exposure and Response Prevention (ERP); High-dose Selective Serotonin Reuptake Inhibitor (SSRI, e.g., Fluoxetine 60-80 mg/day or Sertraline 200 mg/day)", True, None),
            ("Classical Freudian psychoanalysis; Low-dose Diazepam PRN", False, "Psychoanalysis and benzodiazepines are ineffective for OCD; ERP is the evidence-based therapy."),
            ("Systematic desensitization; Haloperidol 10 mg daily", False, "Haloperidol is not first-line for OCD without tics."),
            ("Aversion therapy with electric shocks; Carbamazepine", False, "Aversion therapy is obsolete and unethical; anticonvulsants do not treat OCD.")
        ],
        "pearl": "Obsessive-Compulsive Disorder (OCD): Core features: Obsessions (intrusive, ego-dystonic thoughts/urges) -> Anxiety -> Compulsions (repetitive behaviors performed to neutralize anxiety). EGO-DYSTONIC (patient recognizes them as irrational, unlike delusions). FIRST-LINE PSYCHOTHERAPY: Exposure and Response Prevention (ERP, a form of CBT). FIRST-LINE DRUGS: High-dose SSRIs (Fluoxetine, Sertraline, Fluvoxamine, Paroxetine). Most effective TCA: Clomipramine (potent serotonin reuptake blocker). Note: OCD requires higher doses and longer duration (10-12 weeks) of SSRIs than depression!",
        "citation": "Niraj Ahuja's A Short Textbook of Psychiatry, 8th Ed, Chapter 7 (Neurotic Disorders), p. 116-124.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Opioid Toxicity & Naloxone",
        "stem": (
            "A 26-year-old male is brought unresponsive to the emergency department by his friends from a rave party. "
            "Physical examination reveals a Glasgow Coma Scale (GCS) score of 5, respiratory rate of 6 breaths/min with shallow breathing, "
            "cyanosis of the lips, blood pressure of 88/54 mmHg, and pinpoint, symmetrically constricted pupils (1 mm) that are non-reactive. "
            "Track marks from intravenous needle punctures are visible over both antecubital fossae. "
            "What is the immediate, life-saving competitive opioid receptor antagonist of choice, and what is its typical route and onset?"
        ),
        "options": [
            ("Intravenous Naloxone (0.4 to 2 mg titrated every 2-3 minutes)", True, None),
            ("Oral Naltrexone 50 mg daily", False, "Naltrexone is an orally active, long-acting opioid antagonist used for maintenance relapse prevention in detoxified patients; it has NO role in acute emergency overdose resuscitation!"),
            ("Intravenous Flumazenil 0.2 mg", False, "Flumazenil is a benzodiazepine antagonist, ineffective for opioid-induced respiratory depression."),
            ("Intramuscular Methadone 20 mg", False, "Methadone is a full opioid agonist and would cause fatal respiratory arrest in acute opioid overdose!")
        ],
        "pearl": "Opioid Overdose Classic Triad: 1. COMA / Altered mental status | 2. RESPIRATORY DEPRESSION (respiratory rate <8-10/min) | 3. PINPOINT PUPILS (Miosis). ANTIDOTE: NALOXONE (pure mu-opioid receptor competitive antagonist). Given IV, IM, or intranasal. Reverses respiratory depression within 1-2 minutes! CAUTION: Naloxone half-life is short (30-60 minutes); long-acting opioids (Methadone, slow-release morphine) outlast naloxone, leading to recurrent coma. Naltrexone is for maintenance relapse prevention in clean patients.",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 20 (Opioid Use Disorders), p. 810-822.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Panic Disorder & Agoraphobia",
        "stem": (
            "A 28-year-old female presents to the cardiac emergency room for the fourth time this month, convinced she is having a heart attack. "
            "She describes sudden, unprovoked episodes of intense terror that peak within 10 minutes, accompanied by palpitations, pounding heart, "
            "chest tightness, shortness of breath, paresthesias around her mouth, and a terrifying fear of impending doom or dying. "
            "Extensive cardiac evaluations (serial ECGs, high-sensitivity troponin, echocardiogram) are completely normal. "
            "Between attacks, she lives in constant, anticipatory dread of experiencing another attack, and has begun avoiding taking public buses or crowded malls. "
            "What is the diagnosis, and what is the treatment for acute panic attacks versus long-term maintenance prophylaxis?"
        ),
        "options": [
            ("Panic Disorder with Agoraphobia; Acute: Sublingual/oral Alprazolam or Clonazepam; Long-term: SSRIs (e.g., Sertraline) plus Cognitive Behavioral Therapy", True, None),
            ("Pheochromocytoma; Phenoxybenzamine and surgical adrenalectomy", False, "Pheochromocytoma causes episodic hypertension with headache, sweating, and tachycardia; urinary metanephrines are normal here."),
            ("Generalized Anxiety Disorder; Long-term Diazepam monotherapy", False, "GAD is chronic, continuous, non-episodic worry lasting >6 months without discrete 10-minute panic paroxysms."),
            ("Somatization disorder; High-dose Antipsychotics", False, "Somatization disorder features multiple unexplained physical symptoms over years, not discrete sudden panic surges with anticipatory avoidance.")
        ],
        "pearl": "Panic Disorder & Agoraphobia: Diagnostic features: Recurrent, unexpected Panic Attacks peaking within 10 minutes (Palpitations, Chest pain, Choking, Sweating, Trembling, Fear of dying / going crazy) + Anticipatory Anxiety (constant worry about next attack for >1 month) +/- Agoraphobia (avoidance of places where escape might be difficult, e.g. crowds, public transit). ACUTE ATTACK: Short-acting Benzodiazepines (Alprazolam 0.25-0.5 mg). LONG-TERM MAINTENANCE: SSRIs (Sertraline, Paroxetine) + CBT.",
        "citation": "Niraj Ahuja's A Short Textbook of Psychiatry, 8th Ed, Chapter 7, p. 108-115.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Post-Traumatic Stress Disorder (PTSD)",
        "stem": (
            "A 30-year-old soldier who survived an improvised explosive device (IED) blast in a combat zone 5 months ago "
            "presents with severe insomnia and recurrent, intrusive, vivid nightmares of the explosion. "
            "When he hears sudden loud noises like car backfires or thunder, he experiences terrifying flashbacks as if the explosion is recurring in the present moment, "
            "diving behind furniture in terror. He actively avoids television news and veterans' reunions, feels emotionally detached from his wife, "
            "and exhibits extreme hypervigilance and an exaggerated startle response. What is the diagnosis?"
        ),
        "options": [
            ("Post-Traumatic Stress Disorder (PTSD)", True, None),
            ("Acute Stress Disorder (ASD)", False, "Acute Stress Disorder symptoms occur within 1 month of the trauma and last between 3 days and 1 month; beyond 1 month, it is diagnosed as PTSD."),
            ("Adjustment Disorder", False, "Adjustment disorder occurs within 3 months of an ordinary psychosocial stressor (e.g., divorce, job loss), not catastrophic life-threatening trauma."),
            ("Malingering", False, "Malingering is conscious fabrication of symptoms for external secondary gain (money, avoiding duty).")
        ],
        "pearl": "PTSD vs Acute Stress Disorder: Trigger: Exposure to actual or threatened death, serious injury, or sexual violence. Core Symptom Clusters (≥1 month for PTSD): 1. Intrusive re-experiencing (Flashbacks, Nightmares) | 2. Avoidance of trauma-related stimuli | 3. Negative alterations in cognition and mood (emotional detachment, amnesia) | 4. Hyperarousal (Hypervigilance, exaggerated startle, insomnia). TIMELINE RULE: Symptoms 3 days to 1 month = ACUTE STRESS DISORDER. Symptoms > 1 month = POST-TRAUMATIC STRESS DISORDER (PTSD). First-line treatment: Trauma-focused CBT / EMDR + SSRIs (Sertraline, Paroxetine). Prazosin (alpha-1 blocker) reduces PTSD nightmares!",
        "citation": "Kaplan & Sadock's Synopsis of Psychiatry, 12th Ed, Chapter 11 (Trauma- and Stressor-Related Disorders), p. 430-442.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Delirium vs Dementia Differential",
        "stem": (
            "A 76-year-old male with mild, stable vascular dementia is admitted to the hospital with a urinary tract infection (UTI). "
            "Over the past 24 hours, he has become acutely confused, picking at his intravenous lines, and experiencing fluctuating consciousness, "
            "being drowsy and unarousable at noon but agitated, hallucinating, and screaming at night ('sundowning'). "
            "On examination, his attention span is severely impaired, and he is unable to perform serial 7 subtractions or name the months backward. "
            "Which of the following clinical features is the single most important hallmark that differentiates Delirium from Dementia?"
        ),
        "options": [
            ("Acute onset with fluctuating course and prominent disturbance of Attention and Awareness", True, None),
            ("Gradual, insidious progressive loss of recent memory with clear consciousness", False, "Insidious loss of memory with intact attention and clear consciousness is the hallmark of Dementia."),
            ("Presence of prominent cortical dysphasia and apraxia", False, "Dysphasia and apraxia are focal cortical signs seen in Alzheimer's and vascular dementia."),
            ("Permanent irreversible cognitive decline", False, "Delirium is acutely reversible once the underlying systemic cause (e.g., UTI, sepsis, electrolyte imbalance) is treated.")
        ],
        "pearl": "Delirium vs Dementia: DELIRIUM (Acute Brain Failure): 1. Acute onset (hours to days) | 2. FLUCTUATING course (worse at night / sundowning) | 3. IMPAIRED ATTENTION AND CONSCIOUSNESS (hallmark!) | 4. Visual hallucinations common | 5. Reversible once underlying medical cause is treated. DEMENTIA: 1. Insidious, chronic onset (months to years) | 2. Progressive, stable course | 3. CLEAR CONSCIOUSNESS and normal attention until late stages | 4. Memory impairment (recent > remote) is primary feature | 5. Usually irreversible.",
        "citation": "Niraj Ahuja's A Short Textbook of Psychiatry, 8th Ed, Chapter 3 (Organic Mental Disorders), p. 34-46.",
        "difficulty": "easy"
    }
]
