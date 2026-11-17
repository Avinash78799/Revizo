"""
Authentic High-Yield NEET-PG Clinical Questions for General Surgery
References: Bailey & Love's Short Practice of Surgery (28th Ed), Sabiston Textbook of Surgery (21st Ed)
"""

SURGERY_QUESTIONS = [
    {
        "concept_name": "Core Principles: ATLS Primary Survey & Hemorrhagic Shock",
        "stem": (
            "A 28-year-old male is brought to the emergency trauma resuscitation bay following a head-on motor vehicle collision. "
            "He is pale, diaphoretic, and confused. Vitals: heart rate 136 bpm, blood pressure 82/50 mmHg, respiratory rate 28/min, "
            "and urine output is 12 mL/hr via Foley catheter. Estimated blood loss is approximately 1800 mL (35% of total blood volume). "
            "According to the Advanced Trauma Life Support (ATLS 10th edition) classification of hemorrhagic shock, "
            "what class of shock is this, and what is the mandatory immediate resuscitation fluid/blood strategy?"
        ),
        "options": [
            ("Class III Hemorrhagic Shock; Immediate balanced blood component therapy (Packed Red Blood Cells, Fresh Frozen Plasma, Platelets in 1:1:1 ratio) along with warmed crystalloids", True, None),
            ("Class I Hemorrhagic Shock; Oral rehydration solution and observation", False, "Class I shock is minimal blood loss (<15%, <750 mL) with normal vital signs."),
            ("Class II Hemorrhagic Shock; 3 liters of normal saline bolus without blood products", False, "Class II shock (15-30% loss) has tachycardia but normal blood pressure; Class III has marked hypotension and requires blood transfusion."),
            ("Neurogenic shock; High-dose intravenous Dopamine infusion alone", False, "Neurogenic shock classically features warm peripheries, hypotension with BRADYCARDIA, not hemorrhagic tachycardia.")
        ],
        "pearl": "ATLS Classification of Hemorrhagic Shock (70 kg adult): Class I (<15% loss, <750 mL): HR <100, BP normal, pulse pressure normal. Class II (15-30% loss, 750-1500 mL): HR >100, BP normal, DECREASED pulse pressure (earliest sign). Class III (30-40% loss, 1500-2000 mL): HR >120, HYPOTENSION, confused, oliguria. REQUIRES BLOOD TRANSFUSION! Class IV (>40% loss, >2000 mL): HR >140, severe hypotension, lethargic, anuria. Massive Transfusion Protocol: 1:1:1 ratio (PRBC : FFP : Platelets).",
        "citation": "ATLS Student Course Manual (10th Ed) / Bailey & Love, 28th Ed, Chapter 21 (Shock), p. 288-300.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: ATLS Primary Survey & Hemorrhagic Shock",
        "stem": (
            "During the initial breathing assessment in the ATLS primary survey of a blunt chest trauma victim, "
            "the patient develops severe respiratory distress, cyanosis, and hypotension (BP 70/40 mmHg). "
            "Examination reveals distended neck veins, absence of breath sounds over the entire right hemithorax, "
            "and hyperresonance to percussion with the trachea deviated sharply to the left. "
            "What is the single most urgent, immediate life-saving intervention before obtaining any chest radiograph?"
        ),
        "options": [
            ("Immediate needle decompression / thoracostomy (in 5th intercostal space slightly anterior to mid-axillary line or 2nd ICS mid-clavicular line)", True, None),
            ("Send the patient immediately for an urgent contrast-enhanced CT scan of the chest", False, "TENSION PNEUMOTHORAX IS A CLINICAL DIAGNOSIS! Sending an unstable patient to CT is a fatal error."),
            ("Perform an emergency pericardiocentesis under ultrasound guidance", False, "Pericardiocentesis is for Cardiac Tamponade (Beck's triad: muffled heart sounds, hypotension, JVD, but bilateral breath sounds normal)."),
            ("Administer high-dose intravenous Furosemide", False, "Diuretics are contraindicated in obstructive shock with severe hypovolemia.")
        ],
        "pearl": "Tension Pneumothorax: One-way valve mechanism traps air in pleural space -> collapse of ipsilateral lung -> mediastinal shift to opposite side -> compression of superior/inferior vena cava -> OBSTRUCTIVE SHOCK. Triad: Hypotension + Distended neck veins + Unilateral absent breath sounds with hyperresonance and tracheal deviation. ATLS 10th Ed Update: Immediate decompression with a large-bore cannula (14-gauge) in the 5TH INTERCOSTAL SPACE MID-AXILLARY LINE (preferred over 2nd ICS in adults due to thicker chest wall), followed immediately by Tube Thoracostomy (Chest tube). DO NOT WAIT FOR CXR!",
        "citation": "ATLS 10th Ed / Bailey & Love, 28th Ed, Chapter 23 (Thoracic Trauma), p. 332-340.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Burns Assessment: Rule of Nines & Parkland Formula",
        "stem": (
            "A 30-year-old male weighing 70 kg sustains deep partial-thickness burns in an industrial boiler explosion. "
            "Physical examination reveals burns involving his entire anterior and posterior trunk (36%), "
            "the entire right upper extremity (9%), and the anterior surface of both lower extremities (9% + 9% = 18%). "
            "Total Body Surface Area (TBSA) burned is 63%. According to the Parkland formula, what is the total volume of Ringer's Lactate "
            "required in the first 24 hours, and what volume must be administered during the first 8 hours post-injury?"
        ),
        "options": [
            ("Total 17,640 mL; 8,820 mL in the first 8 hours post-injury", True, None),
            ("Total 8,820 mL; 4,410 mL in the first 8 hours post-injury", False, "Parkland uses 4 mL/kg/% TBSA, not 2 mL/kg/% TBSA."),
            ("Total 25,000 mL; 12,500 mL in the first 8 hours post-injury", False, "Over-resuscitation exceeds the formula and causes fluid creep and abdominal compartment syndrome."),
            ("Total 5,000 mL of 5% Dextrose in normal saline over 24 hours", False, "Ringer's Lactate is the resuscitation fluid of choice, not hypotonic dextrose.")
        ],
        "pearl": "Parkland Formula for Burn Resuscitation: Fluid of Choice: Ringer's Lactate (Hartmann's Solution). Total 24-hr Fluid = 4 mL x Body Weight (kg) x % TBSA burned. Schedule: 50% of total calculated volume given in the FIRST 8 HOURS (calculated from the TIME OF INJURY, not time of hospital arrival!). Remaining 50% given over the NEXT 16 HOURS. Rule of Nines: Head & Neck = 9% | Each Upper Limb = 9% (x2=18%) | Anterior Trunk = 18% | Posterior Trunk = 18% | Each Lower Limb = 18% (x2=36%) | Perineum/Genitalia = 1%. Monitoring endpoint: Urine output 0.5-1.0 mL/kg/hr in adults.",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 5 (Burns), p. 58-72.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Burns Assessment: Rule of Nines & Parkland Formula",
        "stem": (
            "A patient with a full-thickness, circumferential burn involving his entire right forearm and hand is brought to the burn ICU. "
            "Six hours later, the hand becomes cold and pale, capillary refill time is prolonged to 5 seconds, "
            "and radial and ulnar pulses are no longer detectable on Doppler ultrasound due to the constricting, unyielding leathery burn eschar. "
            "What is the immediate bedside surgical procedure required to restore distal limb perfusion?"
        ),
        "options": [
            ("Emergency Escharotomy along the mid-medial and mid-lateral axial borders of the forearm", True, None),
            ("Immediate trans-radial amputation", False, "Amputation is premature and mutilating; escharotomy relieves the tourniquet effect and restores perfusion."),
            ("Intravenous Heparin anticoagulation infusion", False, "Heparin does not relieve mechanical constriction by the rigid coagulated dermis."),
            ("Application of silver sulfadiazine cream and elevation", False, "Topical creams cannot relieve arterial and capillary compartment compression.")
        ],
        "pearl": "Escharotomy in Circumferential Burns: Full-thickness burn eschar is rigid, inelastic, and leathery. Edema beneath the eschar increases tissue pressure -> tourniquet effect -> vascular compromise and muscle necrosis. Bedside Escharotomy: Full-thickness incision made through the dead eschar down into the subcutaneous fat (no anesthesia needed because cutaneous nerve endings are destroyed in 3rd-degree burns!). Relieves constriction instantly. Fasciotomy is reserved if deep compartment pressures remain >30 mmHg after escharotomy.",
        "citation": "Sabiston Textbook of Surgery, 21st Ed, Chapter 20 (Burns), p. 518-528.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Acute Appendicitis & Alvarado Score",
        "stem": (
            "A 19-year-old male presents with dull, periumbilical aching abdominal pain for 12 hours that subsequently shifted "
            "and localized to the right lower quadrant (RLQ), accompanied by anorexia, nausea, and low-grade fever (100.2°F). "
            "Physical examination reveals marked localized tenderness and rebound tenderness at McBurney's point. "
            "Deep palpation of the left lower quadrant elicits sharp pain in the right lower quadrant. "
            "WBC count is 13,800/uL with 82% neutrophils. What is the name of this referred tenderness sign, and what is the patient's Alvarado score?"
        ),
        "options": [
            ("Rovsing's Sign; Alvarado Score = 9 (indicating high probability of acute appendicitis requiring surgery)", True, None),
            ("Murphy's Sign; Alvarado Score = 3", False, "Murphy's sign is inspiratory arrest in acute cholecystitis."),
            ("Cullen's Sign; Alvarado Score = 5", False, "Cullen's sign is periumbilical ecchymosis in acute hemorrhagic pancreatitis."),
            ("Grey Turner's Sign; Alvarado Score = 6", False, "Grey Turner's sign is flank ecchymosis in retroperitoneal hemorrhage / pancreatitis.")
        ],
        "pearl": "Alvarado Score MANTRELS (Total 10): M: Migration of pain to RLQ (1) | A: Anorexia (1) | N: Nausea/Vomiting (1) | T: Tenderness in RLQ (2) | R: Rebound tenderness (1) | E: Elevated temperature ≥37.3°C (1) | L: Leukocytosis >10,000 (2) | S: Shift of neutrophils to left >75% (1). Score ≥7: Highly predictive of acute appendicitis (indicates emergency appendectomy). Rovsing's sign: LLQ pressure forces colonic gas retrogradely into cecum, causing RLQ pain. Psoas sign: Pain on passive hip extension (retrocecal appendix). Obturator sign: Pain on internal rotation of flexed hip (pelvic appendix).",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 73 (The Appendix), p. 1320-1335.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Acute Appendicitis & Alvarado Score",
        "stem": (
            "During open emergency appendectomy for acute phlegmonous appendicitis via a McBurney gridiron incision, "
            "the surgeon easily delivers the cecum into the wound. What anatomical landmark on the surface of the cecum "
            "is the most reliable, constant surgical guide to trace directly to the base of the vermiform appendix?"
        ),
        "options": [
            ("Convergence of the three Taeniae Coli (taenia libera, taenia mesocolica, and taenia omentalis) at the cecal apex", True, None),
            ("The ileocecal valve of Bauhin", False, "The ileocecal valve lies superior to the appendix base on the posteromedial wall."),
            ("The appendicular artery in the mesoappendix", False, "The artery runs within the mobile mesoappendix and does not locate the base on the cecum."),
            ("The folds of Treves (ileocecal fold)", False, "The bloodless fold of Treves is an avascular peritoneal fold, not a guide to the base.")
        ],
        "pearl": "Surgical Anatomy of Appendix: Most constant anatomical feature: The 3 taeniae coli of the ascending colon and cecum converge at the base of the appendix, serving as the definitive surgical guide during difficult appendectomy. Most common anatomical position of appendix tip: RETROCECAL (65%), followed by PELVIC (31%), Subcecal (2%), Pre-ileal (1%), Post-ileal (0.5%). Appendicular artery is an end-artery derived from the inferior division of the ileocolic artery (thrombosis -> gangrene).",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 73, p. 1320-1324.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Gallstone Disease & Laparoscopic Cholecystectomy",
        "stem": (
            "During laparoscopic cholecystectomy for symptomatic cholelithiasis, the operating surgeon carefully dissects "
            "the hepatocystic triangle to achieve the 'Critical View of Safety' (Strasberg criteria) before clipping or dividing any tubular structures. "
            "What are the precise anatomical boundaries of the Triangle of Calot (Calot's original triangle)?"
        ),
        "options": [
            ("Cystic duct inferiorly, Common Hepatic Duct medially, and Cystic Artery superiorly", True, None),
            ("Common bile duct laterally, Portal vein medially, and Duodenum inferiorly", False, "These form part of the free border of the lesser omentum (foramen of Winslow)."),
            ("Cystic duct laterally, Inferior surface of liver superiorly, and Right hepatic artery medially", False, "This is the Hepatobiliary / Hepatocystic triangle, which is larger than the original Calot triangle."),
            ("Falciform ligament anteriorly, Ligamentum teres inferiorly, and IVC posteriorly", False, "These are hepatic surface anatomical fissures.")
        ],
        "pearl": "Calot's Triangle vs Hepatocystic Triangle: Calot's Original Triangle (1891): Bound by Cystic Duct (inferiorly), Common Hepatic Duct (medially), and CYSTIC ARTERY (superiorly). Contains: Lund's node / Calot's lymph node. Hepatocystic Triangle: Bound by Cystic Duct, Common Hepatic Duct, and INFERIOR BORDER OF LIVER. Critical View of Safety (Strasberg): Requires: 1. Clearance of fat and fibrous tissue from hepatocystic triangle | 2. Dissection of lower 1/3 of gallbladder off cystic plate | 3. Exactly TWO and only two structures visualized entering the gallbladder (Cystic duct and Cystic artery). Prevents bile duct injury!",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 67 (Gallbladder and Bile Ducts), p. 1198-1212.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Gallstone Disease & Laparoscopic Cholecystectomy",
        "stem": (
            "A 52-year-old female presents with episodic severe right upper quadrant colicky pain, high-spiking fevers with rigors, "
            "and jaundice for 2 days (Charcot's Triad). Her total bilirubin is 5.8 mg/dL and alkaline phosphatase is 480 U/L. "
            "Abdominal ultrasound shows multiple small calculi in the gallbladder and a dilated common bile duct (CBD) measuring 12 mm "
            "with an acoustic shadowing stone impacted in the distal intrapancreatic portion. There is no hypotension or altered mental status. "
            "What is the standard, evidence-based sequential management strategy?"
        ),
        "options": [
            ("Endoscopic Retrograde Cholangiopancreatography (ERCP) with endoscopic sphincterotomy and stone extraction, followed by elective Laparoscopic Cholecystectomy during the same hospital stay", True, None),
            ("Immediate emergency open common bile duct exploration and T-tube drainage without preoperative ERCP", False, "Surgical open exploration is invasive and carries higher morbidity than initial therapeutic ERCP."),
            ("Percutaneous transhepatic gallbladder drainage alone", False, "Percutaneous cholecystostomy is for acalculous cholecystitis in critically ill ICU patients, not choledocholithiasis."),
            ("Extracorporeal shock-wave lithotripsy (ESWL) without antibiotics", False, "ESWL has high recurrence rates and risks worsening cholangitis and pancreatitis.")
        ],
        "pearl": "Choledocholithiasis & Acute Cholangitis: Charcot's Triad: Jaundice + Fever with rigors + RUQ pain. Reynolds' Pentad (Septic shock): Charcot's triad + Hypotension + Altered Mental Status (requires EMERGENCY biliary decompression). Gold standard sequential management for gallstones with CBD stones: 1. Broad-spectrum IV antibiotics (e.g., Ceftriaxone + Metronidazole) -> 2. Therapeutic ERCP + Sphincterotomy + Balloon/basket extraction -> 3. Laparoscopic Cholecystectomy (to prevent recurrent gallstone migration).",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 67, p. 1214-1224.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Thyroid Nodules & Bethesda Classification",
        "stem": (
            "A 38-year-old female presents with a solitary, painless, firm thyroid nodule measuring 2.5 cm in the right lobe. "
            "Serum TSH is normal (1.8 mIU/L). Neck ultrasound reveals a solid, hypoechoic nodule with irregular, infiltrative margins, "
            "punctate microcalcifications, and a taller-than-wide shape. Fine Needle Aspiration Cytology (FNAC) is performed. "
            "Cytological smear reveals enlarged, overlapping follicular epithelial cells with pale, optically clear 'ground-glass' nuclei, "
            "prominent nuclear grooving, and pseudoinclusions ('Orphan Annie eye' nuclei), along with concentric laminated psammoma bodies. "
            "What is the diagnosis, and what is the primary mode of metastatic spread?"
        ),
        "options": [
            ("Papillary Thyroid Carcinoma (PTC); Lymphatic spread to regional cervical lymph nodes", True, None),
            ("Follicular Thyroid Carcinoma; Hematogenous spread to bones and lungs", False, "Follicular carcinoma cannot be diagnosed on FNAC alone (requires capsular/vascular invasion on histopathology) and spreads hematogenously."),
            ("Medullary Thyroid Carcinoma; Systemic calcitonin-mediated spread", False, "Medullary carcinoma arises from parafollicular C-cells, associated with RET mutations / MEN 2."),
            ("Anaplastic Thyroid Carcinoma; Rapid direct local invasion", False, "Anaplastic carcinoma occurs in elderly patients as a rapidly expanding stony hard compressive neck mass with bizarre giant cells.")
        ],
        "pearl": "Papillary Thyroid Carcinoma (PTC): Most common thyroid malignancy (80-85%). Associated with childhood radiation exposure and RET/PTC or BRAF V600E mutations. Pathognomonic cytology: 1. Orphan Annie Eye nuclei (optically clear, empty appearance) | 2. Nuclear grooves (coffee-bean appearance) | 3. Intranuclear cytoplasmic pseudoinclusions | 4. Psammoma bodies (concentric calcifications). Primary metastatic route: LYMPHATIC SPREAD to cervical lymph nodes (Level II, III, IV, VI). Excellent 10-year survival (>95%).",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 54 (Thyroid Gland), p. 848-862.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Thyroid Nodules & Bethesda Classification",
        "stem": (
            "A 45-year-old male undergoes ultrasound-guided FNAC of a 3 cm solitary thyroid nodule. "
            "The cytopathology report states: 'Bethesda System Category IV: Follicular Neoplasm / Suspicious for a Follicular Neoplasm'. "
            "Why is total thyroidectomy or complete histopathological examination of the excised thyroid lobe mandatory "
            "to differentiate a benign Follicular Adenoma from a malignant Follicular Thyroid Carcinoma?"
        ),
        "options": [
            ("Because malignant Follicular Carcinoma is distinguished from benign Follicular Adenoma strictly by the presence of Capsular and/or Vascular Invasion, which cannot be assessed on cytology smears", True, None),
            ("Because follicular cells always undergo malignant transformation within 6 weeks", False, "Follicular adenomas are benign and do not inevitably transform."),
            ("Because serum thyroglobulin levels are always zero in follicular cancer", False, "Thyroglobulin is elevated in both benign and malignant follicular thyroid tissue."),
            ("Because radioactive iodine ablation is curative without surgery", False, "Surgery is mandatory; radioiodine is adjuvant post-thyroidectomy.")
        ],
        "pearl": "Follicular Neoplasm Diagnostic Dilemma: FNAC CANNOT distinguish between Follicular Adenoma and Follicular Carcinoma because both display identical cellular features. Malignancy (Follicular Carcinoma) is defined STRICTLY by: 1. Full-thickness CAPSULAR INVASION, or 2. VASCULAR INVASION (tumor cells invading into capsular/extracapsular blood vessels). Management: Diagnostic Hemithyroidectomy / Lobectomy. If histopathology shows capsular/vascular invasion -> Completion Thyroidectomy followed by Radioiodine (I-131) ablation.",
        "citation": "Sabiston Textbook of Surgery, 21st Ed, Chapter 36 (Thyroid), p. 892-905.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Breast Cancer Staging & Triple Assessment",
        "stem": (
            "A 54-year-old postmenopausal female presents with a painless, hard lump in the upper outer quadrant of her left breast for 3 months. "
            "On physical examination, the lump measures 2.8 cm, has ill-defined irregular margins, is tethered to the overlying breast skin causing dimpling, "
            "and there are two firm, non-matted, mobile ipsilateral anterior axillary lymph nodes. "
            "According to international clinical standards, what constitutes the mandatory 'Triple Assessment' for all breast lumps?"
        ),
        "options": [
            ("Clinical examination + Bilateral Mammography / Breast Ultrasound + Core Needle Biopsy (Histopathology with ER, PR, HER2 testing)", True, None),
            ("Clinical examination + Serum CA 15-3 level + PET-CT scan", False, "Tumor markers and PET-CT are not initial diagnostic modalities for localized breast lumps."),
            ("Physical examination + Diagnostic Fine Needle Aspiration Cytology (FNAC) alone", False, "FNAC has been replaced by Core Needle Biopsy because core biopsy preserves tissue architecture and allows ER/PR/HER2 receptor status testing."),
            ("Magnetic resonance imaging (MRI) + Incisional open surgical biopsy", False, "Open surgical biopsy is obsolete as initial diagnostic workup; core needle biopsy is standard.")
        ],
        "pearl": "Triple Assessment of Breast Lump: Sensitivity >99% when all 3 components agree: 1. Clinical Examination | 2. Imaging (Bilateral Mammography for age ≥40; Ultrasound for age <40 or dense breasts) | 3. Tissue Sampling: CORE NEEDLE BIOPSY (tru-cut) is the standard of care (provides tissue architecture, invasive vs in-situ distinction, and receptor status: ER, PR, HER-2/neu, Ki-67). FNAC cannot distinguish DCIS from invasive ductal carcinoma!",
        "citation": "Bailey & Love's Short Practice of Surgery, 28th Ed, Chapter 57 (The Breast), p. 910-928.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Breast Cancer Staging & Triple Assessment",
        "stem": (
            "A 48-year-old female with a 2.2 cm unifocal Invasive Ductal Carcinoma in the left lower inner quadrant "
            "has a clinically negative axilla (cN0). She is scheduled for Breast Conserving Surgery (Lumpectomy / Wide Local Excision). "
            "What is the gold standard, minimally invasive surgical technique used to assess the axillary nodal basin "
            "and avoid the severe morbidities of routine Axillary Lymph Node Dissection (ALND) such as arm lymphedema?"
        ),
        "options": [
            ("Sentinel Lymph Node Biopsy (SLNB) using radiolabeled Technetium-99m sulfur colloid and/or isosulfan blue dye", True, None),
            ("Routine complete Level I, II, and III axillary clearance in all patients", False, "Complete ALND is obsolete for clinically node-negative early breast cancer due to high lymphedema rates."),
            ("Blind axillary blind needle aspiration", False, "Blind aspiration has unacceptable false-negative rates."),
            ("Axillary external beam radiotherapy without surgical evaluation", False, "Surgical staging with SLNB is required before deciding on axillary radiation or clearance.")
        ],
        "pearl": "Sentinel Lymph Node Biopsy (SLNB): Sentinel node is the FIRST lymph node in the lymphatic basin to receive drainage from the primary tumor. If the sentinel node is negative on histopathology/frozen section, the remaining axillary nodes are >95% likely to be disease-free, sparing the patient Axillary Lymph Node Dissection (ALND) and preventing chronic upper extremity lymphedema. Dual tracer technique: Technetium-99m nanocolloid + Blue dye (Patent blue / Methylene blue).",
        "citation": "Sabiston Textbook of Surgery, 21st Ed, Chapter 34 (Breast), p. 842-858.",
        "difficulty": "moderate"
    }
]
