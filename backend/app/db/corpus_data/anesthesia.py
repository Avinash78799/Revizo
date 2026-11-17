"""
Authentic High-Yield NEET-PG Clinical Questions for Anesthesiology
References: Miller's Anesthesia (9th Ed), Morgan & Mikhail's Clinical Anesthesiology (7th Ed)
"""

ANESTHESIOLOGY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Malignant Hyperthermia Diagnosis & Dantrolene",
        "stem": (
            "A 24-year-old male with no prior medical history is undergoing emergency open reduction and internal fixation of a fractured femur. "
            "General anesthesia was induced with Propofol and Succinylcholine, and maintained with Sevoflurane and Nitrous Oxide. "
            "Thirty minutes into surgery, the capnograph alarms showing an unexplained, acute rise in End-Tidal Carbon Dioxide (EtCO2) from 38 mmHg to 82 mmHg, "
            "unresponsive to increasing minute ventilation. The patient becomes tachycardic (heart rate 145 bpm) with generalized muscle rigidity, and core body temperature rapidly rises to 40.2°C. "
            "What is the definitive, life-saving therapeutic drug of choice?"
        ),
        "options": [
            ("Intravenous Dantrolene Sodium (initial bolus 2.5 mg/kg)", True, None),
            ("Intravenous Calcium Chloride (10 mL of 10% solution)", False, "Calcium chloride would exacerbate intracellular hypercalcemia and muscle hypercontraction in malignant hyperthermia."),
            ("Intravenous Physostigmine (1 mg slow push)", False, "Physostigmine is an anticholinesterase used for central anticholinergic toxicity, not for malignant hyperthermia."),
            ("Intravenous Epinephrine (1 mg rapid bolus)", False, "Epinephrine would aggravate extreme sympathetic hyperstimulation and malignant tachyarrhythmias.")
        ],
        "pearl": "Malignant Hyperthermia (MH): Autosomal dominant mutation in RYR1 (Ryanodine receptor gene on chromosome 19q) -> massive Ca2+ release from sarcoplasmic reticulum. Triggered by: Volatile inhalational anesthetics (Halothane, Sevoflurane, Desflurane) + Succinylcholine. EARLIEST SIGN: Unexplained rise in EtCO2. DRUG OF CHOICE: IV Dantrolene Sodium (2.5 mg/kg initial bolus, repeated up to 10 mg/kg).",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 39 (Malignant Hyperthermia), p. 1162-1175.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Malignant Hyperthermia Diagnosis & Dantrolene",
        "stem": (
            "A 30-year-old woman whose maternal uncle died during anesthesia is scheduled for an elective laparoscopic cholecystectomy. "
            "Genetic counseling confirms a family history of malignant hyperthermia susceptibility. "
            "Which of the following anesthetic regimens is entirely SAFE to administer to this patient?"
        ),
        "options": [
            ("Sevoflurane inhalational induction followed by Succinylcholine intubation", False, "Both Sevoflurane (volatile agent) and Succinylcholine (depolarizing blocker) are potent triggers of malignant hyperthermia."),
            ("Total Intravenous Anesthesia (TIVA) using Propofol, Fentanyl, and Rocuronium", True, None),
            ("Halothane maintenance with Desflurane emergence", False, "All halogenated volatile inhalational anesthetics are contraindicated in MH susceptibility."),
            ("Isoflurane maintenance with Atracurium and Succinylcholine", False, "Succinylcholine and Isoflurane are triggers of MH.")
        ],
        "pearl": "MH Safe vs Trigger Agents: TRIGGERS: All volatile inhalational agents (Halothane, Isoflurane, Sevoflurane, Desflurane) AND Succinylcholine. SAFE AGENTS: Propofol, Etomidate, Ketamine, Opioids (Fentanyl, Morphine), Benzodiazepines, Nitrous Oxide, and Non-depolarizing Muscle Relaxants (Rocuronium, Vecuronium, Cisatracurium).",
        "citation": "Morgan & Mikhail's Clinical Anesthesiology, 7th Ed, Chapter 44, p. 985-992.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Local Anesthetic Systemic Toxicity (LAST) & Lipid Emulsion",
        "stem": (
            "A 45-year-old male is receiving an ultrasound-guided supraclavicular brachial plexus block with 25 mL of 0.5% Bupivacaine for wrist surgery. "
            "Immediately following the injection, the patient complains of perioral numbness, metallic taste in the mouth, and severe tinnitus. "
            "Within seconds, he develops generalized tonic-clonic convulsions, followed by loss of consciousness and cardiovascular collapse. "
            "The ECG monitor reveals wide-complex ventricular tachycardia. What is the definitive first-line antidote for this condition?"
        ),
        "options": [
            ("20% Intravenous Lipid Emulsion (Intralipid 1.5 mL/kg bolus followed by 0.25 mL/kg/min infusion)", True, None),
            ("Intravenous Lidocaine 1.5 mg/kg bolus", False, "Lidocaine is itself a local anesthetic and would severely aggravate local anesthetic systemic toxicity!"),
            ("Intravenous Flumazenil 0.5 mg bolus", False, "Flumazenil is a benzodiazepine antagonist, not an antidote for local anesthetic cardiotoxicity."),
            ("Intravenous Digoxin 0.5 mg slow infusion", False, "Digoxin increases arrhythmogenicity and has no role in LAST rescue.")
        ],
        "pearl": "Local Anesthetic Systemic Toxicity (LAST): Highly lipid-soluble local anesthetics (Bupivacaine > Ropivacaine) have high affinity for cardiac sodium channels. CNS toxicity (metallic taste, tinnitus, seizures) precedes cardiovascular collapse (ventricular arrhythmias, asystole). ANTIDOTE: 20% Lipid Emulsion (Intralipid) acts as a 'lipid sink' to extract lipophilic local anesthetic from cardiac tissue.",
        "citation": "ASRA Practice Advisory on Local Anesthetic Systemic Toxicity (2020) / Miller's Anesthesia Ch 36.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Local Anesthetic Systemic Toxicity (LAST) & Lipid Emulsion",
        "stem": (
            "A surgeon plans to perform wide local excision of a benign lipoma under local infiltration with 1% Lignocaine with Adrenaline (1:200,000) "
            "in a 70-kg adult male. What is the maximum safe recommended permissible dose of Lignocaine with Adrenaline in this patient?"
        ),
        "options": [
            ("200 mg (approximately 3 mg/kg)", False, "3 mg/kg (max 200 mg) is the maximum safe dose for PLAIN Lignocaine WITHOUT adrenaline."),
            ("500 mg (approximately 7 mg/kg)", True, None),
            ("800 mg (approximately 12 mg/kg)", False, "800 mg is in the toxic range and exceeds the safe limit."),
            ("1000 mg (approximately 15 mg/kg)", False, "1000 mg causes lethal systemic toxicity.")
        ],
        "pearl": "Local Anesthetic Max Doses: Lignocaine PLAIN: 3-4.5 mg/kg (max 200-300 mg) | Lignocaine WITH ADRENALINE: 7 mg/kg (max 500 mg) | Bupivacaine: 2 mg/kg (max 150 mg plain) or 2.5 mg/kg with adrenaline (max 175 mg). Adrenaline causes local vasoconstriction, slowing systemic absorption and extending duration of action.",
        "citation": "Morgan & Mikhail's Clinical Anesthesiology, 7th Ed, Chapter 16, p. 312-320.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Intravenous Anesthetic Agents: Propofol & Ketamine",
        "stem": (
            "A 12-year-old child with severe acute bronchial asthma and persistent bronchospasm presents with an acute right lower quadrant appendiceal perforation "
            "requiring emergency laparotomy. Which of the following intravenous anesthetic induction agents is most advantageous in this patient because of its potent "
            "bronchodilating and sympathomimetic properties?"
        ),
        "options": [
            ("Ketamine", True, None),
            ("Propofol", False, "Propofol has mild bronchodilatory properties but produces significant vasodilation and hypotension without the potent sympathomimetic bronchodilation of Ketamine."),
            ("Thiopental sodium", False, "Thiopental can trigger histamine release and provoke severe bronchospasm in asthmatic patients."),
            ("Etomidate", False, "Etomidate does not produce active bronchodilation and inhibits adrenal steroidogenesis.")
        ],
        "pearl": "Ketamine: Non-competitive NMDA receptor antagonist. Produces 'dissociative anesthesia' (eyes open, cataleptic state, analgesia, amnesia). Key advantages: Potent bronchodilator (drug of choice for status asthmaticus requiring anesthesia), maintains blood pressure (sympathomimetic), preserves protective airway reflexes. Avoid in: Raised intracranial pressure (ICP) and severe coronary artery disease.",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 29 (Intravenous Anesthetics), p. 782-790.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Intravenous Anesthetic Agents: Propofol & Ketamine",
        "stem": (
            "A 65-year-old female undergoes day-care laparoscopic tubal ligation under general anesthesia induced and maintained with Propofol. "
            "Which of the following pharmacological properties of Propofol makes it the premier agent of choice for day-care ambulatory surgery?"
        ),
        "options": [
            ("Rapid clearance and context-sensitive half-life with intrinsic antiemetic properties", True, None),
            ("Potent long-lasting postoperative analgesia equivalent to morphine", False, "Propofol has NO intrinsic analgesic properties; analgesics must be co-administered."),
            ("Zero effect on systemic vascular resistance and myocardial contractility", False, "Propofol causes significant systemic vasodilation and mild myocardial depression, often lowering blood pressure."),
            ("Complete lack of respiratory depression at hypnotic doses", False, "Propofol is a potent respiratory depressant causing dose-dependent apnea.")
        ],
        "pearl": "Propofol (2,6-diisopropylphenol): GABA-A receptor agonist. Ideal for Day Care (Ambulatory) Anesthesia because of: 1. Rapid recovery with clear-headed emergence (context-sensitive half-life is short) | 2. Intrinsic antiemetic action (reduces PONV) | 3. Antipruritic and anticonvulsant properties. Note: Has NO analgesic effect.",
        "citation": "Morgan & Mikhail's Clinical Anesthesiology, 7th Ed, Chapter 8, p. 175-182.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Mallampati Classification & Difficult Airway Algorithm",
        "stem": (
            "During preoperative airway assessment, a 48-year-old obese male is asked to sit upright, open his mouth as wide as possible, and protrude his tongue "
            "WITHOUT phonating. On direct visual inspection of the oral cavity, the anesthesiologist can visualize the hard palate and soft palate, "
            "but the base of the uvula, faucial pillars, and posterior pharyngeal wall are completely obscured by the tongue. "
            "What is the Modified Mallampati Class for this patient?"
        ),
        "options": [
            ("Mallampati Class I", False, "Class I: Soft palate, fauces, uvula, and pillars are all fully visualized."),
            ("Mallampati Class II", False, "Class II: Soft palate, fauces, and entire uvula are visualized."),
            ("Mallampati Class III", True, None),
            ("Mallampati Class IV", False, "Class IV: Only the hard palate is visualized; soft palate is not visible at all.")
        ],
        "pearl": "Modified Mallampati Classification (PUSH): Class I: Pillars, Uvula, Soft palate, Hard palate | Class II: Uvula, Soft palate, Hard palate | Class III: Soft palate, Hard palate (base of uvula only) | Class IV: Hard palate ONLY. Classes III and IV strongly correlate with difficult direct laryngoscopy and intubation.",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 47 (Airway Management), p. 1385-1392.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Mallampati Classification & Difficult Airway Algorithm",
        "stem": (
            "A 35-year-old trauma patient with a full stomach and cervical spine instability is in the operating theater for emergency exploratory laparotomy. "
            "The anesthesiologist prepares for Rapid Sequence Induction and Intubation (RSII). What is the physiological purpose of applying cricoid pressure "
            "(Sellick's maneuver) during RSII?"
        ),
        "options": [
            ("To improve direct visualization of the vocal cords during direct laryngoscopy", False, "Cricoid pressure often worsens laryngoscopic view; BURP (Backward-Upward-Rightward Pressure) improves visualization of cords."),
            ("To compress the esophagus against the anterior surface of the C6 vertebral body, thereby preventing passive regurgitation of gastric contents into the pharynx", True, None),
            ("To stimulate the vagus nerve and prevent tachycardia during intubation", False, "Cricoid pressure does not aim for vagal stimulation."),
            ("To dilate the subglottic space for passage of a larger endotracheal tube", False, "The cricoid cartilage is a complete cartilaginous ring and cannot be dilated by external pressure.")
        ],
        "pearl": "Sellick's Maneuver (Cricoid Pressure): Force applied: 10 Newtons when awake -> 30 Newtons after loss of consciousness. Purpose: Compresses the compliant esophagus between the non-yielding circular cricoid ring and the C6 vertebral body, preventing passive gastric acid regurgitation into the lungs until the endotracheal tube cuff is inflated.",
        "citation": "Morgan & Mikhail's Clinical Anesthesiology, 7th Ed, Chapter 19, p. 388-394.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Minimum Alveolar Concentration (MAC) & Potency",
        "stem": (
            "Anesthesia is maintained in an adult patient with an inhalational agent. The minimum alveolar concentration (MAC) of volatile anesthetics "
            "reflects anesthetic potency. Which of the following physical-chemical properties of an inhalational anesthetic agent is inversely proportional "
            "to its Minimum Alveolar Concentration (MAC)?"
        ),
        "options": [
            ("Blood:Gas partition coefficient", False, "Blood:Gas partition coefficient determines the SPEED of induction and recovery, not potency."),
            ("Oil:Gas partition coefficient (Meyer-Overton Rule)", True, None),
            ("Vapor pressure at 20°C", False, "Vapor pressure determines vaporizer design, not MAC."),
            ("Molecular weight", False, "Molecular weight does not dictate anesthetic potency.")
        ],
        "pearl": "Meyer-Overton Hypothesis: MAC is INVERSELY proportional to lipid solubility (Oil:Gas partition coefficient). Potency = 1 / MAC. High oil:gas coefficient = High potency = Low MAC. For example, Methoxyflurane has the highest oil:gas solubility (970) and lowest MAC (0.16%); Nitrous oxide has the lowest oil:gas solubility (1.4) and highest MAC (104%).",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 26 (Inhalation Anesthetics: Mechanism of Action), p. 642-650.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Minimum Alveolar Concentration (MAC) & Potency",
        "stem": (
            "During general anesthesia with Sevoflurane (1 MAC = 2.0% in oxygen), which of the following physiological or pharmacological factors "
            "will DECREASE the patient's Minimum Alveolar Concentration (MAC) requirement?"
        ),
        "options": [
            ("Hyperthermia", False, "Hyperthermia increases metabolic rate and INCREASES MAC."),
            ("Chronic heavy alcohol abuse (without acute intoxication)", False, "Chronic alcohol tolerance INCREASES MAC requirements."),
            ("Acute hypothermia, advanced age, and acute ethanol intoxication", True, None),
            ("Hypernatremia", False, "Hypernatremia INCREASES MAC requirements.")
        ],
        "pearl": "Factors Influencing MAC: DECREASE MAC (Less anesthetic needed): Hypothermia, Elderly age, Pregnancy (progesterone), Acute alcohol intoxication, Hyponatremia, Opioids, Sedatives. INCREASE MAC (More anesthetic needed): Hyperthermia, Young age / infants (highest MAC at 6 months), Hypernatremia, Chronic alcohol tolerance, Sympathetic stimulation (Amphetamines).",
        "citation": "Morgan & Mikhail's Clinical Anesthesiology, 7th Ed, Chapter 7, p. 154-162.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Spinal vs Epidural Anesthesia Differences",
        "stem": (
            "A 32-year-old primigravida undergoes elective Cesarean section under subarachnoid (spinal) anesthesia at the L3-L4 interspace. "
            "On the second postoperative day, she complains of a severe, throbbing, bilateral fronto-occipital headache that worsens dramatically "
            "upon sitting or standing and is significantly relieved when lying completely flat. There is no neck stiffness or fever. "
            "What is the most definitive therapeutic intervention for refractory Post-Dural Puncture Headache (PDPH)?"
        ),
        "options": [
            ("Epidural autologous blood patch (15-20 mL of sterile autologous venous blood injected into the epidural space)", True, None),
            ("Immediate lumbar puncture drainage of 20 mL of CSF", False, "Draining more CSF would exacerbate intracranial hypotension and traction on pain-sensitive meninges!"),
            ("High-dose intravenous Mannitol 20%", False, "Mannitol is an osmotic diuretic that reduces intracranial pressure and would worsen low-pressure PDPH!"),
            ("Surgical exploration and suturing of the dural tear", False, "Open surgery is unnecessary; epidural blood patch has >90% success rate.")
        ],
        "pearl": "Post-Dural Puncture Headache (PDPH): Caused by continuous CSF leakage through a dural hole -> intracranial hypotension -> downward traction on pain-sensitive meninges and cranial nerves. Cardinal sign: Severe POSTURAL headache (worse upright, relieved supine). Conservative: Bed rest, aggressive oral/IV hydration, Caffeine, Sumatriptan. DEFINITIVE TREATMENT: Epidural Autologous Blood Patch (15-20 mL).",
        "citation": "Miller's Anesthesia, 9th Ed, Chapter 49 (Spinal and Epidural Anesthesia), p. 1478-1485.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Spinal vs Epidural Anesthesia Differences",
        "stem": (
            "When performing a midline lumbar puncture for spinal anesthesia in an adult patient, which anatomical ligament is pierced "
            "immediately before entering the epidural space and gives the characteristic 'loss of resistance' or tactile 'pop'?"
        ),
        "options": [
            ("Supraspinous ligament", False, "Supraspinous ligament is the first tough ligament encountered bridging the tips of spinous processes."),
            ("Interspinous ligament", False, "Interspinous ligament lies between the spinous processes."),
            ("Ligamentum flavum", True, None),
            ("Posterior longitudinal ligament", False, "Posterior longitudinal ligament lies anterior to the spinal cord on the posterior aspect of vertebral bodies.")
        ],
        "pearl": "Layers pierced in midline Spinal Needle insertion: 1. Skin -> 2. Subcutaneous tissue -> 3. Supraspinous ligament -> 4. Interspinous ligament -> 5. Ligamentum flavum (Loss of resistance / pop) -> Epidural space -> 6. Dura mater & Arachnoid mater -> Subarachnoid space (CSF flash).",
        "citation": "Morgan & Mikhail's Clinical Anesthesiology, 7th Ed, Chapter 45, p. 945-952.",
        "difficulty": "easy"
    }
]
