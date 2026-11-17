"""
Authentic High-Yield NEET-PG Clinical Questions for Anatomy
References: B.D. Chaurasia's Human Anatomy (8th Ed), Gray's Anatomy for Students (4th Ed)
"""

ANATOMY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Brachial Plexus & Nerve Injuries",
        "stem": (
            "A difficult breech delivery in a newborn male results in excessive lateral traction on the fetal head and neck, "
            "widening the angle between the head and shoulder. Physical examination of the newborn demonstrates a flaccid left upper extremity "
            "hanging limply by the side: the shoulder is adducted and internally rotated, the elbow is fully extended, the forearm is pronated, "
            "and the wrist is partially flexed ('waiter's tip' or 'policeman's tip' posture). "
            "Biceps reflex is absent, but the grasp reflex of the hand is fully intact. "
            "Which roots / trunks of the brachial plexus are torn or avulsed in this injury (Erb's Palsy)?"
        ),
        "options": [
            ("C5 and C6 nerve roots (Upper Trunk of Brachial Plexus at Erb's Point)", True, None),
            ("C8 and T1 nerve roots (Lower Trunk of Brachial Plexus)", False, "C8-T1 injury produces Klumpke's palsy ('true claw hand' with intrinsic hand muscle paralysis + Horner's syndrome)."),
            ("C7 nerve root alone", False, "Isolated C7 lesion causes triceps weakness and sensory loss over the middle finger without the waiter's tip posture."),
            ("Posterior cord of the brachial plexus", False, "Posterior cord injury causes wrist drop (radial) and deltoid paralysis (axillary).")
        ],
        "pearl": "Brachial Plexus Birth Injuries: 1. ERB-DUCHENNE PALSY: Cause: Injury to UPPER TRUNK (C5, C6 roots) at Erb's point (junction of 6 nerves: C5 root, C6 root, suprascapular n., n. to subclavius, anterior division, posterior division). Muscles paralyzed: Deltoid, Biceps brachii, Brachialis, Brachioradialis, Supraspinatus, Infraspinatus, Supinator. Posture: WAITER'S TIP / POLICEMAN'S TIP (Adducted shoulder, Internally rotated arm, Extended elbow, Pronated forearm, Flexed wrist). Grasp reflex PRESERVED. 2. KLUMPKE'S PALSY: Cause: Upward traction on arm injuring LOWER TRUNK (C8, T1). Muscles: All intrinsic muscles of hand paralyzed -> TOTAL CLAW HAND + Horner Syndrome (ptosis, miosis, anhidrosis due to T1 sympathetic root injury).",
        "citation": "B.D. Chaurasia's Human Anatomy, 8th Ed, Vol 1 (Upper Limb), Chapter 4 (Brachial Plexus), p. 58-68.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Brachial Plexus & Nerve Injuries",
        "stem": (
            "A 24-year-old motorcyclist sustains a closed spiral fracture of the middle third of the humeral shaft. "
            "On physical examination, he is unable to extend his wrist, thumb, and metacarpophalangeal (MCP) joints (Wrist Drop), "
            "and has sensory loss over the dorsal aspect of the first web space (anatomical snuffbox). "
            "Which peripheral nerve is injured, and through which anatomical groove on the posterior surface of the humerus does it travel?"
        ),
        "options": [
            ("Radial Nerve in the Radial (Spiral) Groove of the humerus, accompanied by the Profunda Brachii Artery", True, None),
            ("Axillary Nerve around the surgical neck of the humerus", False, "Axillary nerve wraps around the surgical neck with the posterior circumflex humeral artery, paralyzing the deltoid and causing sensory loss over the 'regimental badge' area."),
            ("Ulnar Nerve behind the medial epicondyle of the humerus", False, "Ulnar nerve passes behind the medial epicondyle, causing ulnar claw hand and sensory loss on the medial 1.5 digits."),
            ("Median Nerve passing anterior to the elbow joint", False, "Median nerve runs anteromedially with the brachial artery in the cubital fossa.")
        ],
        "pearl": "Humerus Fractures & Peripheral Nerve Injuries: 1. Surgical Neck Fracture: AXILLARY NERVE (Deltoid atrophy, flat shoulder, loss of sensation over regimental badge area / lateral deltoid). Accompanied by Posterior Circumflex Humeral Artery. 2. Midshaft / Spiral Groove Fracture: RADIAL NERVE (WRIST DROP, loss of finger extension, sensory loss in 1st dorsal web space). Accompanied by Profunda Brachii Artery. 3. Supracondylar Fracture: ANTERIOR INTEROSSEOUS NERVE (AIN) / MEDIAN NERVE (inability to make 'OK' sign). 4. Medial Epicondyle Fracture: ULNAR NERVE (Claw hand of medial 2 digits, Froment's sign positive).",
        "citation": "Gray's Anatomy for Students, 4th Ed, Chapter 7 (Upper Limb), p. 692-706.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Shoulder Joint & Rotator Cuff",
        "stem": (
            "A 46-year-old painter presents with persistent shoulder pain that worsens when lifting his arm overhead. "
            "On examination, active abduction of the right arm produces sharp pain between 60 degrees and 120 degrees of abduction, "
            "whereas abduction below 60 degrees and above 120 degrees is completely painless ('Painful Arc Syndrome'). "
            "Jobe's 'Empty Can' test (resisted abduction in 90 degrees elevation and 30 degrees internal rotation) is strongly positive. "
            "Which tendon of the rotator cuff (SITS muscles) is the most frequently impinged and torn under the coracoacromial arch?"
        ),
        "options": [
            ("Supraspinatus Tendon", True, None),
            ("Infraspinatus Tendon", False, "Infraspinatus mediates lateral rotation of the shoulder."),
            ("Teres Minor Tendon", False, "Teres minor mediates lateral rotation and adduction, innervated by the axillary nerve."),
            ("Subscapularis Tendon", False, "Subscapularis inserts onto the lesser tubercle of the humerus and mediates medial rotation (tested by lift-off test).")
        ],
        "pearl": "Rotator Cuff Muscles (SITS Mnemonic): 1. SUPRASPINATUS: INITIATES the first 0-15 degrees of arm abduction (Axillary nerve takes over from 15-90 degrees, and Serratus anterior/Trapezius abducts >90 degrees). Most commonly injured/torn rotator cuff tendon (passes through narrow subacromial space; Painful Arc 60-120 degrees). Tested by: Jobe's Empty Can Test. 2. Infraspinatus: Lateral rotation. 3. Teres Minor: Lateral rotation. 4. Subscapularis: MEDIAL rotation (only SITS muscle inserting onto Lesser Tubercle; tested by Gerber's Lift-off test).",
        "citation": "B.D. Chaurasia's Human Anatomy, 8th Ed, Vol 1, Chapter 6 (Shoulder Region), p. 88-98.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Cubital Fossa & Forearm Spaces",
        "stem": (
            "During venipuncture of the median cubital vein in the cubital fossa, an inexperienced phlebotomist accidentally pierces too deeply. "
            "Which tough fibrous aponeurotic band lies immediately deep to the median cubital vein, "
            "safeguarding the underlying Brachial Artery and Median Nerve from accidental puncture?"
        ),
        "options": [
            ("Bicipital Aponeurosis (Lacertus Fibrosus)", True, None),
            ("Interosseous membrane of forearm", False, "Interosseous membrane connects the radius and ulna in the deep forearm."),
            ("Pronator teres deep head", False, "Pronator teres forms the medial boundary of the cubital fossa."),
            ("Transverse carpal ligament (Flexor retinaculum)", False, "Flexor retinaculum is located at the wrist, forming the carpal tunnel.")
        ],
        "pearl": "Cubital Fossa Anatomy & Contents: Boundaries: Base: Imaginary line between medial and lateral epicondyles | Lateral: Medial border of Brachioradialis | Medial: Lateral border of Pronator Teres | Roof: Deep fascia reinforced by the BICIPITAL APONEUROSIS (Lacertus Fibrosus) which separates the superficial Median Cubital Vein from the deeper Brachial Artery. Contents from MEDIAL TO LATERAL (MBBS / MBBR Mnemonic): M: Median Nerve | B: Brachial Artery (bifurcates into radial and ulnar) | B: Biceps Brachii Tendon | R: Radial Nerve (deep/superficial branches).",
        "citation": "B.D. Chaurasia's Human Anatomy, 8th Ed, Vol 1, Chapter 8 (Cubital Fossa), p. 118-124.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Femoral Triangle & Canal",
        "stem": (
            "A 65-year-old multiparous female presents with a tender, irreducible, globular swelling in her right groin "
            "located INFERIOR and LATERAL to the pubic tubercle. She exhibits signs of acute small bowel obstruction. "
            "Emergency surgery is scheduled for an incarcerated Femoral Hernia. "
            "What structure forms the sharp, rigid MEDIAL boundary of the Femoral Ring (the site where strangulation occurs) "
            "that may require incising to release the incarcerated bowel loop?"
        ),
        "options": [
            ("Lacunar Ligament (Gimbernat's Ligament)", True, None),
            ("Inguinal Ligament (Poupart's Ligament)", False, "Inguinal ligament forms the ANTERIOR boundary of the femoral ring."),
            ("Femoral Vein", False, "Femoral vein forms the LATERAL boundary of the femoral canal."),
            ("Pectineal Ligament (Cooper's Ligament)", False, "Pectineal ligament covers the pectineal line of the pubic bone forming the POSTERIOR boundary of the femoral ring.")
        ],
        "pearl": "Femoral Ring & Canal Boundaries: Femoral Canal: Medial compartment of the femoral sheath (contains fat and Cloquet's / Rosenmuller's deep inguinal lymph node). Boundaries of Femoral Ring: Anterior: Inguinal Ligament (Poupart) | Posterior: Pectineal Ligament (Cooper) & Pectineus muscle | Lateral: Femoral Vein | Medial: LACUNAR LIGAMENT (Gimbernat). Hernia Neck: Below and lateral to pubic tubercle (Direct/indirect inguinal hernia is ABOVE and medial to pubic tubercle!). High risk of strangulation (due to sharp lacunar ligament edge). WARNING: In 20-30%, an ABERRANT OBTURATOR ARTERY (Crown of Death / Corona Mortis) arches across the lacunar ligament; incising it causes fatal hemorrhage!",
        "citation": "B.D. Chaurasia's Human Anatomy, 8th Ed, Vol 2 (Lower Limb), Chapter 3 (Femoral Region), p. 44-54.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Knee Joint & Cruciate Ligaments",
        "stem": (
            "A professional soccer player twists his right knee while planting his foot and decelerating rapidly during a match. "
            "He hears an audible 'pop' inside the knee and experiences acute swelling within 2 hours (hemarthrosis). "
            "On physical examination with the knee flexed at 30 degrees, the tibia can be pulled anteriorly relative to the femur "
            "with a soft, mushy endpoint ('Lachman Test strongly POSITIVE'). "
            "Which intra-articular ligament is ruptured, and what is its femoral attachment?"
        ),
        "options": [
            ("Anterior Cruciate Ligament (ACL); attached to the posteromedial aspect of the Lateral Femoral Condyle (LAMP mnemonic)", True, None),
            ("Posterior Cruciate Ligament (PCL); attached to the lateral femoral condyle", False, "PCL attaches to the anterolateral aspect of the Medial Femoral Condyle (LAMP: Lateral condyle = Anterior cruciate; Medial condyle = Posterior cruciate)."),
            ("Medial Collateral Ligament (MCL); attached to the adductor tubercle", False, "MCL is an extracapsular ligament tested by valgus stress at 30 degrees flexion."),
            ("Lateral Collateral Ligament (LCL); attached to the fibular head", False, "LCL is an extracapsular cord-like ligament tested by varus stress.")
        ],
        "pearl": "Cruciate Ligaments Attachments & Testing: LAMP Mnemonic for Femoral Attachments: L: Lateral condyle = A: Anterior cruciate ligament (ACL) | M: Medial condyle = P: Posterior cruciate ligament (PCL). (Specifically: ACL attaches to medial surface of Lateral condyle; PCL attaches to lateral surface of Medial condyle). Most sensitive clinical test for ACL tear: LACHMAN TEST at 30° flexion (superior to Anterior Drawer Test). Unhappy Triad of O'Donoghue: ACL + Medial Meniscus + Medial Collateral Ligament (MCL).",
        "citation": "Gray's Anatomy for Students, 4th Ed, Chapter 6 (Lower Limb), p. 574-588.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Coronary Circulation & Heart Anatomy",
        "stem": (
            "In 85% to 90% of the human population, the coronary circulation is classified as 'Right Dominant'. "
            "What exact anatomical criterion defines Right Coronary Dominance versus Left Coronary Dominance?"
        ),
        "options": [
            ("The origin of the Posterior Interventricular Artery (Posterior Descending Artery / PDA) from the Right Coronary Artery (RCA)", True, None),
            ("The origin of the Sinoatrial (SA) Nodal Artery from the RCA", False, "SA nodal artery arises from RCA in ~60% and LCx in ~40%, but this does NOT define coronary dominance."),
            ("The presence of a larger diameter in the RCA than the LCA", False, "Vessel caliber does not define dominance."),
            ("The supply of the anterior two-thirds of the interventricular septum by the RCA", False, "The anterior 2/3 of the septum is ALWAYS supplied by the LAD (from the LCA), regardless of dominance!")
        ],
        "pearl": "Coronary Dominance Definition: Defined SOLELY by which coronary artery gives off the POSTERIOR DESCENDING ARTERY (PDA / Posterior Interventricular Artery) that runs in the posterior interventricular sulcus: 1. Right Dominant (85-90%): PDA arises from the Right Coronary Artery (RCA). 2. Left Dominant (8-10%): PDA arises from the Left Circumflex Artery (LCx). 3. Co-dominant (2-5%): PDA supplied by both RCA and LCx. Crucial Fact: The AV node artery arises from the dominant artery at the crux of the heart (hence inferior MI from RCA occlusion often causes AV block).",
        "citation": "B.D. Chaurasia's Human Anatomy, 8th Ed, Vol 1 (Thorax), Chapter 18 (Heart), p. 272-284.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Cranial Nerves & Cavernous Sinus",
        "stem": (
            "A 42-year-old female presents with severe facial pain, periorbital edema, proptosis, and chemosis following "
            "a squeezed furuncle (boil) in the 'danger area of the face' (upper lip and nasolabial fold). "
            "She develops complete ophthalmoplegia with ptosis and a dilated pupil in the right eye. "
            "Cavernous Sinus Thrombosis is diagnosed. Which neurovascular structure passes directly THROUGH THE CENTER / INTERIOR "
            "of the cavernous sinus (surrounded by venous blood), and is therefore the EARLIEST nerve affected?"
        ),
        "options": [
            ("Abducens Nerve (Cranial Nerve VI) accompanied by the Internal Carotid Artery", True, None),
            ("Oculomotor Nerve (Cranial Nerve III)", False, "CN III lies in the LATERAL WALL of the cavernous sinus."),
            ("Trochlear Nerve (Cranial Nerve IV)", False, "CN IV lies in the LATERAL WALL of the cavernous sinus."),
            ("Ophthalmic division of Trigeminal Nerve (CN V1)", False, "CN V1 and V2 lie in the LATERAL WALL of the cavernous sinus.")
        ],
        "pearl": "Cavernous Sinus Anatomy: Structures passing THROUGH the lumen (Center): 1. INTERNAL CAROTID ARTERY (with sympathetic carotid plexus) | 2. ABDUCENS NERVE (CN VI) - lies inferolateral to ICA; EARLIEST NERVE INVOLVED in thrombosis or aneurysm (lateral rectus palsy / inability to abduct eye). Structures in the LATERAL WALL (Top to bottom: 'OTOM'): 1. O: Oculomotor Nerve (CN III) | 2. T: Trochlear Nerve (CN IV) | 3. O: Ophthalmic division of Trigeminal (CN V1) | 4. M: Maxillary division of Trigeminal (CN V2). (Note: Mandibular division CN V3 DOES NOT pass through the cavernous sinus!). Danger area of face drains to cavernous sinus via facial vein -> superior ophthalmic vein (valveless!).",
        "citation": "B.D. Chaurasia's Human Anatomy, 8th Ed, Vol 3 (Head & Neck), Chapter 10 (Cranial Cavity), p. 148-158.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Circle of Willis & Stroke Syndromes",
        "stem": (
            "A 62-year-old male presents with sudden-onset vertigo, intractable vomiting, hoarseness of voice, difficulty swallowing (dysphagia), "
            "and ataxia with falling to the right side. Neurological examination reveals: right-sided Horner syndrome (ptosis, miosis, enophthalmos), "
            "loss of pain and temperature sensation on the RIGHT side of the face (ipsilateral trigeminal spinal nucleus), "
            "and loss of pain and temperature sensation on the LEFT side of the body and extremities (contralateral spinothalamic tract). "
            "Occlusion of which arterial branch supplying the lateral medulla produces this Wallenberg Lateral Medullary Syndrome?"
        ),
        "options": [
            ("Posterior Inferior Cerebellar Artery (PICA, branch of Vertebral Artery)", True, None),
            ("Anterior Inferior Cerebellar Artery (AICA)", False, "AICA occlusion causes Lateral Pontine Syndrome with ipsilateral facial nerve (CN VII) palsy and deafness/tinnitus (labyrinthine artery)."),
            ("Superior Cerebellar Artery (SCA)", False, "SCA occlusion causes severe ipsilateral cerebellar ataxia without medullary lower cranial nerve involvement."),
            ("Anterior Spinal Artery (ASA)", False, "ASA occlusion causes Medial Medullary Syndrome (Dejerine syndrome: hypoglossal tongue deviation to side of lesion + contralateral hemiparesis).")
        ],
        "pearl": "Brainstem Stroke Syndromes: 1. Wallenberg's Lateral Medullary Syndrome: Caused by PICA or Vertebral Artery occlusion. Nucleus Ambiguus (CN IX, X) -> Dysphagia, hoarseness, absent gag reflex; Vestibular nuclei -> Vertigo, nystagmus; Spinal trigeminal tract -> IPSILATERAL facial pain/temp loss; Spinothalamic tract -> CONTRALATERAL body pain/temp loss (CROSS SENSORY LOSS!); Sympathetic tract -> Ipsilateral Horner syndrome; Inferior cerebellar peduncle -> Ipsilateral ataxia. 2. Medial Medullary Syndrome: Anterior Spinal Artery (ASA) -> CN XII paralysis (tongue deviates to side of lesion) + contralateral hemiparesis.",
        "citation": "Gray's Anatomy for Students, 4th Ed, Chapter 8 (Neuroanatomy), p. 890-904.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Larynx & Pharynx Anatomy",
        "stem": (
            "During thyroidectomy for a multinodular goiter, complete bilateral accidental transection of the Recurrent Laryngeal Nerves occurs. "
            "Which intrinsic muscle of the larynx is the SOLE ABDUCTOR of the vocal cords ('safety muscle of the larynx') "
            "whose bilateral denervation results in catastrophic adduction of the cords and immediate fatal upper airway asphyxiation?"
        ),
        "options": [
            ("Posterior Cricoarytenoid Muscle", True, None),
            ("Lateral Cricoarytenoid Muscle", False, "Lateral cricoarytenoid is a vocal cord ADDUCTOR."),
            ("Cricothyroid Muscle", False, "Cricothyroid is the TENSOR of the vocal cords, uniquely innervated by the External Branch of the Superior Laryngeal Nerve."),
            ("Thyroarytenoid (Vocalis) Muscle", False, "Thyroarytenoid relaxes the vocal cords.")
        ],
        "pearl": "Laryngeal Muscles Actions & Innervations: 1. SOLE ABDUCTOR (Opens vocal cords / 'SAFETY MUSCLE OF LARYNX'): POSTERIOR CRICOARYTENOID (Mnemonic: PCA = Pulls Cords Apart). Bilateral paralysis -> cords fall to midline -> acute asphyxia requiring emergency tracheostomy! 2. ADDUCTORS (Close cords): Lateral cricoarytenoid & Transverse arytenoid. 3. TENSOR (High pitch): CRICOTHYROID (innervated by EXTERNAL LARYNGEAL NERVE). 4. RELAXERS: Thyroarytenoid (Vocalis). INNERVATION RULE: All intrinsic muscles of larynx are innervated by the RECURRENT LARYNGEAL NERVE, EXCEPT the Cricothyroid (External branch of Superior Laryngeal Nerve!).",
        "citation": "B.D. Chaurasia's Human Anatomy, 8th Ed, Vol 3 (Head & Neck), Chapter 19 (Larynx), p. 288-298.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Pharyngeal Arches & Clefts",
        "stem": (
            "During human embryogenesis, the branchial (pharyngeal) apparatus develops into definitive head and neck structures. "
            "From which specific Pharyngeal Pouch endoderm do the Inferior Parathyroid Glands and the Thymus originate?"
        ),
        "options": [
            ("Third Pharyngeal Pouch (3rd Pouch)", True, None),
            ("Fourth Pharyngeal Pouch (4th Pouch)", False, "4th pouch gives rise to the Superior Parathyroid glands and Ultimobranchial body (C-cells of thyroid)."),
            ("Second Pharyngeal Pouch (2nd Pouch)", False, "2nd pouch gives rise to the Palatine Tonsil lining and supratonsillar fossa."),
            ("First Pharyngeal Pouch (1st Pouch)", False, "1st pouch gives rise to the Eustachian (Auditory) Tube, Middle Ear Cavity, and inner surface of tympanic membrane.")
        ],
        "pearl": "Pharyngeal Pouches Fate (Crucial Inversion Rule): 1st Pouch: Middle ear cavity, Eustachian tube, Mastoid antrum. 2nd Pouch: Palatine Tonsillar fossa. 3RD POUCH: INFERIOR PARATHYROIDS (dorsal wing) + THYMUS (ventral wing) (Mnemonic: 3 = Thymus). 4TH POUCH: SUPERIOR PARATHYROIDS (dorsal wing) + Ultimobranchial body (calcitonin C-cells). INVERSION REASON: 3rd pouch structures migrate further inferiorly down into the neck and anterior mediastinum, pulling the 3rd pouch parathyroid below the 4th pouch parathyroid! (Defective in DiGeorge Syndrome 22q11 -> absent thymus and parathyroids).",
        "citation": "Langman's Medical Embryology, 14th Ed, Chapter 17 (Head and Neck), p. 282-294.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Pharyngeal Arches & Clefts",
        "stem": (
            "A male infant presents with Treacher Collins syndrome (Mandibulofacial Dysostosis). "
            "Embryologically, this condition results from defective migration of neural crest cells into which pharyngeal arch, "
            "responsible for development of the Mandible, Maxilla, Zygomatic bone, Malleus, Incus, and Muscles of Mastication?"
        ),
        "options": [
            ("First Pharyngeal Arch (Mandibular Arch, Meckel's cartilage)", True, None),
            ("Second Pharyngeal Arch (Hyoid Arch, Reichert's cartilage)", False, "2nd arch forms the Stapes, Styloid process, Lesser horn of hyoid, and Muscles of Facial Expression (CN VII)."),
            ("Third Pharyngeal Arch", False, "3rd arch forms the Greater horn of hyoid and Stylopharyngeus muscle (CN IX)."),
            ("Fourth and Sixth Pharyngeal Arches", False, "4th and 6th arches form Laryngeal cartilages and pharyngeal/laryngeal muscles (CN X).")
        ],
        "pearl": "Pharyngeal Arches Derivatives: 1st Arch (Mandibular - CN V3): Meckel's cartilage -> Malleus, Incus, Sphenomandibular ligament, Mandible, Maxilla, Zygoma. Muscles: Mastication (Temporalis, Masseter, Pterygoids), Mylohyoid, Anterior belly of digastric, Tensor veli palatini, Tensor tympani. 2nd Arch (Hyoid - CN VII): Reichert's cartilage -> Stapes, Styloid process, Stylohyoid ligament, Lesser cornu of hyoid. Muscles: Facial expression, Stapedius, Stylohyoid, Posterior belly of digastric. 3rd Arch (CN IX): Greater cornu of hyoid, Stylopharyngeus. 4th Arch (CN X - Superior laryngeal): Cricothyroid, Pharyngeal constrictors. 6th Arch (CN X - Recurrent laryngeal): Intrinsic laryngeal muscles.",
        "citation": "Langman's Medical Embryology, 14th Ed, Chapter 17, p. 270-282.",
        "difficulty": "moderate"
    }
]
