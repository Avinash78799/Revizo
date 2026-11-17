"""
Authentic High-Yield NEET-PG Clinical Questions for Ophthalmology
References: Khurana's Comprehensive Ophthalmology (7th Ed), Kanski's Clinical Ophthalmology (9th Ed)
"""

OPHTHALMOLOGY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Primary Open-Angle vs Angle-Closure Glaucoma",
        "stem": (
            "A 56-year-old female presents to the eye emergency department in the evening with sudden, excruciating pain in her right eye, "
            "severe hemicranial headache, nausea, and vomiting. She reports seeing colored halos around light bulbs. "
            "On slit-lamp examination, the right eye exhibits marked ciliary injection, a steamy 'ground-glass' corneal edema, "
            "a shallow anterior chamber, and a vertically oval, mid-dilated, unreactive pupil. "
            "Intraocular pressure (IOP) measured by Goldmann applanation tonometry is 58 mmHg in the right eye (normal: 10-21 mmHg). "
            "What is the single most definitive long-term surgical/laser intervention to prevent recurrence in this eye and prophylactically in the contralateral fellow eye?"
        ),
        "options": [
            ("Neodymium:YAG (Nd:YAG) Laser Peripheral Iridotomy", True, None),
            ("Argon laser trabeculoplasty (ALT)", False, "Trabeculoplasty is indicated for open-angle glaucoma, not for acute pupillary block angle-closure where the trabecular meshwork is blocked by peripheral iris."),
            ("Cyclocryotherapy to the ciliary body", False, "Cyclodestructive procedures are reserved for refractory absolute glaucoma without visual potential."),
            ("Urgent vitrectomy and silicone oil tamponade", False, "Vitrectomy has no role in acute angle-closure glaucoma.")
        ],
        "pearl": "Acute Angle-Closure Glaucoma: Mechanism: Pupillary block in hyperopic eyes with shallow anterior chambers triggered by mydriasis (dark room / anticholinergics). Clinical Triad: Excruciating pain + Colored halos + Steamy cornea with vertically oval mid-dilated pupil. Emergency Medical Management: IV Mannitol 20% (osmotic draw) + Topical Pilocarpine 2% (miotic) + Topical Timolol / Brimonidine + Oral Acetazolamide. DEFINITIVE SURGICAL/LASER TREATMENT: Nd:YAG Laser Peripheral Iridotomy (creates a bypass channel between posterior and anterior chambers; MUST be performed on BOTH the affected and fellow eye!).",
        "citation": "Khurana's Comprehensive Ophthalmology, 7th Ed, Chapter 9 (Glaucoma), p. 228-242.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Primary Open-Angle vs Angle-Closure Glaucoma",
        "stem": (
            "A 62-year-old male undergoes a routine optical examination. Best-corrected visual acuity is 6/6 in both eyes. "
            "However, Goldmann applanation tonometry shows an IOP of 26 mmHg in the right eye and 27 mmHg in the left eye. "
            "Funduscopic examination reveals bilateral optic disc cupping with a cup-to-disc ratio (CDR) of 0.75, thinning of the inferior and superior neuroretinal rims, "
            "and bayoneting of retinal vessels at the cup margin. Automated visual field perimetry (Humphrey) shows an arcuate scotoma (Bjerrum's scotoma). "
            "Gonioscopy confirms an open angle (Shaffer Grade IV in all 4 quadrants). What is the first-line medical drug class of choice for Primary Open-Angle Glaucoma (POAG)?"
        ),
        "options": [
            ("Prostaglandin F2-alpha analogues (e.g., Latanoprost, Bimatoprost, Travoprost)", True, None),
            ("Oral Carbonic Anhydrase Inhibitors (Acetazolamide)", False, "Systemic acetazolamide has significant adverse effects (metabolic acidosis, hypokalemia, renal stones) and is not first-line maintenance for POAG."),
            ("Topical Cholinergic Agonists (Pilocarpine)", False, "Pilocarpine causes miosis, brow ache, and shallowing of the anterior chamber; superseded as first-line by prostaglandins."),
            ("Topical Hyperosmotic agents (Glycerol)", False, "Glycerol is used for acute acute-angle closure emergency reduction of corneal edema, not chronic open-angle therapy.")
        ],
        "pearl": "Primary Open-Angle Glaucoma (POAG): Painless, progressive bilateral condition. High IOP + Optic disc cupping (ISNT rule violation: Inferior > Superior > Nasal > Temporal rim thickness lost) + Visual field loss (Baring of blind spot -> Seidel scotoma -> Bjerrum arcuate scotoma -> Roenne nasal step -> Tunnel vision). FIRST-LINE DRUG: Prostaglandin Analogues (Latanoprost 0.005% once at bedtime). Mechanism: Increases Uveoscleral outflow (30-35% IOP reduction). Side effects: Iris hyperpigmentation, eyelash hypertrichosis.",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 10, p. 340-356.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Cataract Types & Surgical Techniques (Phaco)",
        "stem": (
            "A 68-year-old retired clerk reports gradual, painless, progressive diminution of vision in both eyes over the past 2 years. "
            "Interestingly, he mentions that while his distance vision has worsened, his near vision has improved so much that he can now read the newspaper "
            "without his presbyopic reading glasses ('second sight'). Slit-lamp biomicroscopy reveals yellowish-brown discoloration and increased optical density "
            "in the central core of both crystalline lenses. What type of senile cataract is responsible for this refractive shift?"
        ),
        "options": [
            ("Senile Nuclear Sclerotic Cataract producing index myopia", True, None),
            ("Posterior Subcapsular Cataract producing severe hyperopia", False, "Posterior subcapsular cataract causes prominent disabling daytime glare in young adults and diabetics, not index myopia."),
            ("Cortical Cuneiform Cataract with wedge-shaped spokes", False, "Cortical cataract features radial cuneiform opacities causing monocular diplopia without second sight."),
            ("Anterior Polar Cataract related to persistent pupillary membrane", False, "Anterior polar cataract is a stationary, congenital opacity, not progressive senile cataract.")
        ],
        "pearl": "Senile Cataract Varieties: 1. Nuclear Cataract: Sclerosis of the lens nucleus -> increases refractive index of the lens -> INDEX MYOPIA -> patient can read without reading glasses ('Second Sight'). 2. Cortical Cataract: Hydration of lens cortex -> wedge-shaped cuneiform spokes pointing centrally -> monocular diplopia. 3. Posterior Subcapsular Cataract: Located at nodal point of eye -> early marked vision loss, disabling glare, vision worse in bright light (pupillary constriction).",
        "citation": "Khurana's Comprehensive Ophthalmology, 7th Ed, Chapter 8 (Diseases of Lens), p. 195-208.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Cataract Types & Surgical Techniques (Phaco)",
        "stem": (
            "During routine modern Phacoemulsification cataract surgery, high-frequency ultrasonic energy is utilized to emulsify the hard cataractous lens nucleus. "
            "At what frequency does the piezoelectric phacoemulsification handpiece typically operate to fragment the nucleus?"
        ),
        "options": [
            ("28 kHz to 45 kHz (ultrasonic range)", True, None),
            ("1 MHz to 5 MHz", False, "1-5 MHz is used in diagnostic B-scan ultrasound, not phacoemulsification."),
            ("100 Hz to 500 Hz", False, "100-500 Hz is within the human audible sound range."),
            ("10 GHz to 20 GHz", False, "Gigahertz frequencies are microwave radar frequencies.")
        ],
        "pearl": "Phacoemulsification Physics: Converts electrical energy into mechanical acoustic vibrations via Piezoelectric crystals operating at 28,000 to 45,000 Hz (28-45 kHz). Jackhammer effect (physical impact of needle tip) + Cavitation effect (microscopic vapor bubbles imploding to create shock waves) liquefy the lens nucleus through a 2.2-2.8 mm clear corneal incision.",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 9 (Cataract Surgery), p. 312-322.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Corneal Ulcers: Bacterial vs Fungal vs Viral",
        "stem": (
            "A 42-year-old agricultural laborer is struck in the right eye by a sugarcane leaf while harvesting in a field. "
            "Four days later, he presents with redness, gritty pain, photophobia, and decreased vision. "
            "Slit-lamp examination demonstrates a greyish-white corneal infiltrate with dry, raised, feathery/crenated margins, "
            "surrounded by multiple punctate 'satellite lesions' in the adjacent clear stroma, and a sterile, non-shifting hypopyon in the anterior chamber. "
            "Corneal scrapings stained with Potassium Hydroxide (10% KOH) reveal septate hyphae. What is the definitive first-line topical antimicrobial of choice?"
        ),
        "options": [
            ("Topical Natamycin (5% ophthalmic suspension) every 1-2 hours", True, None),
            ("Topical Ciprofloxacin 0.3% drops every 30 minutes", False, "Ciprofloxacin has zero antifungal efficacy and will allow fungal keratitis to progress to corneal perforation."),
            ("Topical Dexamethasone 0.1% drops 4 times daily", False, "TOPICAL CORTICOSTEROIDS ARE STRICTLY CONTRAINDICATED in fungal and active bacterial corneal ulcers; they accelerate fungal invasion and cause rapid descemetocele/perforation!"),
            ("Topical Acyclovir 3% ointment 5 times daily", False, "Acyclovir is specific for Herpes Simplex keratitis, not filamentous fungi.")
        ],
        "pearl": "Corneal Ulcers Differential: FUNGAL KERATITIS: History of trauma with vegetative matter (sugarcane leaf, tree branch) -> dry, feathery margins + satellite lesions + endothelial plaque + thick, non-shifting hypopyon. KOH wet mount shows hyphae. DRUG OF CHOICE: Natamycin 5% suspension (effective against Fusarium and Aspergillus). CONTRAINDICATION: CORTICOSTEROIDS ARE STRICTLY FORBIDDEN! BACTERIAL KERATITIS: Wet, necrotic ulcer + mobile hypopyon -> Fortified Cefazolin + Tobramycin.",
        "citation": "Khurana's Comprehensive Ophthalmology, 7th Ed, Chapter 6 (Cornea), p. 118-132.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Corneal Ulcers: Bacterial vs Fungal vs Viral",
        "stem": (
            "A 35-year-old male with a history of recurrent cold sores presents with foreign body sensation, mild redness, and photophobia in his left eye. "
            "On examination, visual acuity is 6/9. Fluorescein staining of the cornea under cobalt blue slit-lamp illumination reveals a branching, arborizing ulcer "
            "with characteristic terminal swellings ('terminal bulbs'). Corneal corneal sensation tested with a cotton wisp is markedly reduced in the affected eye. "
            "What is the causative organism and the first-line topical therapeutic agent?"
        ),
        "options": [
            ("Herpes Simplex Virus Type 1 (HSV-1); Topical Ganciclovir 0.15% gel or Acyclovir 3% ophthalmic ointment", True, None),
            ("Acanthamoeba; Topical Polyhexamethylene biguanide (PHMB)", False, "Acanthamoeba causes severe out-of-proportion pain, radial keratoneuritis, and ring infiltrates in contact lens wearers."),
            ("Pseudomonas aeruginosa; Topical fortified Tobramycin", False, "Pseudomonas causes rapid, liquefactive stromal melting with greenish-yellow sloughing, not a dendritic ulcer."),
            ("Adenovirus Type 8; Topical Prednisolone acetate drops", False, "Adenovirus causes epidemic keratoconjunctivitis with subepithelial nummular infiltrates, not a fluorescein-positive dendritic pattern.")
        ],
        "pearl": "Herpes Simplex Keratitis: Pathognomonic lesion: DENDRITIC ULCER (branching linear ulcer with terminal buds that stain brilliantly with Fluorescein; bed stains green, margins stain with Rose Bengal). KEY DIAGNOSTIC SIGN: Marked hypoesthesia / loss of corneal sensation. DOC: Topical Ganciclovir 0.15% gel or Acyclovir 3% ointment. WARNING: Steroids convert a dendritic ulcer into a sprawling 'Amoebic / Geographic' ulcer!",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 7 (Cornea), p. 222-230.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Diabetic Retinopathy Classification (ETDRS)",
        "stem": (
            "A 58-year-old male with poorly controlled Type 2 Diabetes Mellitus (HbA1c 9.6%) for 16 years presents for diabetic eye screening. "
            "Dilated fundus examination reveals multiple retinal microaneurysms, extensive intraretinal flame-shaped and blot hemorrhages in all four quadrants, "
            "prominent venous beading in two quadrants, and definite intraretinal microvascular abnormalities (IRMA) in one quadrant. "
            "There are NO neovascular tufts on the optic disc (NVD) or elsewhere on the retina (NVE). "
            "According to the Early Treatment Diabetic Retinopathy Study (ETDRS) 4-2-1 rule, what is the classification of this patient's diabetic retinopathy?"
        ),
        "options": [
            ("Mild Non-Proliferative Diabetic Retinopathy (NPDR)", False, "Mild NPDR features microaneurysms only."),
            ("Moderate Non-Proliferative Diabetic Retinopathy (NPDR)", False, "Moderate NPDR has more than microaneurysms but does not fulfill the 4-2-1 criteria for severe NPDR."),
            ("Severe Non-Proliferative Diabetic Retinopathy (NPDR)", True, None),
            ("High-Risk Proliferative Diabetic Retinopathy (PDR)", False, "Proliferative diabetic retinopathy requires the presence of active NEOVASCULARIZATION (NVD or NVE), which is absent in this patient.")
        ],
        "pearl": "ETDRS 4-2-1 Rule for Severe NPDR: Requires at least ONE of the following 3 criteria (without neovascularization): 1. Diffuse microaneurysms/hemorrhages in all 4 quadrants | 2. Venous beading in ≥2 quadrants | 3. Prominent IRMA in ≥1 quadrant. High risk of converting to Proliferative Diabetic Retinopathy (50% within 1 year). Proliferative DR is defined by the appearance of Neovascularization (NVD >1/3 disc diameter or NVE with vitreous hemorrhage).",
        "citation": "Khurana's Comprehensive Ophthalmology, 7th Ed, Chapter 12 (Diseases of Retina), p. 272-284.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Diabetic Retinopathy Classification (ETDRS)",
        "stem": (
            "A 52-year-old diabetic female presents with distortion of straight lines (metamorphopsia) and progressive blurring of central vision in both eyes. "
            "Fundus biomicroscopy and Optical Coherence Tomography (OCT) demonstrate retinal thickening and cystic spaces involving the center of the fovea, "
            "with a central subfield thickness of 420 um. Best-corrected visual acuity is 6/18. "
            "What is the first-line pharmacotherapeutic standard of care for Center-Involving Diabetic Macular Edema (CI-DME)?"
        ),
        "options": [
            ("Intravitreal Anti-Vascular Endothelial Growth Factor (Anti-VEGF, e.g., Aflibercept, Ranibizumab)", True, None),
            ("Focal macular argon laser photocoagulation alone", False, "Intravitreal anti-VEGF has replaced focal laser as the primary first-line standard of care for center-involving DME, offering superior visual acuity gains."),
            ("Panretinal photocoagulation (PRP)", False, "PRP is indicated for proliferative diabetic retinopathy and can actually worsen macular edema acutely."),
            ("Oral Metformin dosage escalation", False, "Systemic glycemic control is essential long-term, but acute center-involving DME requires immediate intravitreal anti-VEGF therapy.")
        ],
        "pearl": "Diabetic Macular Edema (DME): Leading cause of visual impairment in diabetic patients. Diagnosed and monitored via Optical Coherence Tomography (OCT). First-line therapy for center-involving DME: Monthly Intravitreal Anti-VEGF injections (Ranibizumab, Aflibercept, Faricimab). Focal/grid laser is reserved for non-center-involving DME.",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 13 (Retinal Vascular Disease), p. 520-534.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Retinal Detachment: Rhegmatogenous vs Exudative",
        "stem": (
            "A 48-year-old highly myopic male (-7.50 D in both eyes) presents with the sudden appearance of multiple dark floating spots ('cobwebs') "
            "and bright flashing lights (photopsia) in his temporal visual field for 2 days, followed by a dark curtain or shadow falling over the superior visual field. "
            "On indirect ophthalmoscopy with scleral indentation, the retina appears corrugated, greyish-white, and undulates with eye movements. "
            "A horseshoe-shaped full-thickness retinal tear is identified in the superotemporal periphery with subretinal fluid accumulation. "
            "What type of retinal detachment is this, and what is the pathophysiology?"
        ),
        "options": [
            ("Rhegmatogenous Retinal Detachment (RRD); full-thickness retinal break allowing liquefied vitreous to enter the subretinal space", True, None),
            ("Tractional Retinal Detachment (TRD); fibrovascular bands contracting and pulling the neurosensory retina without a break", False, "Tractional RD is seen in proliferative diabetic retinopathy where fibrovascular membranes pull the retina, resulting in a concave, immobile detachment without breaks."),
            ("Exudative (Serous) Retinal Detachment; hydrostatic fluid accumulation secondary to choroidal tumor", False, "Exudative RD produces a smooth, ballooning, convex detachment with shifting fluid and no retinal breaks."),
            ("Retinoschisis; splitting of the neurosensory retina without detachment from the RPE", False, "Retinoschisis is an absolute scotoma without tears or vitreous traction.")
        ],
        "pearl": "Retinal Detachment (RD) Types: 1. Rhegmatogenous (RRD - most common): Caused by a retinal break (rhegma = tear/hole, e.g. Horseshoe tear, lattice degeneration, high myopia) -> liquefied vitreous dissects between neurosensory retina and retinal pigment epithelium (RPE). Features: Flashes + Floaters + Curtain falling; convex, corrugated, mobile retina. Treatment: Pneumatic retinopexy, Scleral buckle, or Pars Plana Vitrectomy. 2. Tractional RD: Proliferative DR; concave, immobile, NO break. 3. Exudative RD: Harada disease, VKH, eclampsia; shifting fluid, NO break.",
        "citation": "Khurana's Comprehensive Ophthalmology, 7th Ed, Chapter 12 (Retina), p. 288-298.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Retinal Detachment: Rhegmatogenous vs Exudative",
        "stem": (
            "A 28-year-old primigravida at 34 weeks gestation with severe preeclampsia (BP 180/115 mmHg) develops acute, painless, profound visual loss in both eyes. "
            "Fundus examination reveals bilateral, smooth, highly elevated bullous retinal detachments without any visible tears or holes. "
            "The subretinal fluid characteristically shifts gravity-dependently when the patient changes position from upright to supine ('shifting fluid sign'). "
            "What is the management of choice for this retinal detachment?"
        ),
        "options": [
            ("Immediate bilateral scleral buckling and cryopexy", False, "Scleral buckle is for rhegmatogenous RD with breaks; exudative RD has no breaks and resolves with systemic control."),
            ("Control of blood pressure and delivery of the fetus; exudative detachment spontaneously resolves completely after delivery", True, None),
            ("Emergency pars plana vitrectomy with silicone oil endotamponade", False, "Vitrectomy is contraindicated in sterile exudative RD of preeclampsia."),
            ("Intravitreal injection of tissue plasminogen activator (tPA)", False, "tPA has no role in serous neurosensory retinal detachment.")
        ],
        "pearl": "Exudative (Serous) Retinal Detachment: Caused by breakdown of blood-retina barrier (choroidal vascular hyperpermeability). Key causes: Severe Preeclampsia / Eclampsia, Vogt-Koyanagi-Harada (VKH) disease, Malignant hypertension, Choroidal hemangioma. Hallmark sign: SHIFTING FLUID (fluid moves rapidly to lowest dependent portion with changes in patient posture). Retina is smooth and bullous with NO tears. Resolves spontaneously once underlying etiology is treated!",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 16 (Retinal Detachment), p. 658-664.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Optic Neuritis & Papilledema Differentials",
        "stem": (
            "A 27-year-old female presents with subacute, painful loss of vision in her right eye developing over 3 days. "
            "She reports that the retro-orbital eye pain is markedly exacerbated by eye movements. Visual acuity is reduced to counting fingers at 2 meters. "
            "Color vision is disproportionately impaired (severe dyschromatopsia). Swinging-flashlight examination reveals a Relative Afferent Pupillary Defect (RAPD / Marcus Gunn pupil) "
            "in the right eye. Funduscopic examination shows a completely NORMAL-APPEARING optic disc and retinal vasculature in both eyes ('neither the doctor nor the patient sees anything'). "
            "What is the diagnosis, and which demyelinating disease is she at high risk for developing?"
        ),
        "options": [
            ("Retrobulbar Optic Neuritis; Multiple Sclerosis", True, None),
            ("Papilledema; Idiopathic Intracranial Hypertension (Pseudotumor cerebri)", False, "Papilledema is bilateral optic disc swelling due to raised ICP with normal visual acuity initially, no eye pain on movement, and no RAPD."),
            ("Anterior Ischemic Optic Neuropathy (AION); Giant Cell Arteritis", False, "AION presents in elderly individuals (>60 yrs) with painless, sudden altitudinal visual field defect and pale swollen disc."),
            ("Central Retinal Artery Occlusion; Carotid atherosclerosis", False, "CRAO features painless sudden complete blindness with a cherry-red spot at the macula.")
        ],
        "pearl": "Optic Neuritis: Typified by young female (20-40 yrs) with subacute unilateral vision loss + PAIN on eye movements (due to traction of superior and medial rectus muscle origins on the optic nerve sheath at the annulus of Zinn). Features: RAPD (Marcus Gunn pupil) + Disproportionate loss of color vision (red desaturation) + Central scotoma. In Retrobulbar Neuritis (65%): Disc looks completely normal! 50-70% develop Multiple Sclerosis within 15 years. ONTT Protocol: IV Methylprednisolone (1 g/day for 3 days) speeds visual recovery; ORAL PREDNISONE ALONE IS CONTRAINDICATED as it increases recurrence rates!",
        "citation": "Khurana's Comprehensive Ophthalmology, 7th Ed, Chapter 13 (Optic Nerve), p. 308-316.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Optic Neuritis & Papilledema Differentials",
        "stem": (
            "A 29-year-old obese female presents with chronic generalized throbbing headaches, transient obscurations of vision lasting a few seconds "
            "when bending forward, and pulsatile synchronous tinnitus. Brain MRI with MR venography reveals completely normal brain parenchyma and ventricles "
            "with no mass or dural venous sinus thrombosis. Lumbar puncture in the lateral decubitus position shows an elevated opening pressure of 34 cm H2O "
            "(normal <20-25 cm H2O) with normal CSF biochemical and microscopic analysis. Fundus examination reveals bilateral, symmetrical, severe optic disc swelling "
            "with blurred margins, flame hemorrhages, and absence of spontaneous venous pulsations. What is the diagnosis and first-line medical therapy?"
        ),
        "options": [
            ("Idiopathic Intracranial Hypertension (Pseudotumor Cerebri); Weight reduction and oral Acetazolamide", True, None),
            ("Bilateral optic neuritis; High-dose oral Prednisolone monotherapy", False, "Steroids are not first-line for pseudotumor cerebri and can trigger rebound intracranial hypertension on withdrawal."),
            ("Cavernous sinus thrombosis; High-dose IV Heparin and broad-spectrum antibiotics", False, "Cavernous sinus thrombosis presents acutely with chemosis, proptosis, and ophthalmoplegia of CN III, IV, VI."),
            ("Malignant astrocytoma; Surgical craniotomy and debulking", False, "MRI was entirely normal, ruling out space-occupying lesions.")
        ],
        "pearl": "Papilledema vs Papillitis: Papilledema = Passive, non-inflammatory bilateral disc swelling caused by RAISED INTRACRANIAL PRESSURE (ICP). Cardinal signs: Bilateral, visual acuity PRESERVED early, transient obscurations of vision (seconds), enlarged blind spot on fields. Idiopathic Intracranial Hypertension (IIH / Pseudotumor Cerebri): Obese female of childbearing age + headache + papilledema + normal MRI + elevated opening CSF pressure (>25 cm H2O). DOC: Weight loss + Acetazolamide (carbonic anhydrase inhibitor reduces CSF production). Refractory: Optic nerve sheath fenestration or VP/LP shunt.",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 19 (Neuro-ophthalmology), p. 770-782.",
        "difficulty": "moderate"
    }
]
