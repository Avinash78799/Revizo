"""
Supplementary High-Yield NEET-PG Clinical Questions
Brings every subject in neet_pg.db to 20-25 authentic, deduplicated clinical questions.
"""

SUPPLEMENTARY_QUESTIONS = [
    # --- ANESTHESIOLOGY (6 questions) ---
    {
        "subject": "Anesthesiology",
        "concept_name": "Core Principles: Intravenous Anesthetic Agents: Propofol & Ketamine",
        "stem": (
            "A 72-year-old male with severe coronary artery disease and an LVEF of 25% is scheduled for emergency bowel resection. "
            "Which intravenous anesthetic induction agent is renowned for producing the most exceptional hemodynamically stable profile "
            "(minimal change in heart rate, blood pressure, and cardiac output), but causes transient adrenal cortical suppression "
            "via reversible inhibition of the 11-beta-hydroxylase enzyme?"
        ),
        "options": [
            ("Etomidate", True, None),
            ("Propofol", False, "Propofol causes significant vasodilation and myocardial depression, precipitating hypotension in cardiogenic compromise."),
            ("Ketamine", False, "Ketamine increases myocardial oxygen consumption and is avoided in severe coronary ischemia."),
            ("Thiopental", False, "Thiopental causes peripheral venous pooling and negative inotropy.")
        ],
        "pearl": "Etomidate Clinical Pearls: Premier induction agent for patients with severe CARDIAC COMPROMISE (hypotension, heart failure, shock) because it maintains hemodynamic stability. Critical Adverse Effect: Causes dose-dependent, transient ADRENAL SUPPRESSION by inhibiting 11-beta-hydroxylase (blocking conversion of 11-deoxycortisol to cortisol). Also has high incidence of myoclonus (prevented by prior opioid/fentanyl administration) and postoperative nausea/vomiting.",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 29, p. 790-798.",
        "difficulty": "moderate"
    },
    {
        "subject": "Anesthesiology",
        "concept_name": "Core Principles: Mallampati Classification & Difficult Airway Algorithm",
        "stem": (
            "A 34-year-old male with end-stage renal disease (ESRD) and severe hepatic cirrhosis is scheduled for surgery. "
            "Which non-depolarizing neuromuscular blocking drug is the muscle relaxant of choice in patients with combined renal and liver failure, "
            "because it undergoes spontaneous, non-enzymatic chemical degradation at physiological body temperature and pH (Hofmann Elimination)?"
        ),
        "options": [
            ("Cisatracurium (or Atracurium)", True, None),
            ("Pancuronium", False, "Pancuronium is eliminated 85% by the kidneys; accumulates in renal failure producing prolonged paralysis."),
            ("Vecuronium", False, "Vecuronium is eliminated predominantly by hepatic biliary excretion (40-60%) and kidneys (30%)."),
            ("Rocuronium", False, "Rocuronium is primarily eliminated by the liver into bile (>70%).")
        ],
        "pearl": "Hofmann Elimination (Organ-Independent Clearance): Atracurium and Cisatracurium do NOT depend on liver or kidneys for metabolism. They undergo spontaneous non-enzymatic chemical cleavage at normal body temperature (37°C) and pH (7.4) = HOFMANN ELIMINATION + ester hydrolysis by non-specific plasma esterases. Drug of choice in: RENAL FAILURE AND HEPATIC FAILURE! Metabolite of Atracurium: Laudanosine (can cross BBB and trigger seizures at high doses; Cisatracurium produces 5-fold less laudanosine).",
        "citation": "Morgan & Mikhail's Clinical Anesthesiology, 7th Ed, Chapter 11, p. 222-230.",
        "difficulty": "easy"
    },
    {
        "subject": "Anesthesiology",
        "concept_name": "Core Principles: Malignant Hyperthermia Diagnosis & Dantrolene",
        "stem": (
            "At the conclusion of a 2-hour surgery under general anesthesia with Rocuronium muscle relaxation, "
            "the patient has profound residual neuromuscular blockade (Train-of-Four count 0/4). "
            "Which novel selective cyclodextrin-based relaxant-binding agent can be administered to instantaneously encapsulate "
            "and reverse deep Rocuronium-induced neuromuscular blockade within 2 to 3 minutes without requiring anticholinesterases?"
        ),
        "options": [
            ("Sugammadex (modified gamma-cyclodextrin)", True, None),
            ("Neostigmine combined with Glycopyrrolate", False, "Neostigmine cannot reverse deep block (TOF 0/4) and requires at least 1-2 twitches before administration to avoid recurarization."),
            ("Physostigmine", False, "Physostigmine is used for central anticholinergic syndrome, not for neuromuscular block reversal."),
            ("Edrophonium", False, "Edrophonium is a short-acting anticholinesterase ineffective for deep neuromuscular blockade.")
        ],
        "pearl": "Sugammadex: A modified gamma-cyclodextrin that encapsulates Aminosteroid neuromuscular blockers (ROCURONIUM >> Vecuronium) in a 1:1 tight molecular complex in plasma, inactivating them directly. Advantages: Reverses even PROFOUND / DEEP neuromuscular blockade (TOF 0) within 2-3 minutes! Avoids all muscarinic side effects of neostigmine (bradycardia, bronchospasm, secretions). Note: Ineffective against benzylisoquinolines (Atracurium/Cisatracurium).",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 34, p. 940-952.",
        "difficulty": "easy"
    },
    {
        "subject": "Anesthesiology",
        "concept_name": "Core Principles: Minimum Alveolar Concentration (MAC) & Potency",
        "stem": (
            "A 28-year-old male with a documented genetic atypical variant of Pseudocholinesterase (Butyrylcholinesterase) "
            "is administered Succinylcholine (1.5 mg/kg) for rapid sequence intubation. "
            "Instead of recovering normal spontaneous breathing in 5 to 10 minutes, the patient remains completely apneic and paralyzed "
            "for 4 hours ('Suxamethonium Apnea'). What laboratory test on plasma confirms the presence of homozygous atypical pseudocholinesterase?"
        ),
        "options": [
            ("Dibucaine Number test (abnormally low Dibucaine Number: ~20% in atypical homozygotes vs normal >80%)", True, None),
            ("Eserine Number test", False, "Eserine is not the standard clinical assay for atypical pseudocholinesterase."),
            ("Fluoride Number test for organophosphates", False, "Fluoride number identifies fluoride-resistant variants, but Dibucaine is the standard test for classic atypical pseudocholinesterase."),
            ("Serum Creatine Kinase-MM level", False, "Serum CK reflects rhabdomyolysis, not plasma enzyme inhibition kinetics.")
        ],
        "pearl": "Succinylcholine Apnea & Dibucaine Number: Succinylcholine (SCh) is normally rapidly hydrolyzed in plasma by Pseudocholinesterase (Butyrylcholinesterase / BChE) within 5-10 minutes. In patients with atypical pseudocholinesterase gene (E1a mutation): SCh is not degraded -> prolonged apnea lasting 3-6 hours. DIBUCAINE NUMBER TEST: Dibucaine (local anesthetic) inhibits normal pseudocholinesterase by >80% (Normal Dibucaine Number = 80). In homozygous atypical variants, dibucaine inhibits enzyme by only 20% (Atypical Dibucaine Number = 20). Heterozygotes = 50-60. Management of Sux Apnea: Continue mechanical ventilation until spontaneous recovery occurs; fresh frozen plasma (FFP) can provide normal enzyme.",
        "citation": "Morgan & Mikhail, 7th Ed, Chapter 11, p. 210-218.",
        "difficulty": "hard"
    },
    {
        "subject": "Anesthesiology",
        "concept_name": "Core Principles: Local Anesthetic Systemic Toxicity (LAST) & Lipid Emulsion",
        "stem": (
            "When comparing the enantiomers of the local anesthetic Bupivacaine, Ropivacaine (the pure S-(-) enantiomer) "
            "was developed to improve the therapeutic safety index. What is the key clinical advantage of Ropivacaine over racemic Bupivacaine?"
        ),
        "options": [
            ("Significantly lower cardiotoxicity (lower risk of lethal ventricular arrhythmias and refractory cardiac arrest) and greater sensory-motor differentiation", True, None),
            ("Longer duration of action by 48 hours", False, "Duration of action is comparable to bupivacaine."),
            ("Zero requirement for sodium bicarbonate buffering", False, "Both can be buffered similarly."),
            ("Completely devoid of CNS toxicity", False, "Ropivacaine can still cause CNS toxicity at high doses, but has significantly less cardiac depression.")
        ],
        "pearl": "Ropivacaine vs Bupivacaine: Bupivacaine is a racemic mixture of R-(+) and S-(-) enantiomers; the R-(+) isomer binds tightly to cardiac voltage-gated Na+ channels and dissociates very slowly during diastole, causing fatal ventricular fibrillation. ROPIVACAINE is the pure S-(-) enantiomer (levorotatory). It has significantly LESS CARDIOTOXICITY and produces less motor blockade with equivalent sensory analgesia, making it ideal for labor epidurals and peripheral nerve blocks.",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 36, p. 1020-1035.",
        "difficulty": "moderate"
    },
    {
        "subject": "Anesthesiology",
        "concept_name": "Core Principles: Spinal vs Epidural Anesthesia Differences",
        "stem": (
            "A 42-year-old non-smoking female undergoing laparoscopic hysterectomy has an Apfel score of 4 for Postoperative Nausea and Vomiting (PONV) "
            "(Female gender, Non-smoker, History of motion sickness, Postoperative opioid use). "
            "According to international consensus guidelines for patients at high risk of PONV (>70% risk), "
            "which multimodal prophylactic antiemetic combination is recommended at induction and emergence?"
        ),
        "options": [
            ("Intravenous Dexamethasone (4-8 mg at induction) combined with a 5-HT3 antagonist (Ondansetron 4 mg at emergence) plus TIVA using Propofol", True, None),
            ("Oral Metoclopramide 10 mg alone 2 hours before surgery", False, "Metoclopramide monotherapy is weak and ineffective in high-risk Apfel score 4 patients."),
            ("Intravenous Promethazine 50 mg alone at emergence", False, "Promethazine causes severe postoperative sedation and has high extrapyramidal risk."),
            ("Inhalational Sevoflurane maintenance without antiemetics", False, "Volatile anesthetics are a major trigger for PONV; TIVA with propofol is preferred in high-risk patients.")
        ],
        "pearl": "Apfel Simplified PONV Score: 4 Risk Factors: 1. Female gender | 2. Non-smoker | 3. History of PONV or Motion Sickness | 4. Postoperative Opioids. Risk: 0 = 10%, 1 = 20%, 2 = 40%, 3 = 60%, 4 = 80%. High-risk prophylaxis: 1. Total Intravenous Anesthesia (TIVA with Propofol avoids volatile triggers) | 2. Dexamethasone 4-8 mg IV given at INDUCTION | 3. Ondansetron 4 mg IV given at END OF SURGERY / emergence. Multimodal combination reduces PONV from 80% to <20%.",
        "citation": "Fourth Consensus Guidelines for the Management of Postoperative Nausea and Vomiting (2020) / Miller's Ch 86.",
        "difficulty": "moderate"
    },

    # --- ORTHOPEDICS (6 questions) ---
    {
        "subject": "Orthopedics",
        "concept_name": "Core Principles: Upper Limb Fractures (Colles, Smith, Galeazzi, Monteggia)",
        "stem": (
            "A 6-year-old boy falls from a playground monkey bar onto his outstretched hand and presents with severe elbow swelling, "
            "pain, and S-shaped posterior displacement of the elbow. Plain radiographs confirm a displaced Extension-type Supracondylar Fracture "
            "of the humerus (Gartland Stage III). The brachial artery and median nerve are tented over the sharp proximal bone spike. "
            "Which specific branch of the median nerve is most commonly injured in extension-type supracondylar fractures, "
            "tested clinically by asking the child to make the 'OK' sign (pincer pinch of thumb and index distal phalanges)?"
        ),
        "options": [
            ("Anterior Interosseous Nerve (AIN)", True, None),
            ("Posterior Interosseous Nerve (PIN)", False, "PIN is a branch of the radial nerve injured in Monteggia fracture-dislocations."),
            ("Recurrent motor branch of median nerve", False, "Recurrent motor branch innervates thenar muscles in the palm, injured in carpal tunnel lacerations."),
            ("Superficial radial sensory nerve", False, "Superficial radial nerve is purely sensory to the anatomical snuffbox.")
        ],
        "pearl": "Supracondylar Humerus Fractures Pearls: Most common pediatric elbow fracture (peak age 5-8 yrs). Mechanism: Fall on outstretched hand with elbow hyperextended -> EXTENSION TYPE (95-98%; distal fragment displaced posteriorly). NERVE AT RISK: ANTERIOR INTEROSSEOUS NERVE (AIN, motor branch of median nerve). Clinical Test: 'OK Sign' (tests Flexor Pollicis Longus & Flexor Digitorum Profundus to index finger; failure to make a round 'O' -> pulp-to-pulp pinch). In flexion-type supracondylar fractures (distal fragment displaced anteriorly): ULNAR NERVE is at risk.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 6, p. 86-96.",
        "difficulty": "easy"
    },
    {
        "subject": "Orthopedics",
        "concept_name": "Core Principles: Hip Fractures: Intracapsular vs Extracapsular",
        "stem": (
            "A 13-year-old obese adolescent male presents with a 3-month history of a dull, aching pain in his right KNEE and a painless limp. "
            "Examination of the right knee is completely normal with full range of motion. "
            "However, examination of the right HIP demonstrates obligate EXTERNAL ROTATION when the hip is passively flexed. "
            "Anteroposterior and frog-leg lateral radiographs of the pelvis confirm Slipped Capital Femoral Epiphysis (SCFE). "
            "Which radiological line drawn along the superior border of the femoral neck normally intersects the lateral aspect of the femoral epiphysis, "
            "but fails to intersect it in SCFE (Trethowan's Sign)?"
        ),
        "options": [
            ("Klein's Line", True, None),
            ("Shenton's Line", False, "Shenton's line is a smooth continuous arc along the inferior border of the femoral neck and superior obturator margin, disrupted in hip dislocation or neck fractures."),
            ("Perkins' Line", False, "Perkins' line is a vertical line through the lateral acetabular margin used in Developmental Dysplasia of the Hip (DDH)."),
            ("Hilgenreiner's Line", False, "Hilgenreiner's line is a horizontal line through the triradiate cartilages in DDH.")
        ],
        "pearl": "Slipped Capital Femoral Epiphysis (SCFE): Classic demographic: Obese adolescent boy (11-15 yrs). Pitfall: REFERRED PAIN TO THE KNEE (via obturator nerve) leads to missed hip diagnosis! Physical exam hallmark: External rotation of limb during passive hip flexion. Radiology: KLEIN'S LINE: A line drawn along the superior margin of the femoral neck on AP view normally cuts through the lateral femoral epiphysis. In SCFE, it FAILS TO INTERSECT THE EPIPHYSIS = TRETHOWAN'S SIGN. Treatment: Urgent in-situ single cannulated screw fixation.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 22 (Pediatric Orthopaedics), p. 250-258.",
        "difficulty": "moderate"
    },
    {
        "subject": "Orthopedics",
        "concept_name": "Core Principles: Hip Fractures: Intracapsular vs Extracapsular",
        "stem": (
            "A 2-week-old female infant born by breech delivery undergoes routine neonatal screening for Developmental Dysplasia of the Hip (DDH). "
            "On physical examination, the examiner flexes the infant's hips to 90 degrees and gently adducts the thighs while applying backward pressure, "
            "causing the femoral head to dislocate posteriorly out of the acetabulum with a palpable clunk. "
            "Subsequent abduction of the hip with anterior traction reduces the femoral head back into the acetabulum with a distinct tactile 'clunk'. "
            "What are the names of these two classic clinical diagnostic provocative maneuvers, respectively?"
        ),
        "options": [
            ("Barlow's Test (provocative dislocation) and Ortolani's Test (reduction of dislocated hip)", True, None),
            ("Ortolani's Test for dislocation and Barlow's Test for reduction", False, "Barlow dislocates the unstable hip (Barlow = Backwards); Ortolani reduces it back with abduction (Ortolani = Out)."),
            ("Trendelenburg's Test and Thomas's Test", False, "Trendelenburg tests abductor mechanism; Thomas tests fixed flexion deformity of hip."),
            ("Galeazzi's Test and Patrick's (FABER) Test", False, "Galeazzi tests apparent femoral shortening; FABER tests sacroiliac pathology.")
        ],
        "pearl": "DDH Clinical Tests: 1. BARLOW'S TEST: Hip flexed 90°, adducted, posterior pressure applied -> DISLOCATES an unstable hip ('Barlow dislocates'). 2. ORTOLANI'S TEST: Abduction of flexed hip with gentle forward lift on greater trochanter -> REDUCES the dislocated hip with a palpable 'clunk' ('Ortolani reduces / Outward'). Galeazzi (Allis) Sign: Unequal knee heights when hips and knees are flexed 90° supine. Gold Standard Screening <6 months: ULTRASOUND (Graf classification). First-line treatment <6 months: PAVLIK HARNESS.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 20 (Congenital Deformities), p. 222-234.",
        "difficulty": "easy"
    },
    {
        "subject": "Orthopedics",
        "concept_name": "Core Principles: Compartment Syndrome Diagnosis & Fasciotomy",
        "stem": (
            "A 42-year-old tennis player presents with severe pain over the lateral aspect of his right elbow that worsens "
            "when playing backhand shots or lifting a heavy briefcase. On physical examination, there is point tenderness "
            "over the lateral epicondyle, and pain is sharply exacerbated by RESISTED WRIST EXTENSION with the elbow fully extended (Cozen's Test). "
            "Which tendon origin is primarily degenerated (angiofibroblastic tendinosis) in Tennis Elbow (Lateral Epicondylitis)?"
        ),
        "options": [
            ("Extensor Carpi Radialis Brevis (ECRB)", True, None),
            ("Flexor Carpi Radialis (FCR)", False, "FCR is involved in Golfer's Elbow (Medial Epicondylitis), aggravated by resisted wrist flexion."),
            ("Pronator Teres", False, "Pronator teres is involved in medial epicondylitis or pronator syndrome."),
            ("Extensor Digitorum Longus", False, "ECRB is the primary tendon undergoing microtears and mucoid degeneration at the lateral epicondyle.")
        ],
        "pearl": "Lateral vs Medial Epicondylitis: 1. TENNIS ELBOW (Lateral Epicondylitis): Pathology: Microtears and angiofibroblastic tendinosis at the common extensor origin, specifically EXTENSOR CARPI RADIALIS BREVIS (ECRB). Pain exacerbated by: Resisted wrist extension with elbow straight (Cozen's test) and resisted middle finger extension (Maudsley's test). 2. GOLFER'S ELBOW (Medial Epicondylitis): Common flexor origin (Pronator Teres and Flexor Carpi Radialis). Pain on resisted wrist flexion and pronation.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 27, p. 320-324.",
        "difficulty": "easy"
    },
    {
        "subject": "Orthopedics",
        "concept_name": "Core Principles: Acute Osteomyelitis in Children",
        "stem": (
            "A 28-year-old construction worker presents with chronic dull aching pain in his right mid-tibia for 6 months. "
            "The pain is characteristically WORSE AT NIGHT and is DRAMATICALLY AND COMPLETELY RELIEVED by low-dose Aspirin or NSAIDs within 20 minutes. "
            "Plain radiograph of the tibia demonstrates a small, round radiolucent nidus (<1 cm) surrounded by an intense zone of dense, reactive cortical sclerosis. "
            "What is the diagnosis, and why does Aspirin provide such dramatic symptomatic relief?"
        ),
        "options": [
            ("Osteoid Osteoma; High concentrations of Prostaglandin E2 (PGE2) synthesized within the central vascular nidus are inhibited by NSAIDs", True, None),
            ("Osteoblastoma; Direct suppression of alkaline phosphatase by salicylates", False, "Osteoblastoma is larger (>2 cm), typically in the spine, and does NOT respond dramatically to aspirin."),
            ("Brodie's Abscess (subacute osteomyelitis); Antibacterial effect of aspirin", False, "Brodie's abscess is an intramedullary lucency surrounded by sclerosis, but is an infection, not dramatically relieved by aspirin."),
            ("Eosinophilic Granuloma; Histiocyte apoptosis", False, "Eosinophilic granuloma is Langerhans cell histiocytosis with punched-out lytic lesions.")
        ],
        "pearl": "Osteoid Osteoma: Benign osteoblastic bone tumor. Classic triad: 1. Age 10-25 yrs, male > female | 2. PAIN WORSE AT NIGHT | 3. DRAMATIC RELIEF WITH ASPIRIN / NSAIDs (pathognomonic!). Radiology: Radiolucent NIDUS <1.5 cm diameter surrounded by dense, fusiform cortical sclerosis. Pathology: The vascular nidus produces massive amounts of Prostaglandins (PGE2 and PGI2), stimulating local nerve fibers. CT scan is the imaging modality of choice. Definitive treatment: CT-guided Radiofrequency Ablation (RFA) or surgical excision of nidus.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 24 (Bone Tumours), p. 280-284.",
        "difficulty": "moderate"
    },
    {
        "subject": "Orthopedics",
        "concept_name": "Core Principles: Tuberculosis of Spine (Pott's Disease)",
        "stem": (
            "A 26-year-old athlete twists his knee during a soccer match and presents with joint line tenderness, "
            "recurrent painful knee 'locking' (inability to fully extend the knee), and sensation of giving way. "
            "On physical examination, McMurray's test produces an audible and palpable 'thud' / click along the medial joint line "
            "when the externally rotated flexed knee is brought into extension. "
            "What type of tear of the Medial Meniscus is classically responsible for true mechanical locking of the knee joint?"
        ),
        "options": [
            ("Bucket-handle tear with central displacement of the inner fragment into the intercondylar notch", True, None),
            ("Radial horizontal cleavage tear of the posterior horn", False, "Horizontal tears cause pain and clicking, but do not mechanically block terminal extension."),
            ("Flap (parrot-beak) tear of the anterior horn", False, "Parrot-beak tears cause transient catches, but bucket-handle tears cause persistent mechanical locking."),
            ("Meniscal cyst of the lateral meniscus", False, "Meniscal cysts present as a firm swelling at the lateral joint line that becomes prominent in extension.")
        ],
        "pearl": "Meniscal Tears & Knee Locking: Medial Meniscus is injured 3 times more frequently than Lateral Meniscus (because it is firmly anchored to the deep medial collateral ligament and joint capsule, making it less mobile). Mechanical Knee Locking: Pathognomonic for BUCKET-HANDLE TEAR (longitudinal tear where the inner fragment flips centrally into the intercondylar notch, blocking the femoral condyle from completing terminal extension). Diagnostic Tests: McMurray's test & Apley's grinding test. Gold standard imaging: MRI (T2-weighted sagittal view shows absent bow-tie sign). Treatment: Arthroscopic meniscal repair or partial meniscectomy.",
        "citation": "Apley & Solomon's System of Orthopaedics, 10th Ed, Chapter 28 (The Knee), p. 860-872.",
        "difficulty": "easy"
    },

    # --- OTORHINOLARYNGOLOGY (ENT) (6 questions) ---
    {
        "subject": "Otorhinolaryngology (ENT)",
        "concept_name": "Core Principles: Chronic Suppurative Otitis Media (CSOM) Variants",
        "stem": (
            "A 32-year-old male with chronic atticoantral CSOM presents with high fever, vomiting, severe deep retro-orbital pain, "
            "and horizontal diplopia on looking to the affected side. Physical examination reveals complete lateral gaze paralysis "
            "(sixth cranial nerve / abducens nerve palsy) on the ipsilateral side. "
            "What eponymous triad of Petrous Apicitis (Gradenigo's Syndrome) is demonstrated in this patient?"
        ),
        "options": [
            ("Otorrhea (CSOM) + Retro-orbital pain (Trigeminal nerve involvement) + Abducens nerve (CN VI) palsy", True, None),
            ("Conductive hearing loss + Schwartze sign + Paracusis Willisii", False, "This is the clinical picture of active Otosclerosis."),
            ("Vertigo + SNHL + Tinnitus", False, "This is Meniere's disease triad."),
            ("Facial nerve palsy + Vesicles in concha + Severe earache", False, "This is Ramsay Hunt Syndrome (Herpes Zoster Oticus).")
        ],
        "pearl": "Gradenigo's Syndrome (Petrous Apicitis Triad): Complication of atticoantral CSOM spreading to the petrous apex (Dorello's canal): 1. Persistent Otorrhea (middle ear discharge) | 2. Severe Retro-orbital or Facial Pain (Trigeminal nerve CN V involvement at Meckel's cave) | 3. Lateral Rectus / Abducens Palsy (CN VI paralysis in Dorello's canal causing diplopia on lateral gaze). Urgent management: High-resolution CT + IV antibiotics + Radical Mastoidectomy with Petrous Apicectomy.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 12 (Complications of CSOM), p. 94-102.",
        "difficulty": "moderate"
    },
    {
        "subject": "Otorhinolaryngology (ENT)",
        "concept_name": "Core Principles: Chronic Suppurative Otitis Media (CSOM) Variants",
        "stem": (
            "A 70-year-old diabetic male presents with excruciating, deep, agonizing nocturnal earache (otalgia) refractory to analgesics, "
            "purulent otorrhea, and progressive ipsilateral facial nerve paralysis. "
            "Otoscopic examination reveals red, fleshy granulation tissue at the bony-cartilaginous junction of the external auditory canal floor. "
            "What is the diagnosis, and what is the typical causative organism responsible for Malignant (Necrotizing) Otitis Externa?"
        ),
        "options": [
            ("Malignant Otitis Externa; Pseudomonas aeruginosa", True, None),
            ("Squamous cell carcinoma of middle ear; Human Papillomavirus", False, "Carcinoma of middle ear mimics MOE with granulations, but Pseudomonas in elderly diabetics is the classic necrotizing infection."),
            ("Aspergillus otomycosis; Aspergillus niger", False, "Otomycosis causes pruritus and blotting-paper debris, not severe cranial nerve palsies and osteomyelitis."),
            ("Ramsay Hunt syndrome; Varicella Zoster Virus", False, "Ramsay Hunt features herpetic vesicles in the concha and antihelix, not skull base osteomyelitis.")
        ],
        "pearl": "Malignant (Necrotizing) Otitis Externa: Life-threatening osteomyelitis of the temporal bone and skull base occurring in ELDERLY DIABETICS or immunocompromised patients. Causative organism: PSEUDOMONAS AERUGINOSA (>95%). Hallmark: Granulation tissue at the junction of cartilaginous and bony external canal (Fissures of Santorini). Complication: Multiple lower cranial nerve palsies (CN VII earliest, followed by IX, X, XI, XII at jugular foramen). Imaging: Technetium-99m scan for diagnosis; Gallium-67 scan for monitoring therapeutic cure. Treatment: Long-term IV anti-pseudomonal antibiotics (Ciprofloxacin, Ceftazidime, Meropenem) for 6-8 weeks.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 7 (Diseases of External Ear), p. 54-60.",
        "difficulty": "easy"
    },
    {
        "subject": "Otorhinolaryngology (ENT)",
        "concept_name": "Core Principles: Epistaxis: Little's Area & Management",
        "stem": (
            "A 28-year-old male presents with recurrent, severe, bright red epistaxis from his right nostril. "
            "Physical examination reveals multiple tiny, punctate, blanching telangiectasias on his lips, tongue, oral mucosa, and fingertips. "
            "His mother and brother also suffer from chronic recurrent nosebleeds and iron deficiency anemia. "
            "What is this autosomal dominant vascular dysplasia (Osler-Weber-Rendu Syndrome)?"
        ),
        "options": [
            ("Hereditary Hemorrhagic Telangiectasia (HHT)", True, None),
            ("Wegener's Granulomatosis (Granulomatosis with Polyangiitis)", False, "GPA features necrotizing granulomas of the respiratory tract, glomerulonephritis, and c-ANCA."),
            ("Henoch-Schonlein Purpura", False, "HSP features palpable purpura, abdominal pain, arthralgia, and IgA nephropathy in children."),
            ("Churg-Strauss Syndrome", False, "EGPA features asthma, eosinophilia, and p-ANCA vasculitis.")
        ],
        "pearl": "Hereditary Hemorrhagic Telangiectasia (HHT / Osler-Weber-Rendu Disease): Autosomal dominant disorder characterized by widespread arteriovenous malformations (AVMs) and telangiectasias lacking muscular elastic walls. Diagnostic Triad: 1. Recurrent spontaneous EPISTAXIS | 2. Multiple mucocutaneous telangiectasias (lips, tongue, oral mucosa, fingers) | 3. Visceral AVMs (Pulmonary AVMs -> right-to-left shunt, paradoxical brain abscesses; Hepatic AVMs). Management: Estrogen-progesterone therapy, KTP laser photocoagulation, Septodermoplasty (Saunders operation replacing septal mucosa with split-skin graft).",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 24, p. 184-186.",
        "difficulty": "moderate"
    },
    {
        "subject": "Otorhinolaryngology (ENT)",
        "concept_name": "Core Principles: Epistaxis: Little's Area & Management",
        "stem": (
            "A 22-year-old male from a rural farming village in coastal Odisha presents with recurrent epistaxis "
            "and a friable, painless, pedunculated, reddish-purple mass in his right nasal cavity resembling a 'strawberry' or 'mulberry'. "
            "Inspection under light reveals multiple white dots on the surface (sporangia). "
            "Histopathological examination of a biopsy specimen reveals thick-walled, round SPORANGIA filled with thousands of tiny SPORANGIOSPORES. "
            "What is the causative microbiological agent of Rhinosporidiosis?"
        ),
        "options": [
            ("Rhinosporidium seeberi (an aquatic mesomycetozoean protist parasite)", True, None),
            ("Klebsiella rhinoscleromatis", False, "K. rhinoscleromatis causes Rhinoscleroma, featuring Mikulicz cells and Russell bodies, not sporangia."),
            ("Mycobacterium leprae", False, "Leprosy causes lepromatous mucosal nodules with acid-fast bacilli in globi."),
            ("Leishmania braziliensis", False, "Mucocutaneous leishmaniasis causes destructive granulomatous ulceration (espundia).")
        ],
        "pearl": "Rhinosporidiosis: Caused by RHINOSPORIDIUM SEEBERI (classified under Mesomycetozoea, an aquatic protistan fish parasite). Endemic in India (Tamil Nadu, Kerala, Odisha) and Sri Lanka; associated with bathing in public ponds and rivers. Clinical: Friable, vascular, bleeding polypoid mass in nasal cavity with a 'STRAWBERRY' / MULBERRY appearance (white dots on surface = mature sporangia). Histopathology: Large round sporangia (100-300 um) filled with endospores. Treatment: Wide surgical excision with electrocautery of the base + oral Dapsone (prevents recurrences).",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 23 (Granulomatous Diseases of Nose), p. 172-176.",
        "difficulty": "easy"
    },
    {
        "subject": "Otorhinolaryngology (ENT)",
        "concept_name": "Core Principles: Otosclerosis & Carhart's Notch",
        "stem": (
            "A 74-year-old male presents with gradual, progressive, bilateral hearing loss. "
            "He complains that while he can hear people speaking in quiet rooms, he has immense difficulty understanding words "
            "in noisy social gatherings ('I can hear, but I cannot understand speech'). "
            "Pure-tone audiometry demonstrates symmetrical, gently sloping high-frequency Sensorineural Hearing Loss (SNHL) in both ears. "
            "What is this age-related degeneration of the cochlea (Presbycusis)?"
        ),
        "options": [
            ("Sensory / Neural Presbycusis", True, None),
            ("Bilateral Otosclerosis", False, "Otosclerosis causes conductive hearing loss with Carhart's notch, not high-frequency SNHL."),
            ("Meniere's disease", False, "Meniere's causes fluctuating LOW-frequency SNHL with vertigo and tinnitus."),
            ("Noise-Induced Hearing Loss (NIHL)", False, "NIHL classically causes an acoustic notch dip centered specifically at 4000 Hz, with recovery at 8000 Hz.")
        ],
        "pearl": "Presbycusis (Age-Related Hearing Loss): Most common cause of hearing impairment in the elderly (>65 yrs). Characterized by bilateral, symmetrical, progressive HIGH-FREQUENCY SNHL. Speech discrimination is disproportionately impaired (Phonemic regression: difficulty understanding consonants like s, f, th in background noise). Schuknecht Classification: 1. Sensory (loss of hair cells in basal turn of cochlea) | 2. Neural (loss of spiral ganglion neurons) | 3. Strial / Metabolic (atrophy of stria vascularis, flat audiogram) | 4. Cochlear conductive (stiffening of basilar membrane). Management: Binaural digital hearing aids.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 16 (Hearing Loss), p. 122-126.",
        "difficulty": "easy"
    },
    {
        "subject": "Otorhinolaryngology (ENT)",
        "concept_name": "Core Principles: Laryngeal Carcinoma & Vocal Cord Nodules",
        "stem": (
            "In patients undergoing diagnostic evaluation for stridor and upper airway obstruction, "
            "a 3-year-old unimmunized child presents with high fever, sore throat, muffled 'hot potato' voice, "
            "drooling of saliva, and tripod positioning (sitting upright, leaning forward with neck extended). "
            "Lateral soft-tissue neck radiograph demonstrates an enlarged, swollen, thumb-like epiglottis ('Thumbprint Sign'). "
            "What is the diagnosis, and why is direct intraoral depressor examination STRICTLY CONTRAINDICATED at the bedside?"
        ),
        "options": [
            ("Acute Epiglottitis (Supraglottitis); Direct tongue blade depression can trigger fatal instantaneous laryngospasm and complete airway closure", True, None),
            ("Laryngotracheobronchitis (Croup); Causes aspiration of gastric contents", False, "Croup presents with a barking cough and subglottic 'Steeple sign' on AP radiograph."),
            ("Peritonsillar abscess (Quinsy); Triggers rupture of carotid artery", False, "Quinsy is unilateral peritonsillar swelling with uvular deviation, not epiglottitis."),
            ("Retropharyngeal abscess; Causes instantaneous mediastinal rupture", False, "RPA causes widened prevertebral soft tissue shadow on lateral radiograph.")
        ],
        "pearl": "Acute Epiglottitis vs Croup: 1. ACUTE EPIGLOTTITIS: Organism: Haemophilus influenzae type b (Hib). Features: High fever + Toxic appearance + DROOLING of saliva + Tripod posture + Muffled voice (NO barking cough). Lateral X-ray: THUMBPRINT SIGN (swollen epiglottis). MANDATORY RULE: NEVER examine throat with a tongue depressor outside an operating theater (triggers fatal laryngospasm!). Secure airway under controlled anesthesia. 2. CROUP (Acute Laryngotracheobronchitis): Parainfluenza virus Type 1. Barking seal-like cough + Inspiratory stridor. AP X-ray: STEEPLE SIGN (subglottic narrowing). Treatment: Nebulized Budesonide / Dexamethasone + Nebulized Epinephrine.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 39 (Acute Laryngitis), p. 282-288.",
        "difficulty": "easy"
    }
]
