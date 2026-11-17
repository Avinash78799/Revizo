"""
Authentic High-Yield NEET-PG Clinical Questions for Otorhinolaryngology (ENT)
References: Dhingra's Diseases of Ear, Nose and Throat & Head and Neck Surgery (8th Ed)
"""

ENT_QUESTIONS = [
    {
        "concept_name": "Core Principles: Chronic Suppurative Otitis Media (CSOM) Variants",
        "stem": (
            "A 26-year-old male presents with foul-smelling, scanty, purulent discharge from his left ear for 8 months. "
            "Otoscopic examination reveals a retraction pocket in the pars flaccida (attic) of the tympanic membrane containing white, flaky keratin debris "
            "and an erosion of the outer attic wall (scutum). Tuning fork tests demonstrate conductive hearing loss in the affected ear. "
            "Pure-tone audiogram confirms a 35 dB conductive hearing loss. High-resolution CT (HRCT) of the temporal bone demonstrates bone erosion of the scutum "
            "and ossicular chain. What is the pathological nature of this condition and the definitive treatment of choice?"
        ),
        "options": [
            ("Tubotympanic (Safe / Benign) CSOM; Topical ciprofloxacin ear drops and observation", False, "Tubotympanic CSOM features a CENTRAL perforation in the pars tensa with profuse, non-foul-smelling mucoid discharge and no bone erosion."),
            ("Atticoantral (Unsafe / Squamous) CSOM with Cholesteatoma; Canal Wall Down (or Up) Mastoidectomy with Tympanoplasty", True, None),
            ("Otomycosis; Topical Clotrimazole ear drops and suction clearance", False, "Otomycosis is a fungal ear canal infection (Aspergillus/Candida) showing wet blotting paper or black fungal heads."),
            ("Acute mastoiditis; Intravenous ampicillin without surgery", False, "Acute mastoiditis is an acute complication presenting with retroauricular swelling and sagging of the posterior canal wall.")
        ],
        "pearl": "CSOM Types Compared: Tubotympanic (Safe/Mucosal): Central perforation in pars tensa, profuse mucoid non-foul discharge, no cholesteatoma, bone erosion rare, treated by Tympanoplasty. Atticoantral (Unsafe/Squamous): Attic or marginal posterosuperior perforation, scanty foul-smelling dirty discharge, CHOLESTEATOMA present, high risk of intracranial complications (meningitis, brain abscess), treated by Modified Radical Mastoidectomy.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 10 (CSOM), p. 74-84.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Chronic Suppurative Otitis Media (CSOM) Variants",
        "stem": (
            "Cholesteatoma is histologically characterized as a three-dimensional epidermoid collection of keratinizing squamous epithelium "
            "within the middle ear cleft. Which destructive proteolytic enzyme produced by the perimatrix (subepithelial connective tissue) of cholesteatoma "
            "is primarily responsible for osteoclastic bone resorption of the ossicles and otic capsule?"
        ),
        "options": [
            ("Collagenase (Matrix Metalloproteinase / MMPs) and Acid Phosphatase", True, None),
            ("Lysozyme", False, "Lysozyme is an antibacterial enzyme in secretions, not responsible for bone destruction."),
            ("Myeloperoxidase", False, "Myeloperoxidase is a neutrophil enzyme producing hypochlorous acid."),
            ("Alkaline phosphatase", False, "Alkaline phosphatase is an osteoblastic bone-forming marker, not a bone-resorptive osteoclast enzyme.")
        ],
        "pearl": "Cholesteatoma Pathology: Consists of: 1. Matrix (keratinizing stratified squamous epithelium) | 2. Central Keratin debris | 3. Perimatrix (granulation tissue producing Collagenase / MMP-2 / MMP-9, IL-1, TNF-alpha) causing osteoclast activation and severe bony erosion of the tegmen tympani, lateral semicircular canal, and facial canal.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 11 (Cholesteatoma), p. 85-92.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Otosclerosis & Carhart's Notch",
        "stem": (
            "A 32-year-old female presents with progressive, bilateral hearing loss that worsened noticeably during her recent pregnancy. "
            "She notes that she hears better in noisy environments such as crowded train stations (Paracusis Willisii). "
            "Otoscopic examination reveals normal, intact, pearly-white tympanic membranes bilaterally, though a faint reddish hue is visualized "
            "through the posteroinferior quadrant of the promontory (Schwartze's sign / flamingo pink sign). "
            "On pure-tone audiometry, bone conduction shows a characteristic dip at 2000 Hz. What is the name of this audiometric finding and the surgical procedure of choice?"
        ),
        "options": [
            ("Carhart's notch; Stapedotomy with Teflon piston insertion", True, None),
            ("Acoustic notch (4000 Hz dip); Myringoplasty", False, "4000 Hz dip in air and bone conduction is the acoustic notch characteristic of Noise-Induced Hearing Loss (NIHL)."),
            ("Tullio phenomenon; Radical mastoidectomy", False, "Tullio phenomenon is sound-induced vertigo seen in superior semicircular canal dehiscence or perilymph fistula."),
            ("Gelle's test notch; Cochlear implantation", False, "Gelle's test is a pneumatic tuning fork test, not an audiometric dip at 2000 Hz.")
        ],
        "pearl": "Otosclerosis (Otospongiosis): Autosomal dominant with variable penetrance. Spongy vascular bone replaces normal enchondral bone at the fissula ante fenestram -> stapes footplate ankylosis. Features: 1. Female > Male, worsens in pregnancy | 2. Paracusis Willisii | 3. Schwartze sign (promontory vascularity) | 4. Carhart's Notch (dip in bone conduction at 2000 Hz due to mechanical disruption of ossicular resonance, disappears after stapedotomy!). SURGICAL DOC: Small fenestra Stapedotomy.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 15 (Otosclerosis), p. 110-118.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Otosclerosis & Carhart's Notch",
        "stem": (
            "In patients with active, highly vascular otospongiosis (stapedial otosclerosis), medical therapy is sometimes prescribed to promote "
            "calcification and stabilization of the active osteoid foci before surgical intervention. Which pharmacological agent is used for this purpose?"
        ),
        "options": [
            ("Sodium Fluoride (with Calcium and Vitamin D)", True, None),
            ("Methotrexate", False, "Methotrexate is an antimetabolite used for rheumatoid arthritis and autoimmune inner ear disease."),
            ("Oral Prednisolone", False, "Steroids do not promote sclerosis of active otospongiotic foci."),
            ("Intratympanic Gentamicin", False, "Intratympanic gentamicin is a chemical labyrinthectomy agent used for refractory Meniere's disease.")
        ],
        "pearl": "Medical Management of Otosclerosis: Sodium Fluoride (20-50 mg/day) promotes maturation and sclerosis of active, highly vascular spongy bone by converting hydroxyapatite into fluoroapatite crystals (which are resistant to osteoclastic resorption). Indicated in: Active Schwartze sign, pure sensorineural cochlear otosclerosis, or stapedotomy refusals.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 15, p. 116-118.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Meniere's Disease Diagnostic Triad",
        "stem": (
            "A 45-year-old male presents with recurrent, episodic attacks of severe rotational vertigo lasting 3 to 4 hours, accompanied by nausea and vomiting. "
            "During the attacks, he experiences a sensation of fullness and roaring, low-frequency tinnitus in his left ear. "
            "Pure-tone audiometry demonstrates a low-frequency sensorineural hearing loss in the left ear that fluctuates between attacks. "
            "Glycerol dehydration test produces transient improvement in pure-tone thresholds. What is the fundamental underlying histopathology?"
        ),
        "options": [
            ("Endolymphatic hydrops (distension of the endolymphatic system with rupture of Reissner's membrane)", True, None),
            ("Perilymphatic fistula at the round window membrane", False, "Perilymph fistula occurs after barotrauma or head injury and features Hennebert's sign (vertigo induced by pneumatic otoscopy)."),
            ("Benign Paroxysmal Positional Vertigo (BPPV) canalithiasis of the posterior semicircular canal", False, "BPPV causes brief vertigo lasting <1 minute triggered strictly by head position changes (Dix-Hallpike positive)."),
            ("Vestibular Schwannoma of the inferior vestibular nerve", False, "Vestibular schwannoma causes insidious, progressive high-frequency sensorineural hearing loss with poor speech discrimination.")
        ],
        "pearl": "Meniere's Disease (Endolymphatic Hydrops): Classic Tetrad: 1. Episodic rotational vertigo (20 mins to several hours) | 2. Fluctuating low-frequency SNHL | 3. Roaring tinnitus | 4. Aural fullness. Pathology: Malabsorption in endolymphatic sac -> dilatation of scala media (Reissner's membrane bulge). Diagnostic test: Glycerol dehydration test (positive if PTA improves by ≥10 dB across 3 frequencies). Acute attack DOC: Vestibular sedatives (Dimenhydrinate/Diazepam); Prophylaxis: Low-salt diet (<2g/day) + Betahistine + Thiazide diuretic.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 17 (Meniere's Disease), p. 128-136.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Meniere's Disease Diagnostic Triad",
        "stem": (
            "In the differential diagnosis of peripheral vertigo, an 8-year-old boy presents with profound congenital bilateral sensorineural hearing loss "
            "and severe goiter due to an inborn error in iodine organification. Genetic testing confirms a mutation in the SLC26A4 gene on chromosome 7q. "
            "Temporal bone CT reveals bilateral enlargement of the vestibular aqueduct. What is this syndrome?"
        ),
        "options": [
            ("Pendred Syndrome", True, None),
            ("Usher Syndrome", False, "Usher syndrome is congenital SNHL accompanied by Retinitis Pigmentosa (tunnel vision and night blindness)."),
            ("Waardenburg Syndrome", False, "Waardenburg syndrome features SNHL with heterochromia iridis, white forelock, and dystopia canthorum (PAX3 gene)."),
            ("Alport Syndrome", False, "Alport syndrome is X-linked Type IV collagen defect presenting with SNHL + Glomerulonephritis (hematuria) + Anterior lenticonus.")
        ],
        "pearl": "Genetic Syndromes with SNHL: Pendred Syndrome: SNHL + Thyroid Goiter (impaired perchlorate discharge) + Enlarged Vestibular Aqueduct (SLC26A4 pendrin gene). Usher Syndrome: SNHL + Retinitis Pigmentosa. Waardenburg Syndrome: SNHL + White forelock + Heterochromia iridis. Alport Syndrome: SNHL + Nephritis + Anterior lenticonus.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 4 (Deafness in Children), p. 32-38.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Epistaxis: Little's Area & Management",
        "stem": (
            "A 19-year-old male presents to the emergency room with profuse bright red bleeding from his left nostril following digital trauma (nose-picking). "
            "On anterior rhinoscopy, bleeding is localized to an arterial plexus located on the anteroinferior portion of the cartilaginous nasal septum (Little's area). "
            "Which of the following arteries does NOT contribute to Kiesselbach's plexus in Little's area?"
        ),
        "options": [
            ("Posterior Ethmoidal Artery", True, None),
            ("Anterior Ethmoidal Artery", False, "Anterior ethmoidal artery (from ophthalmic / internal carotid) contributes to Kiesselbach's plexus."),
            ("Sphenopalatine Artery (nasopalatine branch)", False, "Sphenopalatine artery (artery of epistaxis, from maxillary / external carotid) is the main contributor."),
            ("Superior Labial Artery (septal branch) and Greater Palatine Artery", False, "Both superior labial and greater palatine arteries contribute to Kiesselbach's plexus.")
        ],
        "pearl": "Kiesselbach's Plexus / Little's Area: Anteroinferior part of the nasal septum; most common site (90%) of epistaxis in children and young adults. Formed by anastomosis of 4 arteries: 1. Anterior Ethmoidal (from Internal Carotid via Ophthalmic) | 2. Sphenopalatine | 3. Greater Palatine | 4. Superior Labial (septal branch) (all 3 from External Carotid). THE POSTERIOR ETHMOIDAL ARTERY DOES NOT CONTRIBUTE!",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 24 (Epistaxis), p. 178-185.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Epistaxis: Little's Area & Management",
        "stem": (
            "A 68-year-old hypertensive male presents with intractable, severe epistaxis from the posterior aspect of his right nasal cavity that fails to resolve "
            "with anterior nasal packing. Inspection reveals dark red blood pouring down the posterior pharyngeal wall. "
            "Which venous plexus located on the lateral nasal wall inferior to the posterior end of the inferior turbinate is a major source of posterior epistaxis in elderly hypertensives?"
        ),
        "options": [
            ("Woodruff's Naso-nasopharyngeal Plexus", True, None),
            ("Pterygoid venous plexus", False, "Pterygoid venous plexus lies in the infratemporal fossa."),
            ("Batson's vertebral venous plexus", False, "Batson's plexus surrounds the vertebral column."),
            ("Kiesselbach's arterial plexus", False, "Kiesselbach's plexus is situated anteriorly on the septum, not posteriorly on the lateral wall.")
        ],
        "pearl": "Posterior Epistaxis & Woodruff's Plexus: Woodruff's plexus is located on the lateral wall of the nasal cavity just inferior to the posterior end of the inferior turbinate. Common site of severe posterior epistaxis in elderly hypertensives. Requires Posterior Nasal Packing (Foley catheter or Bellocq pack) or endoscopic sphenopalatine artery ligation (ESPAL).",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 24, p. 182-184.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Juvenile Nasopharyngeal Angiofibroma (JNA)",
        "stem": (
            "A 15-year-old adolescent male presents with a history of recurrent, spontaneous, painless, profuse unilateral epistaxis and progressive left-sided nasal obstruction "
            "over the past 6 months. Physical examination reveals a smooth, lobulated, reddish-purple mass in the posterior nasal cavity. "
            "Contrast-enhanced CT shows expansion of the sphenopalatine foramen with anterior bowing of the posterior wall of the maxillary antrum (Holman-Miller sign / antral sign). "
            "Why is pre-operative incisional or transnasal biopsy STRICTLY CONTRAINDICATED in this patient?"
        ),
        "options": [
            ("Because biopsy provokes catastrophic, life-threatening torrential hemorrhage due to lack of a muscular contractile coat in the tumor vessels", True, None),
            ("Because biopsy induces rapid malignant sarcomatous transformation", False, "JNA is a benign vascular tumor and does not undergo malignant degeneration."),
            ("Because it causes instantaneous seeding into the cavernous sinus", False, "JNA does not spread by epithelial seeding; it spreads by direct bony erosion along fissures."),
            ("Because it triggers acute anaphylactic shock", False, "Anaphylaxis is not associated with angiofibroma tissue sampling.")
        ],
        "pearl": "Juvenile Nasopharyngeal Angiofibroma (JNA): Benign, highly vascular, locally aggressive tumor exclusively seen in ADOLESCENT MALES (testosterone/androgen dependent). Origin: Superior margin of sphenopalatine foramen. Classic CT sign: Holman-Miller Sign (anterior bowing of posterior maxillary sinus wall). BIOPSY IS STRICTLY CONTRAINDICATED due to fatal hemorrhage (vessels lack tunica media / smooth muscle elastic lamina!). Treatment: Pre-operative embolization of maxillary artery branches followed by endoscopic or transpalatal surgical excision.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 34 (Nasopharyngeal Tumours), p. 248-254.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Juvenile Nasopharyngeal Angiofibroma (JNA)",
        "stem": (
            "During preoperative preparation of a biopsy-proven juvenile nasopharyngeal angiofibroma in a 16-year-old boy, diagnostic digital subtraction angiography (DSA) "
            "is performed. Which major artery is the primary arterial feeder supplying the tumor and is targeted for selective therapeutic embolization 24-48 hours prior to surgery?"
        ),
        "options": [
            ("Internal Maxillary Artery (branch of External Carotid Artery)", True, None),
            ("Ophthalmic Artery", False, "Ophthalmic artery (from internal carotid) can supply superior intracranial extensions, but internal maxillary is the primary feeder."),
            ("Vertebral Artery", False, "Vertebral artery supplies the posterior fossa."),
            ("Facial Artery", False, "Facial artery supplies the external nose and face, not the primary deep nasopharyngeal mass.")
        ],
        "pearl": "JNA Blood Supply: Primary feeder: Internal Maxillary Artery (specifically sphenopalatine, descending palatine, and middle meningeal branches). Pre-operative superselective transcatheter embolization using Polyvinyl alcohol (PVA) particles performed 24-48 hours before surgery reduces intraoperative blood loss by >70%.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 34, p. 250-252.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Laryngeal Carcinoma & Vocal Cord Nodules",
        "stem": (
            "A 32-year-old female schoolteacher presents with persistent hoarseness of voice for 4 months. She notes that her voice is clear in the morning "
            "after a night of rest but deteriorates progressively through the day after teaching classes. "
            "Video laryngostroboscopy demonstrates small, bilateral, symmetrical, pale, whitish nodules located at the junction of the anterior one-third "
            "and posterior two-thirds of the true vocal cords. What is the diagnosis and the primary initial treatment of choice?"
        ),
        "options": [
            ("Vocal Cord Nodules (Singer's / Teacher's Nodules); Voice therapy (speech therapy) and vocal hygiene", True, None),
            ("Vocal Cord Polyp; Urgent external total laryngectomy", False, "Vocal cord polyps are unilateral, pedunculated or sessile, and managed by micro-laryngeal surgery, not total laryngectomy!"),
            ("Laryngeal Papillomatosis; Intravenous Cidofovir alone", False, "Papillomatosis presents with multiple grape-like clusters caused by HPV 6/11."),
            ("Squamous Cell Carcinoma of glottis; Radical neck dissection", False, "Symmetrical bilateral nodules at the junction of anterior 1/3 and posterior 2/3 in a teacher are classic benign vocal nodules, not malignancy.")
        ],
        "pearl": "Vocal Cord Nodules (Singer's / Screamer's / Teacher's Nodules): Cause: Vocal abuse / hyperfunction. Location: Symmetrical, BILATERAL, at the junction of the ANTERIOR 1/3 and POSTERIOR 2/3 of true vocal cords (maximum amplitude of vibration). Initial Treatment: Conservative: Speech therapy + Vocal hygiene. Microlaryngeal phonomicrosurgical excision is reserved only for hard, fibrotic nodules failing conservative therapy.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 41 (Benign Lesions of Larynx), p. 296-302.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Laryngeal Carcinoma & Vocal Cord Nodules",
        "stem": (
            "A 64-year-old chronic bidi smoker presents with progressive hoarseness of voice for 6 months, recently accompanied by mild inspiratory stridor. "
            "Indirect laryngoscopy reveals an exophytic, ulcerated lesion limited to the anterior two-thirds of the right true vocal cord with normal vocal cord mobility. "
            "There are no palpable cervical lymph nodes (T1aN0M0 Squamous Cell Carcinoma of the Glottis). "
            "Which of the following modalities offers the best combination of oncological cure and excellent voice preservation in early Glottic Carcinoma?"
        ),
        "options": [
            ("External Beam Radiotherapy (EBRT) or Transoral CO2 Laser Microsurgery", True, None),
            ("Total Laryngectomy with bilateral comprehensive neck dissection", False, "Total laryngectomy is a mutilating procedure reserved for advanced T3/T4 tumors, not early T1a glottic cancer!"),
            ("Systemic Cisplatin and Fluorouracil chemotherapy alone without radiation", False, "Chemotherapy alone is not a curative modality for localized T1 glottic cancer."),
            ("Palliative tracheostomy and hospice referral", False, "T1 glottic carcinoma has a >90-95% 5-year cure rate with curative radiotherapy or laser cordectomy.")
        ],
        "pearl": "Laryngeal Carcinoma Pearls: Glottic Carcinoma (most common): Early presentation (hoarseness), slowest metastasis (vocal cords lack lymphatic drainage!). T1a (limited to one vocal cord with normal mobility): Curative with Transoral CO2 Laser Cordectomy OR Radiotherapy (both offer >90% cure with voice preservation). Supraglottic Carcinoma: Rich lymphatics -> early cervical nodal metastasis.",
        "citation": "Dhingra's Diseases of Ear, Nose and Throat, 8th Ed, Chapter 43 (Cancer of Larynx), p. 308-318.",
        "difficulty": "moderate"
    }
]
