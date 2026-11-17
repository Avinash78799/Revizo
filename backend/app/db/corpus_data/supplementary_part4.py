"""
Supplementary High-Yield NEET-PG Clinical Questions: Part 4
Covers: Anatomy (6), Physiology (6), Biochemistry (6).
"""

SUPPLEMENTARY_PART4 = [
    # =========================================================================
    # --- ANATOMY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Anatomy",
        "concept_name": "Upper Limb Neuroanatomy: Radial Nerve Injuries & Spiral Groove",
        "stem": (
            "A 28-year-old motorcyclist sustains a closed midshaft fracture of the right humerus. On clinical examination, "
            "he is unable to extend his right wrist against gravity (complete wrist drop) and cannot extend his metacarpophalangeal joints "
            "(finger drop). He also exhibits sensory loss over the dorsal aspect of the first web space between the thumb and index finger. "
            "However, active extension of the elbow joint against resistance remains completely normal and triceps reflex (C7) is intact. "
            "What anatomical feature explains the selective preservation of elbow extension despite severe wrist drop?"
        ),
        "options": [
            ("The motor nerve branches supplying the long, lateral, and medial heads of the triceps brachii muscle originate from the radial nerve high in the axilla, proximal to the spiral (radial) groove", True, None),
            ("Elbow extension is predominantly mediated by the musculocutaneous nerve through the brachialis muscle", False, "The musculocutaneous nerve innervates coracobrachialis, biceps, and brachialis, which are elbow flexors, not extensors."),
            ("The deep branch of the radial nerve (posterior interosseous nerve) provides collateral motor innervation to the triceps", False, "The posterior interosseous nerve (PIN) innervates the extensor compartment of the forearm; it does not innervate the arm or triceps."),
            ("The anconeus muscle receives dual innervation from the ulnar nerve, maintaining full elbow extension", False, "Anconeus is innervated by the radial nerve; preservation of triceps is solely due to high axillary branches taking off proximal to the groove.")
        ],
        "pearl": "Radial Nerve Injuries by Anatomical Level: 1. INJURY IN THE AXILLA ('Saturday Night Palsy' / Crutch Palsy): Loss of TRICEPS (cannot extend elbow) + WRIST DROP (cannot extend wrist) + FINGER DROP (cannot extend MCP joints) + SENSORY LOSS over posterior arm, posterior forearm, and dorsal first web space (first 3.5 digits dorsum). Triceps reflex is ABSENT. 2. INJURY IN THE SPIRAL (RADIAL) GROOVE (Midshaft Humerus Fracture / Holstein-Lewis fracture): TRICEPS IS SPARED! (Branches to long and lateral heads of triceps arise in the axilla BEFORE entering the spiral groove). Features: WRIST DROP + FINGER DROP + SENSORY LOSS over dorsal first web space (superficial radial nerve). Triceps reflex is PRESERVED! 3. INJURY AT THE ELBOW / SUPINATOR CANAL (Posterior Interosseous Nerve [PIN] entrapment / Arcade of Frohse): NO WRIST DROP (Extensor carpi radialis longus [ECRL] is innervated proximal to bifurcation, so wrist extension with radial deviation is preserved!). FINGER DROP is present. SENSORY LOSS IS COMPLETELY ABSENT (PIN is purely motor!).",
        "citation": "BD Chaurasia's Human Anatomy, 8th Ed, Vol 1 (Upper Limb), Chapter 8; Gray's Anatomy, 42nd Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Anatomy",
        "concept_name": "Lower Limb Anatomy: Femoral Canal Boundaries & Hernia Strangulation",
        "stem": (
            "A 64-year-old multiparous female presents to the emergency department with severe, colicky lower abdominal pain, vomiting, "
            "and a tender, irreducible, walnut-sized mass in the right groin located INFERIOR AND LATERAL to the pubic tubercle. "
            "Emergency surgery reveals a strangulated loop of small bowel within the femoral canal. "
            "Which anatomical structure forms the sharp, rigid MEDIAL boundary of the femoral ring, responsible for the high incidence "
            "of irreducibility and ischemic strangulation in femoral hernias?"
        ),
        "options": [
            ("Lacunar Ligament of Gimbernat", True, None),
            ("Inguinal Ligament of Poupart", False, "The inguinal ligament forms the ANTERIOR boundary of the femoral ring, not the medial boundary."),
            ("Pectineal Ligament of Cooper", False, "The pectineal ligament lies POSTERIORLY on the pecten pubis, forming the posterior boundary of the femoral ring."),
            ("Femoral Vein covered by femoral sheath", False, "The femoral vein lies LATERALLY, separated by a thin fibrous septum from the femoral canal.")
        ],
        "pearl": "Femoral Sheath, Canal & Hernia Anatomy: 1. FEMORAL SHEATH: Formed by downward extension of abdominal fascia (Transversalis fascia anteriorly + Fascia iliaca posteriorly). Divided into 3 compartments: Lateral (Femoral Artery + femoral branch of genitofemoral nerve), Intermediate (Femoral Vein), and Medial (FEMORAL CANAL). Note: Femoral Nerve lies OUTSIDE and lateral to the femoral sheath in the femoral triangle! 2. FEMORAL CANAL: Conical medial space (~1.25 cm long). Contains: Fat, lymphatic vessels, and the Deep Inguinal Lymph Node of Cloquet / Rosenmüller. Base of canal = FEMORAL RING. 3. BOUNDARIES OF THE FEMORAL RING: Anterior: INGUINAL LIGAMENT (Poupart) | Posterior: PECTINEAL LIGAMENT (Cooper) on pecten pubis | Lateral: FEMORAL VEIN (separated by vertical septum) | Medial: LACUNAR LIGAMENT (Gimbernat). 4. SURGICAL PEARL: Femoral hernia is more common in females (wider female pelvis and femoral ring). It accounts for only ~5% of all groin hernias but carries the HIGHEST RISK OF STRANGULATION (up to 40%!) because of the sharp, unyielding crescentic edge of the LACUNAR LIGAMENT. When incising to relieve strangulation, beware of the ABERRANT / ABNORMAL OBTURATOR ARTERY ('Crown of Death' / Corona Mortis: enlarged anastomosis between inferior epigastric and obturator arteries crossing the lacunar ligament; nicking it causes fatal, catastrophic intra-pelvic hemorrhage!).",
        "citation": "BD Chaurasia's Human Anatomy, 8th Ed, Vol 2 (Lower Limb), Chapter 3, p. 55-68; Bailey & Love's Surgery, 28th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Anatomy",
        "concept_name": "Neuroanatomy: Cavernous Sinus Architecture & Septic Thrombosis",
        "stem": (
            "A 24-year-old male develops a furuncle (boil) on the philtrum of his upper lip ('danger area of the face'). He squeezes the lesion. "
            "Three days later, he presents with high spiking fevers, severe periorbital edema, bilateral proptosis, and chemosis. "
            "Cranial nerve examination reveals complete paralysis of the lateral rectus muscle of the right eye with inability to abduct "
            "the globe. Non-contrast CT and MR venography confirm septic cavernous sinus thrombosis. "
            "Which cranial nerve is MOST VULNERABLE to early damage in cavernous sinus thrombosis because it traverses FREE WITHIN THE LUMEN "
            "of the sinus alongside the internal carotid artery, rather than being protected within the lateral dural wall?"
        ),
        "options": [
            ("Abducens Nerve (Cranial Nerve VI)", True, None),
            ("Oculomotor Nerve (Cranial Nerve III)", False, "CN III runs embedded in the protective fibrous lateral wall of the cavernous sinus."),
            ("Trochlear Nerve (Cranial Nerve IV)", False, "CN IV runs embedded in the lateral wall below CN III, protected from direct luminal thrombosis."),
            ("Ophthalmic division of Trigeminal Nerve (CN V1)", False, "CN V1 runs embedded in the lower portion of the lateral wall of the cavernous sinus.")
        ],
        "pearl": "Cavernous Sinus Anatomy & Danger Area of Face: 1. VENOUS RELATIONS & SPREAD: Danger Area of the Face = Upper lip and lower part of nose/philtrum. Facial vein connects with Superior Ophthalmic Vein via Angular Vein, and with Pterygoid Venous Plexus via Deep Facial Vein. These veins are ENTIRELY VALVELESS! Squeezing boils in this zone drives septic thrombophlebitis retrograde into the CAVERNOUS SINUS. 2. STRUCTURES PASSING THROUGH THE CENTER / LUMEN OF THE SINUS: (A) INTERNAL CAROTID ARTERY (surrounded by sympathetic plexus) | (B) ABDUCENS NERVE (CN VI): Lies inferolateral to the internal carotid artery, bathed directly in venous blood inside the sinus cavity! It is the FIRST and MOST FREQUENTLY PARALYZED cranial nerve in cavernous sinus thrombosis or internal carotid aneurysm (causing lateral rectus palsy & medial strabismus/diplopia). 3. STRUCTURES EMBEDDED IN THE LATERAL DURAL WALL (Superior to Inferior): (A) Oculomotor Nerve (CN III) &rarr; (B) Trochlear Nerve (CN IV) &rarr; (C) Ophthalmic Nerve (CN V1) &rarr; (D) Maxillary Nerve (CN V2). (CRITICAL NOTE: Mandibular nerve CN V3 DOES NOT PASS THROUGH OR TOUCH THE CAVERNOUS SINUS; it exits skull through foramen ovale!).",
        "citation": "BD Chaurasia's Human Anatomy, 8th Ed, Vol 3 (Head and Neck), Chapter 14, p. 240-252; Gray's Anatomy, 42nd Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Anatomy",
        "concept_name": "Abdominal Anatomy: Epiploic Foramen (Winslow) & Pringle Maneuver",
        "stem": (
            "During an emergency exploratory laparotomy for a deep penetrating stab wound to the right upper abdomen, the trauma surgeon "
            "encounters torrential parenchymal hemorrhage from the liver. To achieve temporary vascular inflow occlusion (Pringle's Maneuver), "
            "the surgeon places an index finger through the Epiploic Foramen (Foramen of Winslow) and clamps the Hepatoduodenal Ligament "
            "with a vascular atraumatic clamp. "
            "What three vital structures are contained within the free anterior margin of the hepatoduodenal ligament, and what is their precise relative anatomical orientation?"
        ),
        "options": [
            ("Portal Vein posteriorly; Common Bile Duct anterior and to the right; Proper Hepatic Artery anterior and to the left", True, None),
            ("Inferior Vena Cava posteriorly; Right Hepatic Artery anteriorly; Common Hepatic Duct medially", False, "The Inferior Vena Cava forms the POSTERIOR boundary of the foramen of Winslow, not the content of the hepatoduodenal ligament!"),
            ("Portal Vein anteriorly; Proper Hepatic Artery posteriorly; Gastroduodenal Artery laterally", False, "The portal vein is the largest and most posterior structure of the portal triad."),
            ("Main Pancreatic Duct posteriorly; Superior Mesenteric Vein anteriorly; Celiac trunk medially", False, "These structures lie in the retroperitoneum behind the neck of the pancreas, not in the hepatoduodenal ligament.")
        ],
        "pearl": "Foramen of Winslow (Epiploic Foramen / Omental Foramen) & Pringle's Maneuver: 1. COMMUNICATION: The only communication between the Greater Peritoneal Sac and the Lesser Sac (Omental Bursa). 2. BOUNDARIES: Anterior: Free border of Lesser Omentum (HEPATODUODENAL LIGAMENT) containing the PORTAL TRIAD. Posterior: INFERIOR VENA CAVA (IVC) covered by peritoneum. Superior: CAUDATE LOBE of the liver. Inferior: 1st part of DUODENUM and horizontal part of hepatic artery. 3. ANATOMICAL ORIENTATION OF THE PORTAL TRIAD (High-Yield NEET-PG!): POSTERIOR: PORTAL VEIN (widest structure) | ANTERIOR-RIGHT: COMMON BILE DUCT (Duct on the Right!) | ANTERIOR-LEFT: PROPER HEPATIC ARTERY (Artery on the Left!). 4. PRINGLE'S MANEUVER: Clamping the hepatoduodenal ligament compresses the hepatic artery and portal vein, halting 100% of hepatic arterial and portal inflow. SURGICAL RULE: If heavy liver bleeding persists despite Pringle's clamping, the bleeding source is RETROHEPATIC IVC or MAJOR HEPATIC VEINS (which drain into IVC independently of the portal triad!).",
        "citation": "BD Chaurasia's Human Anatomy, 8th Ed, Vol 2 (Abdomen), Chapter 18, p. 270-285; Bailey & Love's Surgery, 28th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Anatomy",
        "concept_name": "Pelvic & Perineal Anatomy: Pudendal Nerve Block & Alcock Canal",
        "stem": (
            "An obstetrician prepares to perform an operative vacuum-assisted vaginal delivery with mediolateral episiotomy in a primigravida. "
            "To achieve complete perineal somatic anesthesia, a transvaginal Pudendal Nerve Block is performed. "
            "The obstetrician guides the needle along the index and middle fingers in the vagina. "
            "What bony landmark is palpated transvaginally to locate the pudendal nerve, and which ligament must the needle penetrate "
            "to anesthetize the nerve before it enters the pudendal (Alcock's) canal?"
        ),
        "options": [
            ("Ischial Spine; Sacrospinous Ligament", True, None),
            ("Ischial Tuberosity; Sacrotuberous Ligament", False, "The sacrotuberous ligament is large and more superficial; the pudendal nerve crosses the tip of the ischial spine and sacrospinous ligament."),
            ("Pectineal Eminence; Inguinal Ligament", False, "The pectineal eminence is anterior on the superior pubic ramus, distant from the perineal pudendal neurovascular bundle."),
            ("Posterior Inferior Iliac Spine; Sacroiliac Ligament", False, "The posterior iliac spine is posterior on the pelvis; the pudendal nerve block target is the ischial spine.")
        ],
        "pearl": "Pudendal Nerve Course & Block: 1. ROOT VALUE: Ventral rami of S2, S3, S4 (sacral plexus; 'S2, 3, 4 keep the poop off the floor'). 2. ANATOMICAL COURSE: Exits pelvis through the GREATER SCIATRIC FORAMEN (inferior to piriformis muscle) &rarr; crosses over the SACROSPINOUS LIGAMENT and the tip of the ISCHIAL SPINE &rarr; re-enters perineum through the LESSER SCIATIC FORAMEN &rarr; enters the PUDENDAL CANAL (Alcock's Canal, a fascial tunnel in the obturator fascia on the lateral wall of the ischioanal / ischiorectal fossa). 3. TERMINAL BRANCHES: (A) Inferior rectal nerve (external anal sphincter & perianal skin) | (B) Perineal nerve (scrotal/labial branches & perineal muscles) | (C) Dorsal nerve of the penis/clitoris. 4. PUDENDAL NERVE BLOCK PROCEDURE: Transvaginal approach: Palpate the ISCHIAL SPINE transvaginally with index finger. Pass guarded needle (Iowa trumpet) through vaginal mucosa and pierce the SACROSPINOUS LIGAMENT just medial and posterior to the ischial spine. Aspirate before injecting local anesthetic (Lidocaine 1%) to avoid intravascular injection into the internal pudendal artery!",
        "citation": "BD Chaurasia's Human Anatomy, 8th Ed, Vol 2 (Pelvis and Perineum), Chapter 26, p. 385-398; DC Dutta's Obstetrics, 9th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Anatomy",
        "concept_name": "Embryology: Pharyngeal (Branchial) Apparatus Derivatives & Anomalies",
        "stem": (
            "A 12-year-old child presents with a painless, smooth, fluctuant cystic mass located along the anterior border of the upper third "
            "of the sternocleidomastoid muscle, just anterior to the muscle and inferior to the angle of the mandible. "
            "Ultrasound confirms a well-circumscribed cystic lesion with internal cholesterol crystals (Branchial Cleft Cyst). "
            "Persistence of which embryological structure due to failure of normal developmental obliteration results in this congenital neck mass?"
        ),
        "options": [
            ("Cervical Sinus of His (formed by overgrowth of the 2nd pharyngeal arch over the 2nd, 3rd, and 4th pharyngeal clefts)", True, None),
            ("Thyroglossal Duct running from the foramen cecum to the thyroid isthmus", False, "Thyroglossal cysts are strictly MIDLINE neck masses that elevate characteristically on tongue protrusion and swallowing."),
            ("First Pharyngeal Cleft and Pouch anomaly (Eustachian tube precursor)", False, "First branchial cleft anomalies present close to the external auditory meatus or angle of the mandible, often with a fistula to the external ear canal."),
            ("Third and Fourth Pharyngeal Pouches forming thymic rests", False, "Pharyngeal pouches are internal endodermal derivatives; branchial cleft cysts arise from external ectodermal branchial clefts / cervical sinus.")
        ],
        "pearl": "Pharyngeal (Branchial) Apparatus Master Guide: 1. ARCHES (Mesoderm + Neural Crest): 1st Arch (Mandibular, CN V3): Muscles of mastication, mylohyoid, anterior digastric, tensor tympani, tensor veli palatini, Malleus, Incus, Meckel's cartilage. 2nd Arch (Hyoid, CN VII): Muscles of facial expression, posterior digastric, stylohyoid, Stapedius, Stapes, Styloid process, lesser horn of hyoid. 3rd Arch (CN IX): Stylopharyngeus, greater horn of hyoid, common & internal carotid arteries. 4th Arch (CN X, superior laryngeal): Cricothyroid, pharyngeal constrictors, thyroid cartilage, aortic arch / right subclavian. 6th Arch (CN X, recurrent laryngeal): Intrinsic laryngeal muscles (except cricothyroid), cricoid cartilage, pulmonary arteries & ductus arteriosus. 2. POUCHES (Endoderm): 1st: Middle ear cavity & Eustachian tube | 2nd: Palatine tonsil crypts | 3rd: INFERIOR PARATHYROID GLANDS & THYMUS | 4th: SUPERIOR PARATHYROID GLANDS & Ultimobranchial body (C cells). 3. CLEFTS (Ectoderm): 1st Cleft: External Auditory Meatus. 2nd, 3rd, 4th Clefts: Covered by the downward overgrowth of the 2nd arch to form the transient CERVICAL SINUS OF HIS. If the cervical sinus fails to obliterate &rarr; LATERAL BRANCHIAL CLEFT CYST (along anterior border of sternocleidomastoid!).",
        "citation": "Langman's Medical Embryology, 14th Ed, Chapter 17 (Head and Neck), p. 280-298; Inderbir Singh's Human Embryology, 12th Ed.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- PHYSIOLOGY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Physiology",
        "concept_name": "Cardiovascular Physiology: Jugular Venous Pulse (JVP) Waves & Canon Waves",
        "stem": (
            "A 68-year-old male with a history of anterior myocardial infarction presents with recurrent syncopal attacks. "
            "On physical examination, his arterial pulse is slow and regular at 36 bpm. Inspection of the internal jugular venous pulsations "
            "reveals intermittent, towering, massive pulsations ('Giant Cannon A-Waves') that shoot up to the angle of the jaw. "
            "ECG demonstrates complete atrioventricular (AV) dissociation with a ventricular escape rhythm of 36 bpm. "
            "What precise physiological event generates these 'Cannon A-Waves' in the jugular venous pulse?"
        ),
        "options": [
            ("Right atrial contraction occurring simultaneously against a closed tricuspid valve during ventricular systole", True, None),
            ("Massive systolic backflow of blood into the right atrium due to tricuspid valve regurgitation", False, "Tricuspid regurgitation produces giant 'V-waves' / 'C-V waves' (Lancisi's sign) during ventricular systole, not intermittent cannon A-waves."),
            ("Rapid early diastolic filling of a stiff, non-compliant right ventricle", False, "Rapid early diastolic filling generates a prominent 'y-descent' and S3 gallop, not an upward presystolic cannon wave."),
            ("Reversal of flow in the superior vena cava caused by constrictive pericarditis", False, "Constrictive pericarditis produces Kussmaul's sign and steep x and y descents ('Friedreich's sign'), not intermittent cannon A-waves.")
        ],
        "pearl": "Jugular Venous Pulse (JVP) Waves & Pathology: 1. NORMAL WAVES: 'a' wave: Presystolic, caused by RIGHT ATRIAL CONTRACTION (absent in Atrial Fibrillation!). 'c' wave: Ventricular isovolumetric contraction; bulging of tricuspid valve into right atrium. 'x' descent: Atrial relaxation & downward pulling of tricuspid floor by contracting ventricles. 'v' wave: Late systolic venous filling of right atrium against CLOSED tricuspid valve. 'y' descent: Tricuspid opening & rapid passive diastolic emptying of right atrium into ventricle. 2. ABNORMAL JVP PATTERNS (High-Yield NEET-PG!): A. CANNON A-WAVES: Occur when right atrium contracts against a CLOSED TRICUSPID VALVE &rarr; pressure wave reflected back into jugular veins! Regular Cannon Waves: Junctional rhythm / AVNRT / Ventricular pacing. Irregular / Intermittent Cannon Waves: COMPLETE (3rd DEGREE) HEART BLOCK (AV dissociation: atria and ventricles beat independently; whenever P-wave coincides with QRS/systole, a cannon wave erupts!) & Ventricular Tachycardia. B. GIANT V-WAVES: TRICUSPID REGURGITATION (systolic regurgitation jets back into atrium). C. STEEP Y-DESCENT (Friedreich's Sign): CONSTRICTIVE PERICARDITIS. D. SLOW / ABSENT Y-DESCENT: CARDIAC TAMPONADE (pericardial fluid impairs ventricular filling in early diastole!).",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 30 (Heart as a Pump); Guyton and Hall Textbook of Medical Physiology, 14th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Physiology",
        "concept_name": "Respiratory Physiology: Lung Volumes, FRC Measurement & Flow-Volume Loops",
        "stem": (
            "A clinical physiologist performs pulmonary function testing on a healthy 25-year-old male volunteer. "
            "Standard dry-rolling seal spirometry can measure Tidal Volume (TV), Inspiratory Reserve Volume (IRV), "
            "and Expiratory Reserve Volume (ERV). "
            "Which of the following lung volumes or capacities CANNOT be measured by direct spirometry and requires Helium Dilution "
            "or Whole-Body Plethysmography for accurate quantification?"
        ),
        "options": [
            ("Functional Residual Capacity (FRC), Residual Volume (RV), and Total Lung Capacity (TLC)", True, None),
            ("Vital Capacity (VC), Inspiratory Capacity (IC), and Tidal Volume (TV)", False, "Vital capacity, inspiratory capacity, and tidal volume are completely exhaled or inhaled and are directly measurable by spirometry."),
            ("Forced Expiratory Volume in 1 second (FEV1) and Peak Expiratory Flow Rate (PEFR)", False, "FEV1 and PEFR are dynamic timed volumes measured directly on standard spirometry and peak flow meters."),
            ("Inspiratory Reserve Volume (IRV) and Expiratory Reserve Volume (ERV)", False, "Both IRV and ERV are directly measured by spirometry with maximal effort breathing.")
        ],
        "pearl": "Lung Volumes, Capacities & Spirometry Rules: 1. CORE RULE: ANY LUNG VOLUME OR CAPACITY THAT CONTAINS THE RESIDUAL VOLUME (RV) CANNOT BE MEASURED BY SPIROMETRY! Because spirometry measures only the air that moves in and out of the mouth, the air remaining in the lungs after maximal expiration (Residual Volume) is unreachable. 2. UNMEASURABLE BY DIRECT SPIROMETRY: (A) Residual Volume (RV) | (B) Functional Residual Capacity (FRC = ERV + RV) | (C) Total Lung Capacity (TLC = VC + RV). METHODS TO MEASURE RV / FRC / TLC: (1) Helium Dilution Method (C1V1 = C2[V1+V2]; measures communicating gas only) | (2) Nitrogen Washout Method | (3) Body Plethysmography (Boyle's law P1V1=P2V2; GOLD STANDARD because it measures ALL thoracic gas, including non-communicating bullae!). 3. FUNCTIONAL RESIDUAL CAPACITY (FRC): Volume of gas in lungs at the end of normal tidal expiration (~2200-2400 mL). It is the RESTING EQUILIBRIUM POINT OF THE RESPIRATORY SYSTEM where the outward recoil of the chest wall exactly balances the inward elastic recoil of the lungs! 4. FLOW-VOLUME LOOPS: Obstructive (Asthma, COPD): FEV1/FVC < 0.70, scooped-out concave expiratory limb, increased RV and TLC. Restrictive (Pulmonary Fibrosis): FEV1/FVC normal or elevated (>0.75), narrow symmetrical 'witch's hat' loop, reduced TLC and FVC.",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 34 (Pulmonary Function); West's Respiratory Physiology, 11th Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Physiology",
        "concept_name": "Renal Physiology: Countercurrent Mechanism & Tubuloglomerular Feedback",
        "stem": (
            "During periods of severe physiological water deprivation, the human kidney can concentrate urine up to 1,200 mOsm/kg H2O. "
            "This hyperosmolar medullary gradient is established by the countercurrent multiplier mechanism in the loop of Henle. "
            "Which anatomical segment of the nephron acts as the PRIMARY COUNTERCURRENT MULTIPLIER by actively transporting sodium and chloride "
            "into the medullary interstitium while remaining completely IMPERMEABLE TO WATER?"
        ),
        "options": [
            ("Thick Ascending Limb of the Loop of Henle (TAL)", True, None),
            ("Thin Descending Limb of the Loop of Henle", False, "The thin descending limb is highly permeable to water via AQP-1 and completely impermeable to solutes/NaCl; it concentrates tubular fluid passively."),
            ("Proximal Convoluted Tubule (PCT)", False, "The PCT reabsorbs 65% of filtered NaCl and water isotonically (osmolality remains 300 mOsm/kg); it does not generate medullary hypertonicity."),
            ("Cortical Collecting Duct", False, "Cortical collecting duct reabsorbs water under ADH control into the cortex (where blood flow rapidly removes it), not the deep hyperosmolar medulla.")
        ],
        "pearl": "Renal Countercurrent Architecture Master Guide: 1. COUNTERCURRENT MULTIPLIER = LOOP OF HENLE: (A) Thick Ascending Limb (TAL): The active engine! Actively reabsorbs Na+, K+, and 2 Cl- via the NKCC2 cotransporter (inhibited by Loop Diuretics: Furosemide). CRUCIAL PROPERTY: COMPLETELY IMPERMEABLE TO WATER! Transports solute into the medullary interstitium without water, making the interstitium hyperosmolar and the luminal tubular fluid hypo-osmolar ('diluting segment'). (B) Thin Descending Limb: Highly permeable to water (via Aquaporin-1) and impermeable to solutes. Water leaves lumen into hypertonic medulla, concentrating luminal fluid to 1200 mOsm/kg at the hairpin turn. 2. COUNTERCURRENT EXCHANGER = VASA RECTA: Hairpin loops of peritubular capillaries in medulla. SLOW BLOOD FLOW preserves the medullary hypertonicity without washing it out (passive diffusion of water out and solutes in on descending side, reversed on ascending side). 3. UREA RECYCLING: Contributes ~50% of the medullary hyperosmolar gradient via UT-A1/UT-A3 transporters in inner medullary collecting ducts (stimulated by ADH / Vasopressin). 4. TUBULOGLOMERULAR FEEDBACK (TGF): Specialized Macula Densa cells in TAL/early DCT sense luminal NaCl delivery via NKCC2. High NaCl &rarr; ATP/Adenosine release &rarr; constricts AFFERENT ARTERIOLE &rarr; reduces GFR back to normal autoregulatory baseline.",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 37 (Renal Function); Guyton and Hall Medical Physiology, 14th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Physiology",
        "concept_name": "Neurophysiology: Nerve Action Potential, Ion Gates & Refractory Periods",
        "stem": (
            "During the recording of an intracellular action potential in a mammalian peripheral myelinated axon, a microelectrode detects "
            "a rapid depolarization phase from the resting membrane potential of -70 mV up to +35 mV, followed by rapid repolarization. "
            "During the initial phase of repolarization (between +35 mV and -50 mV), application of a supramaximal electrical stimulus "
            "fails completely to evoke a second action potential, regardless of stimulus strength. "
            "What physiological state defines this Absolute Refractory Period (ARP), and what molecular conformation of the voltage-gated "
            "sodium channel accounts for it?"
        ),
        "options": [
            ("Inactivation gate (h-gate) closure of the voltage-gated sodium channels; Channels are locked in an inactivated non-conducting state and cannot reopen until the membrane repolarizes to near resting potential", True, None),
            ("Activation gate (m-gate) closure with rapid opening of delayed rectifier chloride channels", False, "The activation m-gate is open during the upstroke; the inactivation h-gate closes at the peak to cause the absolute refractory period."),
            ("Persistent opening of hyperpolarizing sodium-calcium exchangers", False, "Na+/Ca2+ exchangers do not mediate the absolute refractory period of the action potential."),
            ("Exhaustion of intracellular ATP required to operate the Na+/K+-ATPase pump", False, "The Na+/K+ pump restores ionic gradients over thousands of cycles; a single action potential involves minimal ion shifts and does not exhaust ATP.")
        ],
        "pearl": "Action Potential Gates & Refractory Periods: 1. VOLTAGE-GATED SODIUM CHANNEL (Nav): Possesses TWO gates: Activation gate ('m-gate' on outer pore) and Inactivation gate ('h-gate' on intracellular loop). (A) Resting state (-70 mV): m-gate CLOSED, h-gate OPEN. Channel is ready to fire. (B) Depolarization / Upstroke (Threshold -55 mV): m-gate opens rapidly &rarr; massive inward Na+ current. (C) Peak (+30 to +35 mV): h-gate CLOSES RAPIDLY ('inactivation') &rarr; halts Na+ influx. Simultaneously, voltage-gated Delayed Rectifier K+ channels open &rarr; outward K+ efflux &rarr; Repolarization. 2. ABSOLUTE REFRACTORY PERIOD (ARP): Extends from threshold firing until approximately halfway through repolarization. During ARP, ALL Na+ channels are either already open or INACTIVATED (h-gate closed). NO STIMULUS, NO MATTER HOW STRONG, CAN GENERATE A SECOND ACTION POTENTIAL! Functional significance: Limits the maximum firing frequency of neurons and ENSURES UNIDIRECTIONAL (ORTHODROMIC) CONDUCTION of the action potential along the axon! 3. RELATIVE REFRACTORY PERIOD (RRP): Follows ARP until resting potential is restored. Some Na+ channels have reset to resting state (h-gate open, m-gate closed), but delayed K+ channels remain open (after-hyperpolarization). A SUPRAMAXIMAL STIMULUS CAN EVOKE AN ACTION POTENTIAL, but with lower amplitude and higher threshold.",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 4 (Excitable Tissue: Nerve); Guyton and Hall Medical Physiology, 14th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Physiology",
        "concept_name": "Gastrointestinal Physiology: Gastric Acid Secretion & Second Messengers",
        "stem": (
            "Gastric acid (HCl) secretion by parietal (oxyntic) cells in the gastric corpus and fundus is regulated by neural, hormonal, "
            "and paracrine pathways acting on cell surface receptors. "
            "Which of the following secretagogues acts specifically on parietal cells by stimulating Histamine H2 receptors, activating "
            "adenylyl cyclase, and elevating intracellular cyclic AMP (cAMP) to stimulate the luminal H+/K+-ATPase proton pump?"
        ),
        "options": [
            ("Histamine released from Enterochromaffin-Like (ECL) cells", True, None),
            ("Gastrin released from antral G cells acting via CCK-B receptors", False, "Gastrin acts via CCK-B receptors coupled to Gq &rarr; Phospholipase C &rarr; IP3/DAG &rarr; intracellular Calcium, NOT cAMP."),
            ("Acetylcholine released from postganglionic vagal efferents acting via M3 muscarinic receptors", False, "Acetylcholine acts via M3 receptors coupled to Gq &rarr; IP3/DAG &rarr; Calcium elevation, not the cAMP pathway."),
            ("Somatostatin released from antral D cells acting via SSTR2 receptors", False, "Somatostatin is an INHIBITORY paracrine hormone coupled to Gi, which DECREASES cAMP to inhibit acid secretion.")
        ],
        "pearl": "Gastric Acid Secretion & Parietal Cell Signal Transduction: Final Common Effector: Luminal H+/K+-ATPase ('Proton Pump') &mdash; pumps H+ into gastric lumen in exchange for K+ (potently and irreversibly blocked by Omeprazole, Pantoprazole). 1. THE THREE STIMULATORS OF ACID SECRETION: (A) HISTAMINE (Paracrine): Released from Enterochromaffin-Like (ECL) cells in lamina propria. Binds H2 RECEPTORS on parietal cells &rarr; Gs protein &rarr; activates ADENYLYL CYCLASE &rarr; INCREASES INTRACELLULAR cAMP &rarr; Protein Kinase A &rarr; activates proton pump. (Blocked by H2 blockers: Famotidine). (B) ACETYLCHOLINE (Neurocrine): Vagus nerve releases ACh &rarr; binds M3 MUSCARINIC RECEPTORS &rarr; Gq protein &rarr; activates Phospholipase C (PLC) &rarr; IP3/DAG &rarr; INCREASES INTRACELLULAR CALCIUM. (Blocked by Atropine). (C) GASTRIN (Endocrine): Antral G cells release Gastrin &rarr; binds CCK-B (CCK-2) RECEPTORS on parietal cells (& elevates Ca2+) AND on ECL cells (most potent physiologic action: stimulates ECL cells to release histamine!). 2. POTENTIATION PHENOMENON: Simultaneous activation of cAMP pathway (Histamine) and Ca2+ pathway (ACh/Gastrin) produces a synergistic response far greater than the sum of individual inputs! 3. INHIBITORS: Somatostatin (D cells, Gi-coupled &rarr; decreases cAMP) and Prostaglandin E2 (PGE2, Gi-coupled; NSAIDs block PGE2 synthesis &rarr; hypersecretion & ulcers!).",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 25 (Regulation of GI Function); Guyton and Hall Medical Physiology, 14th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Physiology",
        "concept_name": "Endocrine Physiology: Calcium Homeostasis, PTH & Calcitriol Actions",
        "stem": (
            "A 38-year-old female undergoes total thyroidectomy for multinodular goiter. On postoperative day 2, she develops perioral tingling, "
            "numbness in her fingertips, and painful carpopedal spasm upon inflation of the blood pressure cuff above systolic pressure (positive Trousseau's sign). "
            "Laboratory testing confirms severe acute hypocalcemia (serum ionized Ca2+ 0.72 mmol/L, total Ca2+ 6.8 mg/dL) and elevated serum phosphate (5.8 mg/dL) "
            "due to inadvertent devascularization of the parathyroid glands. "
            "In a healthy individual, which combination of direct physiological actions does Parathyroid Hormone (PTH) exert on the renal tubules?"
        ),
        "options": [
            ("Stimulates Calcium reabsorption in the Distal Convoluted Tubule, INHIBITS Phosphate reabsorption in the Proximal Convoluted Tubule (phosphaturic effect), and activates renal 1-alpha-hydroxylase", True, None),
            ("Stimulates both Calcium and Phosphate reabsorption in the proximal convoluted tubule", False, "PTH inhibits proximal tubular phosphate reabsorption to prevent precipitation of calcium phosphate salts in tissues."),
            ("Inhibits renal tubular calcium reabsorption while stimulating bone mineralization", False, "PTH stimulates renal calcium reabsorption and promotes osteoclastic bone resorption to elevate serum calcium."),
            ("Directly stimulates intestinal calcium transport without requiring active vitamin D metabolites", False, "PTH has zero direct action on the intestinal brush border; its gut effects are entirely mediated indirectly via Calcitriol synthesis in the kidney.")
        ],
        "pearl": "Parathyroid Hormone (PTH) & Calcium-Phosphate Homeostasis: Synthesized by CHIEF CELLS of parathyroid glands. Secretion triggered by hypocalcemia sensed by the G-protein coupled CALCIUM-SENSING RECEPTOR (CaSR; cinacalcet is a calcimimetic activating CaSR). DIRECT ACTIONS OF PTH: 1. RENAL TUBULES: (A) STIMULATES CALCIUM REABSORPTION in the Distal Convoluted Tubule (DCT via apical TRPV5 channels and basolateral NCX1) &rarr; reduces urinary calcium excretion. (B) INHIBITS PHOSPHATE REABSORPTION in the Proximal Convoluted Tubule (PCT) by internalizing and degrading Na+/Phosphate cotransporters (NaPi-2a/2c) &rarr; CAUSES MASSIVE PHOSPHATURIA! (Rule: 'PTH is Phosphaturic' &mdash; prevents metastatic CaHPO4 tissue calcification). (C) STIMULATES 1-ALPHA-HYDROXYLASE in the PCT &rarr; converts 25-OH-D3 (Calcidiol) to 1,25-(OH)2-D3 (CALCITRIOL / Active Vitamin D). 2. SKELETAL BONE: Binds receptors on OSTEOBLASTS &rarr; upregulates RANK-LIGAND (RANKL) &rarr; binds RANK on osteoclast precursors &rarr; stimulates OSTEOCLAST ACTIVATION & bone resorption &rarr; releases Ca2+ and PO4 into blood! 3. INTESTINAL TRACT: NO DIRECT ACTION! Acts INDIRECTLY via renal Calcitriol, which upregulates intestinal TRPV6, Calbindin-D9k, and PMCA1b to enhance gut absorption of both calcium and phosphate.",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 21 (Hormonal Control of Calcium); Guyton and Hall Medical Physiology, 14th Ed.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- BIOCHEMISTRY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Biochemistry",
        "concept_name": "Carbohydrate Metabolism: Pyruvate Dehydrogenase Complex & Cofactors",
        "stem": (
            "A 4-month-old infant presents with severe lactic acidosis, developmental regression, hypotonia, and microcephaly. "
            "Biochemical testing reveals markedly elevated blood lactate, pyruvate, and alanine, with a normal lactate-to-pyruvate ratio. "
            "Enzymatic assay confirms congenital deficiency of the E1 (alpha-subunit) of the Pyruvate Dehydrogenase (PDH) Complex. "
            "Which of the following dietary regimens is indicated to provide an alternative energy source for the brain while bypassing "
            "the defective glycolytic pathway without worsening lactic acid generation?"
        ),
        "options": [
            ("Ketogenic Diet high in fat and rich in purely ketogenic amino acids (Leucine and Lysine)", True, None),
            ("High-carbohydrate, low-fat diet supplemented with oral glucose polymers", False, "Carbohydrates generate pyruvate via glycolysis, which cannot enter the Krebs cycle and is shunted into lactic acid, causing fatal acidosis!"),
            ("High-protein diet enriched exclusively in glucogenic amino acids (Alanine and Glycine)", False, "Glucogenic amino acids are transaminated to pyruvate, directly exacerbating the severe lactic acidosis."),
            ("Diet completely restricted in branched-chain amino acids (Valine, Leucine, Isoleucine)", False, "BCAA restriction is the treatment for Maple Syrup Urine Disease (MSUD), not pyruvate dehydrogenase deficiency.")
        ],
        "pearl": "Pyruvate Dehydrogenase (PDH) Complex & Ketogenic Amino Acids: 1. REACTION & LOCALIZATION: Mitochondrial matrix enzyme complex that catalyzes the irreversible oxidative decarboxylation: Pyruvate + NAD+ + CoA &rarr; Acetyl-CoA + CO2 + NADH + H+. Bridges GLYCOLYSIS with the CITRIC ACID (KREBS) CYCLE! 2. THE 5 MANDATORY VITAMIN COFACTORS (Mnemonic: 'Tender Loving Care For Nancy'): (1) Thiamine pyrophosphate (TPP from Vitamin B1 &mdash; E1 subunit: pyruvate decarboxylase) | (2) Lipoic Acid / Lipoamide (E2 subunit &mdash; inhibited by Arsenic!) | (3) Coenzyme A (CoA from Pantothenic acid B5 &mdash; E2) | (4) FAD (from Riboflavin B2 &mdash; E3: dihydrolipoyl dehydrogenase) | (5) NAD+ (from Niacin B3 &mdash; E3). 3. PDH DEFICIENCY: X-linked dominant mutation in E1 alpha subunit. Pyruvate cannot convert to Acetyl-CoA &rarr; shunted to LACTATE (via LDH &rarr; severe congenital lactic acidosis) and ALANINE (via ALT). MANAGEMENT: KETOGENIC DIET! (Fat ratio 3:1 or 4:1). Fat-derived ketone bodies (Acetoacetate, Beta-hydroxybutyrate) and the PURELY KETOGENIC AMINO ACIDS &mdash; LEUCINE AND LYSINE &mdash; convert directly into Acetyl-CoA and Acetoacetyl-CoA without passing through pyruvate, providing ATP for brain tissue without generating lactic acid!",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 17 (Citric Acid Cycle); Lehninger Principles of Biochemistry, 8th Ed.",
        "difficulty": "hard"
    },
    {
        "subject": "Biochemistry",
        "concept_name": "Inborn Errors of Amino Acid Metabolism: PKU vs Alkaptonuria",
        "stem": (
            "A 5-day-old infant born via uncomplicated home delivery is evaluated. The child has fair skin, blond hair, and blue eyes "
            "(distinctly lighter than his unaffected dark-haired parents and siblings). The mother notes a strange, pungent, "
            "'mousy' or 'musty' odor clinging to his wet diapers. Serum testing confirms hyperphenylalaninemia (>20 mg/dL / 1200 mcmol/L). "
            "Quantitative enzyme assay reveals complete deficiency of Phenylalanine Hydroxylase (Classic PKU). "
            "In this patient, which amino acid becomes an CONDITIONALLY ESSENTIAL amino acid that must be supplied in the diet to prevent deficiency?"
        ),
        "options": [
            ("Tyrosine", True, None),
            ("Tryptophan", False, "Tryptophan is an independent essential amino acid; it is not synthesized from phenylalanine."),
            ("Methionine", False, "Methionine is a sulfur-containing essential amino acid; it is not downstream of phenylalanine hydroxylase."),
            ("Cysteine", False, "Cysteine is synthesized from methionine and serine via cystathionine beta-synthase; it is conditionally essential in homocystinuria, not PKU.")
        ],
        "pearl": "Phenylketonuria (PKU) & Inborn Errors of Phenylalanine: 1. CLASSIC PKU: Etiology: Autosomal recessive deficiency of PHENYLALANINE HYDROXYLASE (PAH, chromosome 12). (Rare variant: deficiency of Dihydropteridine Reductase or Tetrahydrobiopterin [BH4] synthesis). Reaction: Phenylalanine &rarr; Tyrosine (requires O2 and BH4). When PAH is blocked: Phenylalanine accumulates and is transaminated to PHENYLKETONES (Phenylpyruvate, Phenyllactate, Phenylacetate). 2. CLINICAL MANIFESTATIONS: (A) Severe progressive intellectual disability (IQ <50, microcephaly, seizures) | (B) MOUSY / MUSTY BODY ODOR (due to phenylacetate in sweat and urine) | (C) Hypopigmentation: Fair skin, blonde hair, blue eyes (excess phenylalanine competitively inhibits TYROSINASE, blocking melanin synthesis!). 3. NUTRITIONAL MANAGEMENT: (A) STRICT LIFELONG RESTRICTION of dietary phenylalanine (avoid meat, dairy, aspartame!) | (B) DIETARY SUPPLEMENTATION OF TYROSINE! Because phenylalanine cannot be hydroxylated to tyrosine, TYROSINE BECOMES A STRICTLY ESSENTIAL AMINO ACID! 4. ALKAPTONURIA: Deficiency of Homogentisate 1,2-Dioxygenase &rarr; homogentisic acid accumulates. URINE TURNS BLACK ON STANDING / ALKALINIZATION. Ochronosis (bluish-black cartilage deposits) and severe ochronotic arthropathy.",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 29 (Catabolism of Proteins); Robbins & Cotran Pathology, 10th Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Biochemistry",
        "concept_name": "Lipid Metabolism: Familial Hypercholesterolemia & Apolipoproteins",
        "stem": (
            "A 32-year-old male with no prior medical history suffers an acute anterior ST-elevation myocardial infarction. "
            "Physical examination reveals bilateral firm, nodular, non-tender thickening of the Achilles tendons (Tendon Xanthomas), "
            "bilateral xanthelasmas around the medial canthi, and a prominent premature corneal arcus. "
            "Fasting lipid profile demonstrates: Total Cholesterol 390 mg/dL, LDL Cholesterol 310 mg/dL, HDL Cholesterol 42 mg/dL, "
            "and Triglycerides 138 mg/dL (normal). His father and paternal uncle both died of sudden cardiac death before age 40. "
            "What genetic molecular defect causes this condition (Familial Hypercholesterolemia, Fredrickson Type IIa)?"
        ),
        "options": [
            ("Autosomal dominant loss-of-function mutation in the Low-Density Lipoprotein (LDL) Receptor gene, impairing receptor-mediated endocytosis of LDL by hepatocytes", True, None),
            ("Autosomal recessive deficiency of Lipoprotein Lipase (LPL) enzyme", False, "LPL deficiency causes Type I Hyperchylomicronemia with massive hypertriglyceridemia (>1000 mg/dL) and eruptive xanthomas, not elevated LDL or tendon xanthomas."),
            ("Homozygous mutation in Apolipoprotein E (ApoE2/E2)", False, "ApoE2 homozygosity causes Type III Dysbetalipoproteinemia, featuring palmar xanthomas and tuberoeruptive xanthomas with elevated IDL and chylomicron remnants."),
            ("Loss-of-function mutation in Apolipoprotein C-II preventing LPL activation", False, "ApoC-II deficiency mimics LPL deficiency with severe chylomicronemia and acute pancreatitis, not isolated LDL hypercholesterolemia.")
        ],
        "pearl": "Familial Hypercholesterolemia (FH / Type IIa) & Apolipoproteins: 1. GENETICS & PATHOGENESIS: Autosomal dominant (prevalence 1 in 250 in heterozygotes). Molecular causes: (A) Mutations in LDL RECEPTOR (LDLR, >85% of cases) &rarr; failure of hepatic clathrin-coated pit endocytosis of circulating LDL | (B) Familial defective ApoB-100 (ligand for LDLR) | (C) Gain-of-function mutations in PCSK9 (PCSK9 normally degrades LDL receptors; targeted by mAb inhibitors Evolocumab and Alirocumab!). 2. CLINICAL HALLMARKS: (A) Massive elevation of pure LDL-C (Heterozygotes: 250-450 mg/dL; Homozygotes: >600-1000 mg/dL) | (B) PREMATURE CORONARY ARTERY DISEASE (myocardial infarction in 30s-40s in heterozygotes, in childhood <10 yrs in homozygotes!) | (C) TENDON XANTHOMAS (nodular cholesterol deposits pathognomonic in ACHILLES TENDONS and extensor digitorum tendons!) | (D) Xanthelasma & Corneal arcus. 3. APOLIPOPROTEIN KEY ROLES: ApoB-100: Synthesized in liver; present on VLDL, IDL, LDL; binds LDL receptor. ApoB-48: Synthesized in intestine (via RNA editing of ApoB mRNA by cytidine deaminase); present on Chylomicrons. ApoA-1: Present on HDL; activates LCAT (Lecithin-Cholesterol Acyltransferase) for reverse cholesterol transport. ApoC-II: Activates Lipoprotein Lipase (LPL). ApoE: Mediates remnant uptake via LRP in liver.",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 25 (Lipid Transport & Storage); Braunwald's Heart Disease, 12th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Biochemistry",
        "concept_name": "Purine Metabolism: Gout, HGPRT & Lesch-Nyhan Syndrome",
        "stem": (
            "A 2-year-old boy is brought to the pediatric neurology clinic with severe global developmental delay, generalized choreoathetosis, "
            "and spastic diplegia. The mother is distressed because the child has developed severe, repetitive, uncontrollable compulsive "
            "self-mutilation, biting his lips, buccal mucosa, and fingertips until they bleed. "
            "She also reports discovering gritty, orange-colored 'sand' deposits staining the diapers since infancy. "
            "Serum uric acid is markedly elevated at 14.2 mg/dL. "
            "Deficiency of which enzyme in the purine salvage pathway is responsible for this X-linked recessive disorder (Lesch-Nyhan Syndrome)?"
        ),
        "options": [
            ("Hypoxanthine-Guanine Phosphoribosyltransferase (HGPRT)", True, None),
            ("Adenosine Deaminase (ADA)", False, "ADA deficiency impairs purine degradation, accumulating dATP which is toxic to lymphocytes, causing Severe Combined Immunodeficiency (SCID), not self-mutilation."),
            ("Xanthine Oxidase", False, "Xanthine oxidase converts hypoxanthine to xanthine and uric acid; its deficiency causes hypouricemia and xanthinuria, the opposite of hyperuricemia."),
            ("PRPP Synthetase loss-of-function", False, "PRPP synthetase hyperactivity can cause gout; loss of function reduces purine synthesis without self-mutilation.")
        ],
        "pearl": "Purine Salvage Pathway & Lesch-Nyhan Syndrome: 1. PURINE SALVAGE: Salvages preformed free purine bases (Hypoxanthine, Guanine, Adenine) to conserve cellular energy: (A) HGPRT: Hypoxanthine + PRPP &rarr; IMP; Guanine + PRPP &rarr; GMP. (B) APRT: Adenine + PRPP &rarr; AMP. 2. LESCH-NYHAN SYNDROME: Inheritance: X-LINKED RECESSIVE (males affected). Enzyme deficiency: HYPOXANTHINE-GUANINE PHOSPHORIBOSYLTRANSFERASE (HGPRT). Biochemical consequences: Purine bases cannot be salvaged &rarr; free hypoxanthine and guanine are shunted into PURINE DEGRADATION &rarr; massive overproduction of URIC ACID. Simultaneously, PRPP (phosphoribosyl pyrophosphate) levels soar, accelerating de novo purine synthesis! 3. CLINICAL TETRAD (Mnemonic: 'HGPRT'): (H) Hyperuricemia (juvenile gout, gouty nephropathy, ORANGE 'SAND' / sodium urate crystals in diapers) | (G) Gout | (P) Pissed off (COMPULSIVE AGGRESSIVE SELF-MUTILATION: lip and finger biting, head-banging) | (R) Retardation (intellectual disability) | (T) Tone/dystonia (choreoathetosis, spasticity). 4. GOUT CRYSTAL OPTICS: Monosodium Urate (MSU) crystals in joints: NEEDLE-SHAPED, STRONGLY NEGATIVE BIREFRINGENCE under polarized light microscopy (Yellow when aligned parallel to the compensator slow axis; Blue when perpendicular!).",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 33 (Metabolism of Purine & Pyrimidine Nucleotides); Nelson Pediatrics, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Biochemistry",
        "concept_name": "Nutritional Biochemistry: Vitamin B12 vs Folate & Spinal Degeneration",
        "stem": (
            "A 56-year-old strict vegan for 20 years presents with profound fatigue, symmetric numbness and paresthesias in both feet, "
            "and an unsteady 'slapping' gait that worsens in the dark. Physical examination reveals impaired proprioception and vibration "
            "sense up to the knees bilaterally, spasticity with hyperreflexia, and bilateral extensor plantar responses (positive Babinski sign). "
            "CBC demonstrates macrocytic anemia (Hemoglobin 8.1 g/dL, Mean Corpuscular Volume MCV 118 fL) with hypersegmented neutrophils (&ge;6 lobes). "
            "Serum testing confirms severe Vitamin B12 deficiency. "
            "Accumulation of which abnormal biochemical metabolite directly interferes with myelin sheath synthesis and induces Subacute "
            "Combined Degeneration (SCD) of the dorsal and lateral columns of the spinal cord?"
        ),
        "options": [
            ("Methylmalonic Acid (MMA) and its precursor Methylmalonyl-CoA", True, None),
            ("Homocysteine only, with normal methylmalonic acid levels", False, "Elevated homocysteine with normal methylmalonic acid is characteristic of pure FOLATE deficiency, which NEVER causes subacute combined degeneration!"),
            ("Orotic Acid and uracil crystals", False, "Orotic acid accumulates in Hereditary Orotic Aciduria (UMP synthase deficiency) and OTC deficiency, causing megaloblastic anemia refractory to B12/folate without neuropathy."),
            ("Figlu (Formiminoglutamic acid)", False, "Figlu excretion in urine occurs in Folate deficiency (histidine loading test), not Vitamin B12 deficiency.")
        ],
        "pearl": "Vitamin B12 (Cobalamin) vs Folate (B9) Biochemistry & Neuropathy: 1. THE TWO VITAMIN B12-DEPENDENT ENZYMATIC REACTIONS: (A) METHIONINE SYNTHASE (Homocysteine &rarr; Methionine): Requires Methylcobalamin and N5-methyl-THF. Transfers methyl group from N5-methyl-THF to homocysteine. When B12 is deficient, folate is trapped as N5-methyl-THF ('FOLATE TRAP'), impairing purine/thymidylate synthesis and causing MEGALOBLASTIC ANEMIA. (B) METHYLMALONYL-CoA MUTASE (L-Methylmalonyl-CoA &rarr; Succinyl-CoA): Requires Adenosylcobalamin. Essential for propionate catabolism from odd-chain fatty acids, isoleucine, valine, methionine, and threonine. When B12 is deficient, METHYLMALONIC ACID (MMA) ACCUMULATES! 2. PATHOPHYSIOLOGY OF SUBACUTE COMBINED DEGENERATION (SCD): Elevated methylmalonyl-CoA incorporates abnormal odd-carbon and branched fatty acids into neuronal myelin lipids &rarr; DESTRUCTION / DEMYELINATION OF DORSAL COLUMNS (loss of vibration and position sense) and LATERAL CORTICOSPINAL TRACTS (spasticity, paraparesis, hyperreflexia). 3. DIAGNOSTIC CRUX: B12 Deficiency: ELEVATED Methylmalonic Acid + ELEVATED Homocysteine + NEUROLOGICAL SYMPTOMS (SCD). Folate Deficiency: NORMAL Methylmalonic Acid + ELEVATED Homocysteine + ZERO NEUROLOGICAL SYMPTOMS! (Administering folate alone to a B12-deficient patient corrects the anemia but allows catastrophic irreversible neurological degeneration to progress!).",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 44 (Micronutrients: Vitamins & Minerals); Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Biochemistry",
        "concept_name": "Molecular Biology: DNA Polymerases, Telomerase & Nucleotide Excision Repair",
        "stem": (
            "An 8-year-old child presents with severe cutaneous photosensitivity, marked erythema, and blistering on minimal sun exposure, "
            "accompanied by diffuse poikiloderma, freckling, and multiple cutaneous squamous cell carcinomas on the face and neck. "
            "A defect in the Nucleotide Excision Repair (NER) pathway prevents the excision of which specific ultraviolet light-induced DNA lesions?"
        ),
        "options": [
            ("Intra-strand cross-linked Cyclobutane Pyrimidine Dimers (Thymine-Thymine dimers)", True, None),
            ("Guanine deamination resulting in spontaneous uracil mismatches", False, "Deaminated bases (e.g., uracil from cytosine) are excised by Base Excision Repair (BER) via DNA glycosylases, not NER."),
            ("Double-strand DNA breaks induced by ionizing radiation", False, "Double-strand breaks are repaired by Non-Homologous End Joining (NHEJ, deficient in ataxia telangiectasia) or Homologous Recombination (BRCA1/2)."),
            ("Microsatellite slippage loops generated during DNA polymerase replication", False, "Replication slippage and base mismatches are repaired by Mismatch Repair (MMR: MSH2, MLH1, deficient in Lynch syndrome).")
        ],
        "pearl": "DNA Repair Pathways & Human Genetic Syndromes: 1. NUCLEOTIDE EXCISION REPAIR (NER): Lesions repaired: BULKY, HELIX-DISTORTING LESIONS &mdash; primarily CYCLOBUTANE PYRIMIDINE DIMERS (Thymine dimers) induced by UV-B light, and bulky chemical carcinogen adducts. Mechanism: Endonuclease cleaves the damaged strand on both sides of the dimer, excising an oligonucleotide fragment of 24-32 nucleotides; DNA polymerase delta/epsilon fills the gap, and DNA ligase seals it. DEFECTIVE IN: XERODERMA PIGMENTOSUM (XP: extreme UV sensitivity, >2,000-fold increase in skin cancers [basal cell, squamous cell, melanoma] before age 20!). 2. BASE EXCISION REPAIR (BER): Lesions repaired: Non-bulky base damage (spontaneous deamination, oxidation, alkylation). Mechanism ('GEL-P'): DNA Glycosylase removes damaged base &rarr; AP Endonuclease cleaves 5' end of AP site &rarr; Lyase cleaves 3' end &rarr; DNA Polymerase beta &rarr; Ligase. 3. MISMATCH REPAIR (MMR): Corrects erroneous unmethylated daughter strand mismatches during S-phase replication. Defective in: LYNCH SYNDROME (HNPCC). 4. NON-HOMOLOGOUS END JOINING (NHEJ): Repairs double-strand breaks without homology. Defective in: ATAXIA TELANGIECTASIA (ATM gene) & Fanconi Anemia.",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 35 (DNA Organization, Replication & Repair); Lehninger Principles of Biochemistry, 8th Ed.",
        "difficulty": "easy"
    }
]
