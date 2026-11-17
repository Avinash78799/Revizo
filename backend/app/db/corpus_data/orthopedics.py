"""
Authentic High-Yield NEET-PG Clinical Questions for Orthopedics
References: Maheshwari's Essential Orthopaedics (7th Ed), Apley & Solomon's System of Orthopaedics (10th Ed)
"""

ORTHOPEDICS_QUESTIONS = [
    {
        "concept_name": "Core Principles: Upper Limb Fractures (Colles, Smith, Galeazzi, Monteggia)",
        "stem": (
            "A 62-year-old postmenopausal woman presents to the emergency room with severe right wrist pain and deformity after slipping on an icy pavement "
            "and landing heavily on her dorsiflexed outstretched hand. On physical examination, the wrist demonstrates a classic 'dinner fork deformity' "
            "with dorsal tilt, dorsal displacement, and radial deviation of the distal radius fragment. "
            "There is no neurovascular deficit. What is the diagnosis and the classic displacement deformity characteristic of this injury?"
        ),
        "options": [
            ("Colles fracture; dorsal tilt and dorsal displacement of the distal radial articular fragment", True, None),
            ("Smith fracture; volar displacement of the distal radial fragment (garden spade deformity)", False, "Smith fracture (reverse Colles) occurs from a fall onto a flexed wrist with volar displacement."),
            ("Barton fracture; intra-articular fracture-subluxation of the radiocarpal joint with volar rim displacement", False, "Barton fracture is an intra-articular fracture-subluxation of the distal radius."),
            ("Chauffeur fracture; isolated avulsion fracture of the radial styloid process", False, "Chauffeur (Hutchinson) fracture is an isolated intra-articular fracture of the radial styloid.")
        ],
        "pearl": "Distal Radius Fractures: Colles Fracture: Fall on outstretched hand (FOOSH), distal fragment displaced DORSALLY and SUPINATED ('dinner fork deformity'). Commonest complication: Malunion. Smith Fracture: Reverse Colles, fall on flexed wrist, distal fragment displaced VOLARLY ('garden spade deformity').",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 5 (Injuries of the Upper Limb), p. 74-82.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Upper Limb Fractures (Colles, Smith, Galeazzi, Monteggia)",
        "stem": (
            "A 28-year-old male motorcyclist is struck by a car and sustains a fracture of the upper third of the ulnar shaft accompanied by dislocation of the radial head. "
            "Which named fracture-dislocation complex does this represent, and which peripheral nerve is at the highest risk of iatrogenic or traumatic injury?"
        ),
        "options": [
            ("Monteggia fracture-dislocation; Posterior Interosseous Nerve (PIN, deep branch of radial nerve)", True, None),
            ("Galeazzi fracture-dislocation; Anterior Interosseous Nerve (AIN)", False, "Galeazzi is a fracture of the distal third of radius with DRUJ (distal radioulnar joint) dislocation."),
            ("Essex-Lopresti fracture; Ulnar nerve at the cubital tunnel", False, "Essex-Lopresti is a comminuted radial head fracture with interosseous membrane disruption and DRUJ dislocation."),
            ("Nightstick fracture; Superficial branch of radial nerve", False, "Nightstick fracture is an isolated fracture of the ulnar shaft without dislocation.")
        ],
        "pearl": "MUGR Mnemonic: Monteggia = Ulnar shaft fracture + Proximal radial head dislocation (Nerve at risk: Posterior Interosseous Nerve [PIN] -> finger drop without wrist drop). Galeazzi = Radius shaft fracture (junction of middle & distal third) + Distal Radioulnar Joint (DRUJ) dislocation (Nerve at risk: AIN or Ulnar nerve).",
        "citation": "Apley & Solomon's System of Orthopaedics, 10th Ed, Chapter 24, p. 712-720.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Hip Fractures: Intracapsular vs Extracapsular",
        "stem": (
            "A 74-year-old woman with a history of osteoporosis trips over a rug at home and falls onto her right hip. "
            "She is unable to bear weight and is brought to the orthopedic casualty. Physical examination reveals that the right lower extremity is "
            "shortened and EXTERNALLY ROTATED by approximately 45 degrees. Anteroposterior pelvis radiograph demonstrates a displaced intracapsular fracture of the femoral neck (Garden Stage IV). "
            "What is the primary vascular supply to the femoral head that is disrupted in this displaced fracture, predisposing to avascular necrosis (AVN)?"
        ),
        "options": [
            ("Medial circumflex femoral artery (retinacular branches)", True, None),
            ("Obturator artery branch to the ligamentum teres", False, "Artery of ligamentum teres supplies only a small area near the fovea capitis in adults and is insufficient alone to prevent AVN."),
            ("Deep femoral artery perforators", False, "Perforating arteries supply the shaft of the femur, not the femoral head."),
            ("Inferior gluteal artery", False, "Inferior gluteal artery contributes to the cruciate anastomosis, not the direct retinacular supply.")
        ],
        "pearl": "Femoral Head Blood Supply & Hip Fractures: Main blood supply: Retinacular vessels derived from the Medial Circumflex Femoral Artery. Intracapsular (subcapital/transcervical) fractures tear these vessels -> HIGH risk of Avascular Necrosis (AVN) and Non-union. Treatment in elderly: Hemiarthroplasty or Total Hip Arthroplasty (THA). Extracapsular (intertrochanteric) fractures have rich cancellous blood supply; treated with Dynamic Hip Screw (DHS) or Proximal Femoral Nail (PFN).",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 9 (Hip Fractures), p. 112-124.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Hip Fractures: Intracapsular vs Extracapsular",
        "stem": (
            "An 80-year-old male presents with severe right groin pain and inability to walk after a fall. On physical examination, the right leg is "
            "markedly shortened and EXTREMELY externally rotated (almost 90 degrees, resting on the examination couch). Pelvic X-ray reveals a multi-fragmentary "
            "intertrochanteric fracture. Why is the external rotation deformity significantly more exaggerated in an intertrochanteric fracture compared to a subcapital neck of femur fracture?"
        ),
        "options": [
            ("Because the entire iliopsoas tendon is completely severed", False, "Iliopsoas is not severed; it exerts strong external rotation on the proximal fragment."),
            ("Because the fracture line is extracapsular, freeing the distal shaft from the restraining iliofemoral ligament (Bigelow's ligament) and allowing gravity/psoas to externally rotate the limb", True, None),
            ("Because of complete spasm of the gluteus medius and minimus muscles", False, "Gluteus medius and minimus are abductors and internal rotators, not external rotators."),
            ("Because of associated disruption of the posterior cruciate ligament in the knee", False, "The knee ligaments are uninvolved.")
        ],
        "pearl": "Hip Fracture Physical Signs: Intracapsular (Neck of Femur): Moderate external rotation (45 degrees) because the intact hip capsule (iliofemoral ligament) limits further rotation. Extracapsular (Intertrochanteric): Marked external rotation (nearly 90 degrees, limb rests on lateral border of foot) because the fracture lies outside the capsule constraint.",
        "citation": "Apley & Solomon's System of Orthopaedics, 10th Ed, Chapter 27, p. 835-842.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Compartment Syndrome Diagnosis & Fasciotomy",
        "stem": (
            "A 22-year-old male sustains a closed, displaced fracture of the tibial shaft in a motorcycle accident. The limb is immobilized in a full-leg plaster cast. "
            "Six hours later, the patient develops excruciating calf pain that is unremitting and completely out of proportion to the injury, requiring repeated doses of intravenous morphine. "
            "Passive extension of the great toe elicits severe, intolerable pain in the anterior compartment. Distal dorsalis pedis and posterior tibial pulses are still palpable. "
            "Intra-compartmental pressure monitoring reveals an anterior compartment pressure of 42 mmHg (diastolic blood pressure is 68 mmHg, Delta P = 26 mmHg). "
            "What is the single most urgent and mandatory next step in management?"
        ),
        "options": [
            ("Administer intravenous Mannitol and elevate the affected leg above heart level", False, "Elevating the leg above heart level reduces arterial perfusion pressure and worsens compartment ischemia!"),
            ("Immediate emergency two-incision four-compartment fasciotomy of the leg", True, None),
            ("Apply local ice packs and increase the intravenous opioid infusion rate", False, "Analgesia and ice delay surgical decompression and lead to irreversible muscle necrosis and Volkmann contracture."),
            ("Order an urgent Doppler ultrasound of lower extremity arteries", False, "Pulses are classically PRESERVED until late irreversible necrosis; relying on pulse absence is a fatal mistake.")
        ],
        "pearl": "Acute Compartment Syndrome: EARLIEST & MOST SENSITIVE SIGN: Pain out of proportion to injury, exacerbated by PASSIVE stretch of compartment muscles. Cardinal rule: Peripheral pulses are PRESERVED until late irreversible necrosis! Diagnostic threshold: Absolute pressure >30 mmHg OR Delta P (Diastolic BP - Compartment Pressure) < 30 mmHg. DEFINITIVE TREATMENT: Emergency Fasciotomy of all involved compartments (never elevate leg above heart!).",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 3 (Complications of Fractures), p. 38-44.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Compartment Syndrome Diagnosis & Fasciotomy",
        "stem": (
            "Following an untreated high-energy supracondylar fracture of the humerus with brachial artery entrapment, a 7-year-old child develops "
            "Volkmann's Ischemic Contracture (VIC). Which deep muscle in the anterior compartment of the forearm is the most sensitive to ischemia "
            "and most severely affected in this condition?"
        ),
        "options": [
            ("Pronator teres", False, "Pronator teres is a superficial muscle, less severely involved than deep flexors."),
            ("Flexor digitorum profundus (FDP) and Flexor pollicis longus (FPL)", True, None),
            ("Brachioradialis", False, "Brachioradialis is in the mobile wad, innervated by the radial nerve and rarely infarcted in VIC."),
            ("Extensor digitorum communis", False, "Extensors are in the posterior compartment; VIC primarily affects the deep anterior flexor compartment.")
        ],
        "pearl": "Volkmann Ischemic Contracture (VIC): Caused by unaddressed compartment syndrome of the forearm following supracondylar humerus fracture. Most vulnerable muscles: Flexor Digitorum Profundus (FDP) and Flexor Pollicis Longus (FPL). Most vulnerable nerve: Median nerve. Results in flexion deformity of wrist, hyperextension of MCP joints, and flexion of IP joints ('Volkmann claw').",
        "citation": "Apley & Solomon's System of Orthopaedics, 10th Ed, Chapter 24, p. 705-710.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Osteosarcoma vs Ewing Sarcoma Radiological Signs",
        "stem": (
            "A 16-year-old athletic male presents with persistent pain and localized swelling around his right distal thigh for 2 months, which wakes him from sleep at night. "
            "Plain radiograph of the right distal femur demonstrates a mixed radiodense and radiolucent lesion centered in the METAPHYSIS, with cortical destruction, "
            "periosteal elevation forming a triangular shell of reactive new bone (Codman's triangle), and prominent spicules of bone radiating perpendicular to the cortex ('sunburst' appearance). "
            "Serum alkaline phosphatase (ALP) and lactate dehydrogenase (LDH) are elevated. What is the most likely diagnosis?"
        ),
        "options": [
            ("Osteosarcoma (Osteogenic Sarcoma)", True, None),
            ("Ewing Sarcoma", False, "Ewing sarcoma occurs in the DIAPHYSIS of long bones and characteristically exhibits an 'onion-skin' concentric lamellated periosteal reaction."),
            ("Osteochondroma", False, "Osteochondroma is a benign exostosis projecting away from the joint with cortex and medullary cavity continuous with parent bone."),
            ("Giant Cell Tumor (Osteoclastoma)", False, "Giant cell tumor occurs strictly in the EPIPHYSIS after physeal closure and presents as an eccentric, 'soap-bubble' lytic lesion without periosteal reaction.")
        ],
        "pearl": "Bone Tumors Location & Radiology: Osteosarcoma: Metaphysis, Age 10-20 yrs, 'Sunburst' appearance + Codman's triangle, produces osteoid. Ewing Sarcoma: Diaphysis, Age 5-15 yrs, small round blue cells (t(11;22)), 'Onion-skin' periosteal reaction. Giant Cell Tumor (GCT): Epiphysis, Age 20-40 yrs, 'Soap-bubble' appearance, eccentric, no sclerotic rim.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 24 (Bone Tumours), p. 278-290.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Osteosarcoma vs Ewing Sarcoma Radiological Signs",
        "stem": (
            "An 11-year-old boy presents with intermittent fever, localized pain, warmth, and firm swelling over the mid-shaft of his right femur for 6 weeks. "
            "Erythrocyte sedimentation rate (ESR) is 78 mm/hr and WBC count is 14,500/uL. Radiograph reveals a permeative lytic lesion in the DIAPHYSIS "
            "with prominent concentric, multi-layered 'onion-skin' periosteal reaction. Core needle biopsy demonstrates sheets of uniform, small, round, blue cells "
            "with periodic acid-Schiff (PAS) positive glycogen granules in the cytoplasm. Cytogenetic analysis is positive for which characteristic reciprocal translocation?"
        ),
        "options": [
            ("t(9;22)(q34;q11)", False, "t(9;22) is the Philadelphia chromosome characteristic of Chronic Myeloid Leukemia (BCR-ABL1)."),
            ("t(11;22)(q24;q12) producing the EWSR1-FLI1 fusion transcript", True, None),
            ("t(8;14)(q24;q32)", False, "t(8;14) involves c-MYC and Ig heavy chain in Burkitt Lymphoma."),
            ("t(14;18)(q32;q21)", False, "t(14;18) involves BCL-2 in Follicular Lymphoma.")
        ],
        "pearl": "Ewing Sarcoma Translocation & Pathology: Translocation: t(11;22)(q24;q12) in 85-90% of cases, creating the EWSR1-FLI1 fusion oncoprotein. Histology: Small round blue cell tumor, PAS positive (glycogen-rich cytoplasm), CD99 (MIC-2) positive membrane staining. Mimics osteomyelitis with fever and elevated ESR.",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 26 (Bones and Joints), p. 1198-1204.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Acute Osteomyelitis in Children",
        "stem": (
            "A 6-year-old boy presents with high fever, chills, and refusal to bear weight on his right lower extremity for 3 days. "
            "Physical examination reveals marked localized tenderness, warmth, and edema over the proximal tibial metaphysis. "
            "The adjacent knee joint has full active and passive range of motion without effusion. Blood cultures are drawn. "
            "What is the single most common causative microbiological pathogen responsible for acute hematogenous osteomyelitis in this pediatric age group?"
        ),
        "options": [
            ("Staphylococcus aureus", True, None),
            ("Pseudomonas aeruginosa", False, "Pseudomonas is seen characteristically in puncture wounds through rubber sneakers or in intravenous drug users."),
            ("Salmonella enteritidis", False, "Salmonella is classic in patients with Sickle Cell Disease, but S. aureus remains overall most common in normal children."),
            ("Neisseria gonorrhoeae", False, "Gonococcus causes septic arthritis in sexually active adolescents/young adults.")
        ],
        "pearl": "Acute Hematogenous Osteomyelitis: Most common organism overall in all age groups: Staphylococcus aureus. Most common site in children: Metaphysis of long bones (lower end of femur, upper end of tibia) due to sluggish blood flow in hairpin capillary loops. Sickle Cell Disease: Salmonella; Neonates: Group B Streptococcus and S. aureus; Puncture wounds through sneakers: Pseudomonas.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 15 (Infections of Bones and Joints), p. 165-174.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Acute Osteomyelitis in Children",
        "stem": (
            "In chronic osteomyelitis resulting from inadequately treated acute bone infection, radiographs demonstrate a dense, sclerotic, detached island "
            "of non-viable necrotic dead bone surrounded by a sheath of vascular reactive new periosteal bone. "
            "What are the precise pathological terms for this dead bone fragment and the surrounding new bone envelope, respectively?"
        ),
        "options": [
            ("Sequestrum and Involucrum", True, None),
            ("Involucrum and Cloaca", False, "Involucrum is the new bone; cloaca is the drainage opening in the involucrum."),
            ("Sequestrum and Cloaca", False, "Cloaca is the cortical defect allowing pus discharge."),
            ("Callus and Osteoid", False, "Callus and osteoid refer to fracture healing and bone matrix, not necrotic osteomyelitis pathology.")
        ],
        "pearl": "Chronic Osteomyelitis Pathological Triad: 1. Sequestrum: A piece of dead, devascularized cortical bone (appears hyperdense on X-ray due to absence of vascular resorption) | 2. Involucrum: Sheath of new reactive bone formed by periosteum around the sequestrum | 3. Cloaca: Opening in the involucrum through which pus discharges to form a sinus tract.",
        "citation": "Apley & Solomon's System of Orthopaedics, 10th Ed, Chapter 4 (Infections), p. 88-96.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Tuberculosis of Spine (Pott's Disease)",
        "stem": (
            "A 34-year-old male presents with chronic dull low back pain for 5 months, low-grade evening fevers, night sweats, and a 7-kg weight loss. "
            "On spinal examination, there is localized tenderness and a prominent sharp, angular kyphotic knuckle (gibbus) in the lower thoracic spine. "
            "Neurological examination reveals hyperreflexia and ankle clonus in both lower extremities. Magnetic resonance imaging (MRI) shows narrowing of the "
            "T9-T10 intervertebral disc space with destruction of adjacent anterior vertebral bodies and a prevertebral cold abscess. "
            "What is the most characteristic anatomical pattern of tuberculous spinal involvement seen in Pott's spine?"
        ),
        "options": [
            ("Paradiscal involvement affecting adjacent halves of two contiguous vertebrae and the intervening intervertebral disc", True, None),
            ("Isolated posterior element destruction of spinous processes sparing vertebral bodies", False, "Tuberculosis typically destroys anterior vertebral bodies and spares posterior elements initially; posterior involvement is seen in ~5%."),
            ("Diffuse skip lesions involving only alternate intervertebral discs without bony erosion", False, "TB is primarily an osseous disease destroying the anterior subchondral bone before disc necrosis occurs."),
            ("Hypertrophic bony ankylosis of facet joints with syndesmophyte formation", False, "Syndesmophytes and facet ankylosis are characteristic of Ankylosing Spondylitis (bamboo spine), not TB.")
        ],
        "pearl": "Tuberculosis of Spine (Pott's Disease): Most common type: PARADISCAL type (affects contiguous subchondral bone of 2 adjacent vertebrae + intervening disc). Most common site: Lower thoracic & thoracolumbar spine. Cold Abscess: Lacks signs of acute inflammation (Psoas abscess tracks along psoas sheath below inguinal ligament). Gibbus: Sharp angular kyphosis due to collapse of anterior wedged vertebral bodies. Earliest MRI sign: T2 hyperintensity and disc space narrowing.",
        "citation": "Maheshwari's Essential Orthopaedics, 7th Ed, Chapter 17 (Tuberculosis of Bones and Joints), p. 192-206.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Tuberculosis of Spine (Pott's Disease)",
        "stem": (
            "A patient with advanced Pott's paraplegia due to lower thoracic tuberculous spondylodiscitis presents with progressive spastic paraparesis. "
            "Which of the following constitutes an absolute indication for emergency surgical decompression (anterolateral decompression and stabilization) "
            "over conservative anti-tubercular therapy alone?"
        ),
        "options": [
            ("Rapidly deteriorating neurological deficit, bowel/bladder sphincter dysfunction, or dense paraplegia unresponsive to medical therapy", True, None),
            ("Presence of an asymptomatic cold abscess in the lumbar region without neurodeficit", False, "Asymptomatic cold abscesses can be treated medically or aspirated under ultrasound guidance."),
            ("Elevated erythrocyte sedimentation rate (ESR >70 mm/hr)", False, "Elevated ESR is an inflammatory marker expected in TB and monitored for response to medical therapy."),
            ("Persistent low-grade fever during the first 2 weeks of ATT", False, "Fever often takes several weeks to resolve under ATT and is not an indication for major spinal surgery.")
        ],
        "pearl": "Pott's Paraplegia Surgical Indications (Griffiths Classification): Absolute surgical indications: 1. Onset of paraplegia during ATT (medical failure) | 2. Rapidly progressive motor weakness or paraplegia in flexion | 3. Sphincter involvement (urinary retention/incontinence) | 4. Severe spinal instability or gross kyphotic deformity.",
        "citation": "Apley & Solomon's System of Orthopaedics, 10th Ed, Chapter 21 (The Spine), p. 612-622.",
        "difficulty": "hard"
    }
]
