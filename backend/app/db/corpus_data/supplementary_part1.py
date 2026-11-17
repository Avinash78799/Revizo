"""
Supplementary High-Yield NEET-PG Clinical Questions: Part 1
Covers: Ophthalmology (6), Obstetrics & Gynecology (6), Radiodiagnosis (6), Dermatology (6).
"""

SUPPLEMENTARY_PART1 = [
    # =========================================================================
    # --- OPHTHALMOLOGY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Ophthalmology",
        "concept_name": "Glaucoma: Open-Angle vs Angle-Closure & Pharmacotherapy",
        "stem": (
            "A 62-year-old hyperopic female presents to the emergency room with excruciating right eye pain, "
            "severe ipsilateral hemicranial headache, nausea, and vomiting that began after sitting in a dark movie theater. "
            "She reports seeing rainbow-colored halos around streetlights and blurred vision. Examination reveals an intraocular "
            "pressure (IOP) of 56 mmHg in the right eye, a ciliary flush, a steamy 'ground-glass' cornea, a shallow anterior chamber, "
            "and a vertically oval, mid-dilated, non-reactive pupil. "
            "Which of the following is the definitive curative procedure to prevent recurrence once acute IOP is medically controlled?"
        ),
        "options": [
            ("Nd:YAG Laser Peripheral Iridotomy (LPI) in the affected eye and prophylactic LPI in the fellow eye", True, None),
            ("Topical Atropine 1% sulfate eyedrops every 15 minutes", False, "Atropine is a cycloplegic mydriatic that dilates the pupil, causing further crowding of the angle and worsening pupillary block."),
            ("Immediate emergent Trabeculectomy with Mitomycin C", False, "Filtration surgery is reserved for refractory cases; laser peripheral iridotomy is the definitive first-line procedure."),
            ("Long-term topical Latanoprost monotherapy without procedural intervention", False, "Prostaglandin analogs increase uveoscleral outflow in open-angle glaucoma; they do not relieve pupillary block.")
        ],
        "pearl": "Acute Primary Angle-Closure Glaucoma (PACG): Trigger: Pupillary block in shallow anterior chambers (hyperopes) triggered by mydriasis (darkness, anticholinergics). Clinical triad: Rock-hard eye (IOP >50 mmHg) + Steamy cornea + Mid-dilated non-reactive oval pupil. Immediate medical management: IV Mannitol (20% osmotic diuretic), IV/oral Acetazolamide (carbonic anhydrase inhibitor), topical Beta-blocker (Timolol), and topical Pilocarpine 1-2% (miotic to pull iris root away from trabecular meshwork once IOP <30 mmHg). DEFINITIVE TREATMENT: Nd:YAG Laser Peripheral Iridotomy (creates a bypass channel between posterior and anterior chambers). ALWAYS perform prophylactic LPI in the contralateral fellow eye because 50% will develop an acute attack within 5 years.",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 11 (Glaucoma), p. 342-349; Parson's Diseases of the Eye, 23rd Ed, p. 256-264.",
        "difficulty": "medium"
    },
    {
        "subject": "Ophthalmology",
        "concept_name": "Diabetic Retinopathy: Staging & Anti-VEGF / Laser Management",
        "stem": (
            "A 54-year-old male with an 18-year history of poorly controlled type 2 diabetes mellitus (HbA1c 9.8%) presents for a routine "
            "dilated fundus examination. Funduscopy demonstrates extensive microaneurysms, blot hemorrhages in all 4 quadrants, prominent "
            "venous beading in 2 quadrants, and intraretinal microvascular abnormalities (IRMA) in 1 quadrant. Crucially, there is NO "
            "neovascularization of the disc (NVD) or neovascularization elsewhere (NVE). "
            "According to the Early Treatment Diabetic Retinopathy Study (ETDRS) 4-2-1 rule, what is the clinical diagnosis and recommended action?"
        ),
        "options": [
            ("Severe Non-Proliferative Diabetic Retinopathy (NPDR); High risk of progression to proliferative retinopathy within 1 year requiring close monitoring or Panretinal Photocoagulation (PRP)", True, None),
            ("Proliferative Diabetic Retinopathy (PDR); Immediate emergency Pars Plana Vitrectomy", False, "PDR requires active neovascularization (NVD/NVE) or vitreous hemorrhage. Vitrectomy is not indicated here."),
            ("Mild Non-Proliferative Diabetic Retinopathy; Return for annual screening after 12 months", False, "Mild NPDR only has microaneurysms; the presence of 4-2-1 criteria defines severe NPDR."),
            ("Clinically Significant Macular Edema (CSME); Focal argon laser photocoagulation to optic nerve head", False, "Laser is never applied to the optic nerve head; ETDRS defines CSME by retinal thickening at the fovea.")
        ],
        "pearl": "ETDRS 4-2-1 Rule for Severe NPDR: Diagnosed when ANY ONE of the following is present WITHOUT neovascularization: 1. Diffuse microaneurysms/hemorrhages in all 4 quadrants | 2. Venous beading in &ge;2 quadrants | 3. Prominent IRMA in &ge;1 quadrant. (If 2 or more criteria met = Very Severe NPDR). 50% of severe NPDR progress to Proliferative Diabetic Retinopathy (PDR) within 1 year. Hallmark of PDR: Neovascularization of the Disc (NVD) or Neovascularization Elsewhere (NVE) driven by ischemia-induced vascular endothelial growth factor (VEGF). Gold standard treatment for high-risk PDR: Panretinal Photocoagulation (PRP; destroys ischemic peripheral retina to reduce VEGF load) +/- Intravitreal Anti-VEGF (Aflibercept / Ranibizumab / Bevacizumab).",
        "citation": "Parson's Diseases of the Eye, 23rd Ed, Chapter 20 (Diseases of the Retina), p. 308-315; ETDRS Report No. 10.",
        "difficulty": "hard"
    },
    {
        "subject": "Ophthalmology",
        "concept_name": "Retinal Vascular Occlusion: CRAO vs CRVO",
        "stem": (
            "A 68-year-old male with hypertension, carotid atherosclerosis, and paroxysmal atrial fibrillation experiences sudden, dramatic, "
            "completely painless loss of vision in his left eye upon waking. Visual acuity is reduced to 'counting fingers at 1 meter'. "
            "Pupillary examination demonstrates an afferent pupillary defect (Marcus Gunn pupil) in the left eye. "
            "Dilated funduscopy reveals a milky-white, opaque, ischemic ground-glass retina with a strikingly bright 'cherry-red spot' "
            "at the fovea and attenuated, thread-like retinal arterioles with segmented blood columns ('boxcarring'). "
            "What anatomical feature explains the persistent 'cherry-red spot' at the fovea in this condition?"
        ),
        "options": [
            ("The thin foveola lacks inner retinal layers and ganglion cells, allowing visualization of the underlying vascular choroid supplied by the ciliary circulation", True, None),
            ("Massive preretinal boat-shaped hemorrhage pooling beneath the internal limiting membrane at the macula", False, "Boat-shaped hemorrhages occur in subhyaloid/preretinal hemorrhage, not arterial occlusion."),
            ("Selective sparing of the central retinal vein permitting engorgement of macular venules", False, "CRAO is an arterial occlusion; venous engorgement ('blood and thunder') is seen in CRVO."),
            ("Direct toxic extravasation of hemoglobin through damaged retinal pigment epithelium (RPE)", False, "The RPE is intact; the appearance is optical contrast between opaque edema and thin foveola.")
        ],
        "pearl": "Central Retinal Artery Occlusion (CRAO): Ophthalmic emergency ('ocular stroke'). Etiology: Embolus (carotid plaque / Hollenhorst cholesterol crystal, or cardiac thrombus) occluding the central retinal artery (end artery from ophthalmic artery). Findings: Sudden painless profound monocular vision loss + Marcus Gunn pupil + Milky-white retinal ischemic whitening + 'Cherry-red spot' at the macula (foveola has no ganglion cell/nerve fiber layers; vascular choroid supplied by short posterior ciliary arteries shines through). Note: If a Cilioretinal Artery (present in 15-20% of population from posterior ciliary system) is present, central macular vision is preserved! Emergency measures: Ocular massage, paracentesis of anterior chamber, sublingual isosorbide dinitrate, and IV Acetazolamide to lower IOP and dislodge embolus downstream.",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 13 (Retinal Vascular Disease), p. 530-536; Harrison's Principles of Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Ophthalmology",
        "concept_name": "Corneal Ulceration: Bacterial vs Fungal Keratitis",
        "stem": (
            "A 40-year-old agricultural laborer presents with a painful red left eye, photophobia, foreign body sensation, and blurred "
            "vision 5 days after being struck by a flying sugarcane leaf. Examination reveals ciliary congestion, a grayish-white corneal "
            "infiltrate with feathery, indistinct margins, multiple discrete satellite stromal lesions surrounding the main infiltrate, "
            "an elevated endothelial plaque, and a fixed, non-progressive hypopyon in the anterior chamber. "
            "Potassium hydroxide (KOH 10%) mount of corneal scrapings shows septate hyphae branching at 45 degrees. "
            "Which of the following is the topical drug of choice for this infection?"
        ),
        "options": [
            ("Topical Natamycin 5% suspension hourly", True, None),
            ("Topical Moxifloxacin 0.5% eyedrops with Dexamethasone 0.1% drops", False, "Topical corticosteroids are ABSOLUTELY CONTRAINDICATED in fungal keratitis as they cause rapid fungal proliferation and corneal perforation."),
            ("Topical Ganciclovir 0.15% gel 5 times daily", False, "Ganciclovir is an antiviral used for Herpes Simplex dendritic epithelial keratitis, not fungal infections."),
            ("Topical Tobramycin 1.4% with Ceftriaxone fortified eyedrops", False, "Antibacterial drops do not treat fungal keratitis caused by Aspergillus/Fusarium.")
        ],
        "pearl": "Fungal Keratitis (Mycotic Ulcer): Classic history: Trauma with vegetative matter (sugarcane leaf, tree twig, cow tail). Organisms: Filamentous fungi (Aspergillus, Fusarium) in tropical/agricultural settings; Candida in immunosuppressed. Clinical signs: Dry, grayish-white elevated slough + FEATHERY INDISTINCT MARGINS + SATELLITE LESIONS + Endothelial plaque + Sterile/fixed hypopyon. Diagnosis: 10% KOH wet mount (shows hyphae) and Gram stain, followed by culture on Sabouraud's Dextrose Agar (SDA) without cycloheximide. Drug of choice: Natamycin 5% suspension (polyene, DOC for filamentous fungi). Amphotericin B 0.15% is preferred for Candida. CRITICAL RULE: Corticosteroids are STRICTLY CONTRAINDICATED (causes unchecked fungal growth and descemetocele perforation).",
        "citation": "Parson's Diseases of the Eye, 23rd Ed, Chapter 13 (Diseases of the Cornea), p. 182-188; Dhingra ENT & Eye Essentials.",
        "difficulty": "medium"
    },
    {
        "subject": "Ophthalmology",
        "concept_name": "Retinal Detachment: Rhegmatogenous vs Exudative vs Tractional",
        "stem": (
            "A 28-year-old high myope (-7.50 D in both eyes) notices sudden flashes of light (photopsia) in his temporal visual field, "
            "followed by a shower of black floating spots ('cobwebs'). Over the next 24 hours, he describes a dark 'curtain or shadow falling "
            "over the superior field of vision'. Slit-lamp biomicroscopy of the anterior vitreous reveals pigment granules ('tobacco-dusting' "
            "or Shafer's sign). Dilated indirect ophthalmoscopy reveals an undulating, convex, grayish-white detached retina with a full-thickness "
            "horseshoe retinal tear at the equator. "
            "What type of retinal detachment does this patient have, and what is the underlying pathophysiology?"
        ),
        "options": [
            ("Rhegmatogenous Retinal Detachment; A full-thickness retinal break allows liquefied vitreous fluid to pass into the subretinal space, separating neurosensory retina from RPE", True, None),
            ("Tractional Retinal Detachment; Fibrovascular membranes contract and pull the retina anteriorly without any retinal break", False, "Tractional RD (seen in PDR) has concave surfaces, no retinal break, and does not show Shafer's sign."),
            ("Exudative (Serous) Retinal Detachment; Hydrostatic fluid leakage from choroidal tumor with shifting fluid", False, "Exudative RD has shifting fluid, smooth convex elevation without breaks, seen in Harada's or choroidal melanoma."),
            ("PVD without detachment; Benign collapse of vitreous gel requiring reassurance only", False, "Presence of a horseshoe tear with subretinal fluid and Shafer's sign confirms an active rhegmatogenous retinal detachment.")
        ],
        "pearl": "Retinal Detachment (RD) Classification: 1. RHEGMATOGENOUS RD (Most common): Caused by a retinal break (horseshoe tear / atrophic hole) allowing liquefied synchytic vitreous into the subretinal space (between neurosensory retina and retinal pigment epithelium). Preceded by Posterior Vitreous Detachment (PVD) causing flashes (photopsia) and floaters. Key sign: SHAFER'S SIGN (pigment cells / 'tobacco dust' in anterior vitreous). 2. TRACTIONAL RD: Caused by contraction of fibrovascular membranes pulling retina (seen in Proliferative Diabetic Retinopathy, ROP). No retinal break, concave surface, immobile. 3. EXUDATIVE / SEROUS RD: Subretinal fluid accumulation without breaks or traction (e.g., VKH disease, choroidal hemangioma, preeclampsia). Hallmark: SHIFTING FLUID (fluid shifts with head position changes).",
        "citation": "Kanski's Clinical Ophthalmology, 9th Ed, Chapter 15 (Retinal Detachment), p. 660-672; Parson's Diseases of the Eye.",
        "difficulty": "medium"
    },
    {
        "subject": "Ophthalmology",
        "concept_name": "Uveitis: Anterior Uveitis, HLA-B27 & Hypopyon",
        "stem": (
            "A 26-year-old male with chronic inflammatory low back pain and morning stiffness lasting over an hour (HLA-B27 positive) "
            "presents with severe acute pain, photophobia, redness, and lacrimation in his right eye. "
            "Slit-lamp examination demonstrates ciliary (circumcorneal) flush, fine mutton-fat keratic precipitates (KPs) on the corneal "
            "endothelium, 3+ cells and flare in the anterior chamber (Tyndall effect), and posterior synechiae giving rise to an irregular, "
            "'festooned pupil' upon dilation. "
            "Which of the following classes of eyedrops is ESSENTIAL in the immediate management to relieve ciliary spasm and prevent complete pupillary seclusion (seclusio pupillae)?"
        ),
        "options": [
            ("Topical Cycloplegic-Mydriatic (e.g., Homatropine 2% or Atropine 1%) combined with intensive topical Corticosteroids", True, None),
            ("Topical Pilocarpine 2% miotic eyedrops every 30 minutes", False, "Pilocarpine causes intense miosis and ciliary spasm, which increases pupil contact with lens, promoting irreversible circular posterior synechiae."),
            ("Topical Prostaglandin analogs (Latanoprost 0.005%) twice daily", False, "Prostaglandin analogs exacerbate intraocular inflammation and blood-aqueous barrier breakdown in active uveitis."),
            ("Topical Carbonic Anhydrase Inhibitor monotherapy without steroids", False, "CAIs do not treat the underlying inflammatory cascade or prevent devastating pupillary adhesions.")
        ],
        "pearl": "Acute Anterior Uveitis (Iridocyclitis): Strongly associated with HLA-B27 spondyloarthropathies (Ankylosing Spondylitis, Reactive Arthritis, Psoriatic Arthritis, IBD). Cardinal signs: Circumcorneal ciliary flush + Aqueous cells and flare (Tyndall phenomenon) + Keratic precipitates (KPs on endothelium) + Constricted sluggish pupil + Posterior Synechiae (adhesions of iris to anterior lens capsule; causes irregular 'festooned pupil' when dilated). Complications: Seclusio pupillae (360-degree adhesion) leading to iris bombé, secondary angle-closure glaucoma, and complicated cataract. Treatment Pillars: 1. Cycloplegic-Mydriatics (Homatropine / Atropine): Relieves agonizing ciliary spasm pain and breaks/prevents posterior synechiae! 2. Intensive Topical Corticosteroids (Prednisolone acetate 1%): Suppresses intraocular inflammation.",
        "citation": "Parson's Diseases of the Eye, 23rd Ed, Chapter 15 (Diseases of the Uveal Tract), p. 216-224; Kanski's Ophthalmology.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- OBSTETRICS & GYNECOLOGY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Obstetrics & Gynecology",
        "concept_name": "Hypertensive Disorders of Pregnancy: Preeclampsia & Eclampsia Management",
        "stem": (
            "A 24-year-old primigravida at 34 weeks of gestation presents to the triage unit with a throbbing frontal headache, scotomata, "
            "and epigastric pain. Her blood pressure is 168/112 mmHg on two occasions 4 hours apart, and urine dipstick reveals 3+ protein. "
            "While being positioned on the examination bed, she suddenly develops facial twitching followed by generalized tonic-clonic convulsions. "
            "After securing her airway and placing her in the left lateral tilt position, what is the drug of choice, loading dose, and clinical monitoring required for convulsion control?"
        ),
        "options": [
            ("Magnesium Sulfate (Pritchard regimen: 4 g IV over 10-15 min + 10 g IM [5 g in each buttock]); Monitor patellar reflexes, respiratory rate (&ge;12/min), and urine output (&ge;30 mL/hr)", True, None),
            ("Intravenous Diazepam 10 mg push repeated every 5 minutes; Monitor arterial blood gas and cardiac telemetry", False, "Benzodiazepines cause fetal respiratory depression and hypothermia; MgSO4 is far superior for eclampsia."),
            ("Intravenous Phenytoin 1 g infusion over 1 hour; Monitor serum drug levels and ECG QTc interval", False, "Phenytoin was proven inferior to Magnesium Sulfate in the landmark Collaborative Eclampsia Trial."),
            ("Immediate IV Labetalol 20 mg bolus as sole anticonvulsant without neuroprotective agents", False, "Labetalol lowers blood pressure but has zero anticonvulsant action against eclamptic seizures.")
        ],
        "pearl": "Eclampsia & Magnesium Sulfate Regimens: Drug of choice for prophylaxis and treatment of eclamptic convulsions: Magnesium Sulfate (Collaborative Eclampsia Trial showed 52% reduction in recurrent seizures vs diazepam). Pritchard Regimen: Loading: 4 g IV (20% solution) slowly over 10-15 min + 10 g IM (50% solution, 5 g in each buttock). Maintenance: 5 g IM in alternate buttocks every 4 hours. Zuspan Regimen: 4 g IV loading over 20 min, then 1 g/hr continuous IV infusion. CLINICAL MONITORING CRITERIA (before each maintenance dose): 1. Knee jerk (patellar reflex) MUST be present (loss of reflex occurs at 8-10 mEq/L, earliest sign of toxicity) | 2. Respiratory rate &ge;12/min (depression occurs at 12 mEq/L) | 3. Urine output &ge;30 mL/hr (100 mL in 4 hours; Mg is excreted exclusively by kidneys!). Therapeutic level: 4-7 mEq/L. Cardiac arrest occurs at >15-20 mEq/L. SPECIFIC ANTIDOTE FOR TOXICITY: 10 mL of 10% Calcium Gluconate IV slowly over 10 minutes.",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 17 (Hypertensive Disorders in Pregnancy), p. 218-232; Williams Obstetrics, 26th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Obstetrics & Gynecology",
        "concept_name": "Postpartum Hemorrhage (PPH): Etiology & Stepwise Surgical Control",
        "stem": (
            "A 28-year-old G3P2 undergoes an uncomplicated full-term vaginal delivery of an 4.2 kg infant. Ten minutes after expulsion "
            "of an intact placenta, profuse vaginal bleeding occurs. Abdominal palpation reveals a soft, boggy, poorly contracted uterus "
            "reaching above the umbilicus. Continuous uterine massage and an intravenous infusion of 20 IU Oxytocin fail to arrest the bleeding. "
            "Estimated blood loss exceeds 900 mL, and the patient is tachycardic (pulse 124 bpm, BP 88/54 mmHg). "
            "Which of the following uterotonic agents is CONTRAINDICATED if the patient has a known history of moderate-to-severe bronchial asthma?"
        ),
        "options": [
            ("15-methyl Prostaglandin F2-alpha (Carboprost / Hemabate) 0.25 mg IM", True, None),
            ("Methylergonovine (Methergine) 0.2 mg IM", False, "Methergine is contraindicated in hypertension and preeclampsia due to intense vasoconstriction, not in asthma."),
            ("Misoprostol (Prostaglandin E1) 800 mcg sublingually/rectally", False, "Misoprostol (PGE1) causes mild bronchodilation and shivering/fever; it is safe in asthmatics."),
            ("Tranexamic acid 1 g IV over 10 minutes", False, "Tranexamic acid is an antifibrinolytic indicated within 3 hours of PPH onset in all patients, including asthmatics.")
        ],
        "pearl": "Postpartum Hemorrhage (PPH) Management: Definition: Blood loss &ge;500 mL following vaginal delivery or &ge;1000 mL following cesarean section. 4 T's Etiology: Tone (Atony ~70-80%, most common) > Trauma (lacerations ~20%) > Tissue (retained cotyledons ~10%) > Thrombin (coagulopathy ~1%). UTEROTONIC PHARMACOPEIA & CONTRAINDICATIONS: 1. Oxytocin: 1st line agent, safe in all patients | 2. Methylergonovine (Methergine): CONTRAINDICATED in Hypertension / Preeclampsia / Heart disease (triggers hypertensive crisis & stroke) | 3. Carboprost (15-methyl PGF2a): CONTRAINDICATED in BRONCHIAL ASTHMA (potent bronchoconstrictor causing fatal bronchospasm) | 4. Misoprostol (PGE1): 800 mcg per rectum/sublingual, safe in asthma. STEPWISE SURGICAL CASCADE for refractory atony: Uterine tamponade balloon (Bakri balloon) &rarr; B-Lynch uterine compression sutures &rarr; Bilateral Uterine artery ligation (O'Leary) &rarr; Bilateral Internal Iliac (Hypogastric) artery anterior division ligation &rarr; Subtotal/Total Peripartum Hysterectomy.",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 29 (Postpartum Hemorrhage), p. 410-422; ACOG Practice Bulletin No. 183.",
        "difficulty": "medium"
    },
    {
        "subject": "Obstetrics & Gynecology",
        "concept_name": "Ectopic Pregnancy: Diagnostic Thresholds & Medical vs Surgical Criteria",
        "stem": (
            "A 27-year-old nulligravida presents with 6 weeks of amenorrhea, mild dull aching right lower quadrant pain, and spotting. "
            "She is hemodynamically stable (BP 118/74 mmHg, pulse 76 bpm). Bimanual pelvic examination reveals normal uterine size with mild "
            "right adnexal tenderness without cervical motion tenderness. Serum quantitative beta-hCG is 2400 mIU/mL. "
            "Transvaginal ultrasonography (TVUS) shows an empty uterine cavity with an endometrial thickness of 12 mm, no fluid in the pouch "
            "of Douglas, and an unruptured right tubal gestational mass measuring 2.4 cm without visible embryonic cardiac motion. "
            "Which of the following is the most appropriate management for this patient?"
        ),
        "options": [
            ("Single-dose intramuscular Methotrexate (50 mg/m² BSA) with serial beta-hCG monitoring on days 4 and 7", True, None),
            ("Immediate emergency exploratory laparotomy with right total salpingectomy", False, "Laparotomy is reserved for hemodynamically unstable ruptured ectopic pregnancy. She is stable with an unruptured mass."),
            ("Repeat transvaginal ultrasound in 4 weeks without intervention", False, "An ectopic pregnancy requires active treatment; waiting 4 weeks invites tubal rupture and exsanguination."),
            ("Uterine suction curettage to evacuate an assumed missed abortion", False, "The empty uterus at beta-hCG 2400 mIU/mL with an adnexal mass confirms ectopic pregnancy; D&C will not treat the tubal mass.")
        ],
        "pearl": "Ectopic Pregnancy: Sites: Ampulla (70%, most common overall) > Isthmus (12%, ruptures earliest at 6-8 wks) > Fimbria (11%) > Interstitial / Cornual (2-3%, ruptures latest at 12-14 wks with cataclysmic bleeding due to uterine artery anastomosis). Discriminatory Zone: Serum beta-hCG level at which an intrauterine gestational sac MUST be visible on TVUS (1500-2000 mIU/mL; 6000 mIU/mL on transabdominal US). Empty uterus above discriminatory zone = Ectopic until proven otherwise! MEDICAL MANAGEMENT WITH METHOTREXATE (Folate antagonist inhibiting DHFR): Criteria for Methotrexate: 1. Hemodynamically stable | 2. Unruptured ectopic mass | 3. Gestational mass &le;3.5 cm in largest diameter | 4. No embryonic cardiac activity on TVUS | 5. Baseline serum beta-hCG <5000 mIU/mL. Protocol: Single-dose IM Methotrexate (50 mg/m²). Check beta-hCG on Day 4 and Day 7. A fall of &ge;15% between Day 4 and Day 7 indicates successful medical resolution.",
        "citation": "Williams Obstetrics, 26th Ed, Chapter 19 (Ectopic Pregnancy), p. 370-384; DC Dutta's Obstetrics, 9th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Obstetrics & Gynecology",
        "concept_name": "Gestational Trophoblastic Disease: Complete vs Partial Mole & Follow-up",
        "stem": (
            "A 22-year-old G1P0 at 11 weeks of amenorrhea presents with severe hyperemesis gravidarum, dark prune-juice vaginal bleeding, "
            "and bilateral palpable ovarian masses. Examination reveals a fundal height corresponding to 18 weeks of gestation. "
            "Her blood pressure is 152/98 mmHg. Laboratory testing shows a serum beta-hCG of 320,000 mIU/mL and suppressed TSH with elevated free T4. "
            "Pelvic ultrasonography demonstrates an enlarged uterus with an echogenic intra-cavitary mass displaying a classic 'snowstorm' "
            "or 'bunch-of-grapes' vesicular pattern with absent fetal parts, alongside bilateral theca lutein ovarian cysts. "
            "What is the expected karyotype and p57 immunohistochemical staining pattern for this pathology?"
        ),
        "options": [
            ("46,XX (diploid, 100% androgenetic paternal origin); Absent (negative) p57 expression in cytotrophoblasts and villous stroma", True, None),
            ("69,XXY (triploid, dispermic fertilization); Strong diffuse nuclear p57 expression", False, "Triploid karyotype with positive p57 is the hallmark of Partial hydatidiform mole, which contains fetal parts."),
            ("45,X0 (Turner syndrome); Weak mosaic cytoplasmic p57 expression", False, "Turner syndrome is not a molar pregnancy; complete mole is diploid."),
            ("46,XY (maternal uniparental disomy); Positive membranous p57 expression", False, "Complete mole is of purely paternal origin (androgenesis), silencing maternally expressed p57.")
        ],
        "pearl": "Complete vs Partial Hydatidiform Mole: 1. COMPLETE MOLE: Karyotype: 46,XX (90%) or 46,XY (10%), 100% PATERNAL in origin (androgenetic: duplication of single sperm in an enucleated ovum). Fetal tissue: Completely ABSENT. Villi: Generalized diffuse hydropic swelling with central cisterns & diffuse circumferential trophoblastic hyperplasia. p57 (KIP2): NEGATIVE (p57 is a maternally imprinted gene; since maternal genome is absent, complete mole shows zero p57 expression!). Clinical presentation: Uterus size > dates + Extremely high beta-hCG (>100,000) + Prune-juice discharge + Snowstorm USG + Bilateral Theca Lutein cysts + Early preeclampsia (<20 wks) + Hyperthyroidism (beta-hCG stimulates TSH receptor). Risk of choriocarcinoma: 2.5-4%. 2. PARTIAL MOLE: Karyotype: TRIPLOID 69,XXY / 69,XXX (fertilization of normal haploid ovum by 2 sperms). Fetal parts: PRESENT. p57: POSITIVE. Uterus size < dates. Risk of choriocarcinoma: <0.5%.",
        "citation": "Novak's Gynecology, 16th Ed, Chapter 40; DC Dutta's Textbook of Obstetrics, 9th Ed, p. 190-198.",
        "difficulty": "hard"
    },
    {
        "subject": "Obstetrics & Gynecology",
        "concept_name": "Polycystic Ovary Syndrome (PCOS): Rotterdam Criteria & Ovulation Induction",
        "stem": (
            "A 25-year-old woman presents to the reproductive medicine clinic with primary infertility for 2 years, irregular menstrual cycles "
            "(oligomenorrhea every 60-90 days), and worsening facial hirsutism and acne. Her BMI is 29.4 kg/m². "
            "Physical examination shows Ferriman-Gallwey hirsutism score of 12 and velvety hyperpigmented plaques on the nape of her neck "
            "(acanthosis nigricans). Pelvic ultrasound reveals bilateral enlarged ovaries (volume 12 mL each) with 24 peripheral subcapsular "
            "follicles measuring 2-8 mm arranged in a 'necklace pattern' around an echogenic central stroma. "
            "According to the international evidence-based guidelines, what is the FIRST-LINE pharmacological agent for ovulation induction in this patient?"
        ),
        "options": [
            ("Letrozole (Aromatase Inhibitor) 2.5 mg daily for 5 days starting on cycle day 3", True, None),
            ("Clomiphene Citrate 50 mg daily as preferred first-line over aromatase inhibitors", False, "International guidelines (Teede et al.) established Letrozole as superior to Clomiphene with higher live-birth and mono-ovulation rates."),
            ("Metformin monotherapy 1500 mg daily as sole ovulation agent", False, "Metformin improves insulin resistance and menstrual regularity but is inferior to Letrozole for ovulation and live births."),
            ("Combined oral contraceptive pills (Drospirenone + Ethinylestradiol)", False, "COCPs regulate bleeding and treat hirsutism in women NOT seeking pregnancy; they prevent ovulation and cannot treat infertility.")
        ],
        "pearl": "Polycystic Ovary Syndrome (PCOS) - Rotterdam Consensus Criteria (2 of 3 required): 1. Oligo- or anovulation | 2. Clinical and/or biochemical signs of hyperandrogenism (Hirsutism FG score &ge;8, acne, elevated free testosterone) | 3. Polycystic ovaries on ultrasound (&ge;20 follicles per ovary measuring 2-9 mm, and/or ovarian volume &ge;10 mL). Associated features: Elevated LH:FSH ratio (>2:1), Insulin resistance, Acanthosis nigricans, and metabolic syndrome. MANAGEMENT OF INFERTILITY: FIRST-LINE OVULATION INDUCTION AGENT: LETROZOLE (non-steroidal aromatase inhibitor, 2.5-7.5 mg/day on cycle days 3-7). Why Letrozole over Clomiphene? Inhibits estrogen biosynthesis, releasing hypothalamic-pituitary axis from negative feedback, producing physiologic FSH surge WITHOUT anti-estrogenic endometrial thinning or cervical mucus hostility. Results in significantly higher live birth and clinical pregnancy rates with lower multiple gestation risk compared to Clomiphene Citrate.",
        "citation": "Novak's Gynecology, 16th Ed, Chapter 27 (Amenorrhea & PCOS); Teede HJ et al., International Evidence-based Guideline for PCOS, 2023.",
        "difficulty": "medium"
    },
    {
        "subject": "Obstetrics & Gynecology",
        "concept_name": "Endometriosis: Pathogenesis, Triad & Diagnostic Gold Standard",
        "stem": (
            "A 29-year-old nulliparous physician presents with a 4-year history of severe, progressively worsening secondary dysmenorrhea "
            "that begins 2 days prior to menstruation, deep dyspareunia, and cyclical dyschezia (painful defecation during menses). "
            "She has failed therapy with NSAIDs and cyclical oral contraceptives. Pelvic examination reveals extreme tenderness in the "
            "posterior fornix, fixed retroverted uterus, and palpable nodular induration along the uterosacral ligaments. "
            "Transvaginal ultrasound demonstrates bilateral well-defined ovarian cystic lesions with low-level homogeneous internal echoes ('ground-glass' appearance). "
            "What is the GOLD STANDARD investigation for establishing a definitive diagnosis and staging of this disease?"
        ),
        "options": [
            ("Diagnostic Laparoscopy with direct visualization and histological biopsy of endometriotic lesions", True, None),
            ("Serum CA-125 level elevation (>35 U/mL)", False, "CA-125 is non-specific and elevated in adenomyosis, pelvic infection, and ovarian cancer; it is not a diagnostic gold standard."),
            ("Pelvic Magnetic Resonance Imaging (MRI) with contrast", False, "MRI is excellent for deep infiltrating endometriosis (DIE) but cannot replace laparoscopy with biopsy as the definitive gold standard."),
            ("Transvaginal Ultrasound guided fine-needle aspiration of ovarian cysts", False, "Aspiration carries high risk of chemical peritonitis, infection, and recurrence; it is not recommended for diagnosis.")
        ],
        "pearl": "Endometriosis: Presence of functional endometrial glands and stroma outside the uterine cavity. Leading hypothesis: Retrograde Menstruation (Sampson's theory) with coelomic metaplasia (Meyer) and lymphatic dissemination (Halban). Commonest sites: Ovaries (most common) > Pouch of Douglas > Uterosacral ligaments > Rectovaginal septum. Clinical Presentation: 'Classic 4 D's': Dysmenorrhea (secondary, congestive) + Dyspareunia (deep) + Dyschezia (painful defecation) + Dysuria + Infertility (30-50%). Ovarian Endometrioma ('Chocolate Cyst'): Formed by recurrent bleeding; contains thick tarry hemolyzed chocolate-brown fluid. Ultrasound appearance: Homogeneous low-level internal echoes ('GROUND-GLASS APPEARANCE'). GOLD STANDARD FOR DEFINITIVE DIAGNOSIS: DIAGNOSTIC LAPAROSCOPY with histopathologic biopsy. Classic laparoscopic lesions: 'Powder-burn' or 'gunshot' bluish-black lesions, flame-red active implants, white scarring, and adhesions.",
        "citation": "Novak's Gynecology, 16th Ed, Chapter 19 (Endometriosis), p. 505-528; Williams Gynecology, 4th Ed.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- RADIODIAGNOSIS (6 Questions) ---
    # =========================================================================
    {
        "subject": "Radiodiagnosis",
        "concept_name": "Emergency Neuroimaging: Non-Contrast CT vs MRI in Acute Stroke",
        "stem": (
            "A 66-year-old male presents to the stroke emergency room exactly 90 minutes after the sudden onset of right-sided hemiplegia "
            "and expressive aphasia. Blood glucose is 128 mg/dL and BP is 164/92 mmHg. "
            "What is the MANDATORY FIRST-LINE imaging modality that must be performed immediately, and what is its primary clinical objective?"
        ),
        "options": [
            ("Non-Contrast Computed Tomography (NCCT) head; Primary objective is to rule out intracranial hemorrhage to determine eligibility for IV thrombolysis", True, None),
            ("Diffusion-Weighted Magnetic Resonance Imaging (DWI-MRI); Primary objective is to measure ischemic core volume", False, "While DWI-MRI is sensitive for ischemia, emergency NCCT is the rapid standard-of-care first step to rule out hemorrhage before rtPA."),
            ("Digital Subtraction Angiography (DSA); Primary objective is to identify basilar artery thrombosis", False, "DSA is an invasive catheter procedure performed only during endovascular thrombectomy, never as the initial diagnostic screening."),
            ("Carotid and vertebral Doppler ultrasonography; Primary objective is to grade extracranial stenosis", False, "Carotid ultrasound does not image brain parenchyma or exclude hemorrhagic stroke.")
        ],
        "pearl": "Acute Ischemic Stroke Imaging Protocol: Mandatory first step: Non-Contrast Head CT (NCCT). Core objective: EXCLUDE INTRACRANIAL HEMORRHAGE (absolute contraindication to IV recombinant tissue plasminogen activator [rtPA / Alteplase / Tenecteplase]). Window period for IV thrombolysis: Up to 4.5 hours from symptom onset. EARLY ISCHEMIC CT SIGNS (within 3-6 hours): 1. Hyperdense MCA sign (acute thrombus in M1 segment) | 2. Loss of insular ribbon (loss of gray-white differentiation at insular cortex) | 3. Obscuration / blurring of lentiform nucleus | 4. Sulcal effacement. GOLD STANDARD FOR HYPERACUTE ISCHEMIC INFARCTION: MRI with Diffusion-Weighted Imaging (DWI) + Apparent Diffusion Coefficient (ADC) map: Intracellular cytotoxic edema restricts Brownian motion of water molecules &rarr; RESTRICTED DIFFUSION appears hyperintense (BRIGHT) on DWI and hypointense (DARK) on ADC within minutes of ischemia!",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 54 (Stroke); Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Radiodiagnosis",
        "concept_name": "Trauma Imaging: Focused Assessment with Sonography for Trauma (FAST & eFAST)",
        "stem": (
            "A 24-year-old motorcyclist is brought to the trauma bay after a high-speed collision. He is pale, diaphoretic, and hypotensive "
            "(BP 82/46 mmHg, pulse 136 bpm). The trauma surgeon immediately performs an extended Focused Assessment with Sonography for Trauma (eFAST). "
            "In a supine trauma patient, which anatomical window represents the MOST SENSITIVE dependent space in the peritoneal cavity for detecting free hemoperitoneum?"
        ),
        "options": [
            ("Hepatorenal Recess (Morison's Pouch) in the right upper quadrant", True, None),
            ("Splenorenal space in the left upper quadrant", False, "The splenorenal recess is less dependent and accumulates fluid later than Morison's pouch in the supine position."),
            ("Subxiphoid pericardial window", False, "The subxiphoid view evaluates cardiac tamponade in the pericardial sac, not peritoneal hemoperitoneum."),
            ("Right paracolic gutter at the cecal pole", False, "Morison's pouch is more anatomically dependent than the paracolic gutters in a supine patient.")
        ],
        "pearl": "FAST and eFAST Examination in Trauma: FAST scans 4 primary acoustic windows: 1. Hepatorenal recess (MORISON'S POUCH, RUQ): The MOST DEPENDENT space in the peritoneal cavity in a supine patient! Fluid collects between liver and right kidney. 2. Splenorenal recess (LUQ): Between spleen and left kidney. 3. Pelvic / Suprapubic window (Pouch of Douglas in females, Rectovesical pouch in males): Evaluates retrovesical fluid. 4. Subxiphoid / Pericardial window: Evaluates hemopericardium / cardiac tamponade. EXTENDED FAST (eFAST) adds bilateral anterior thoracic scans to evaluate for PNEUMOTHORAX: Normal lung: Lung sliding sign on 2D ('ants marching') and 'Seashore sign' on M-mode. Pneumothorax: ABSENCE of lung sliding and 'Stratosphere / Barcode sign' on M-mode, plus the presence of a 'Lung point' (pathognomonic transition zone between normal sliding and stationary pleura).",
        "citation": "ATLS Student Manual, 10th Ed, Chapter 3 (Abdominal Trauma); Grainger & Allison's Diagnostic Radiology, 7th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Radiodiagnosis",
        "concept_name": "Gastrointestinal Radiology: Bowel Obstruction & Pneumoperitoneum Signs",
        "stem": (
            "A 72-year-old bedridden nursing home resident presents with massive abdominal distension, obstipation, and tympanitic percussion. "
            "Erect plain abdominal radiography demonstrates an enormous, dilated, inverted U-shaped loop of bowel without haustra arising "
            "from the pelvis and extending toward the right upper quadrant, giving the classic appearance of a 'Coffee-Bean Sign'. "
            "There are two air-fluid levels visible within the limbs of the loop. "
            "What is the diagnosis and the underlying anatomical predisposition?"
        ),
        "options": [
            ("Sigmoid Volvulus; Redundant sigmoid loop on a long, narrow mesocolon twisting around its mesenteric axis", True, None),
            ("Cecal Volvulus; Hypermobile cecum rotating toward the left upper quadrant", False, "Cecal volvulus classically appears as a kidney-bean or comma-shaped loop pointing to the LEFT upper quadrant."),
            ("Toxic Megacolon; Fulminant mucosal inflammation with transverse colon diameter >6 cm", False, "Toxic megacolon shows a dilated transverse colon with loss of haustra and mucosal thumbprinting, not a coffee-bean loop."),
            ("Pneumoperitoneum with Rigler's sign; Perforation of anterior duodenal ulcer", False, "Rigler's sign is visualization of both outer and inner bowel walls, not an inverted U-loop.")
        ],
        "pearl": "Volvulus & Abdominal Radiography Classics: 1. SIGMOID VOLVULUS (Most common, ~75% of colonic volvulus): Predisposition: Elderly, institutionalized, chronic constipation, high-fiber diet, Chagas disease. Anatomy: Long redundant sigmoid colon with a narrow mesenteric base twists around its axis. X-ray signs: 'COFFEE-BEAN SIGN' / 'Bent Inner-Tube Sign' / 'Frimann-Dahl sign' (three dense lines converging toward pelvis). Apex points toward RIGHT UPPER QUADRANT. Initial management: Endoscopic detorsion with rigid sigmoidoscopy and flatus tube placement (if no ischemia/gangrene). 2. CECAL VOLVULUS (~20-25%): Hypermobile cecum due to incomplete embryologic retroperitoneal fixation. Apex points toward LEFT UPPER QUADRANT ('Kidney-bean' or 'embryo' shape). 3. RIGLER'S SIGN (Double-wall sign): Air on BOTH the luminal and peritoneal surfaces of bowel wall, diagnostic of PNEUMOPERITONEUM.",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 30 (Large Bowel); Bailey & Love's Short Practice of Surgery, 28th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Radiodiagnosis",
        "concept_name": "Chest Radiograph & HRCT Signs: TB, Bronchiolitis & Crazy-Paving",
        "stem": (
            "A 38-year-old male with active cough, low-grade evening pyrexia, and weight loss undergoes High-Resolution Computed Tomography (HRCT) "
            "of the thorax. The scan demonstrates 2-4 mm well-defined centrilobular nodular opacities with branching linear structures resembling "
            "a budding twig throughout the right upper and middle lobes ('Tree-in-Bud' pattern). "
            "What histopathological process does this characteristic radiological sign signify?"
        ),
        "options": [
            ("Impaction of mucus, pus, or caseous cellular debris within dilated branching terminal and respiratory bronchioles (endobronchial spread of infection)", True, None),
            ("Diffuse lymphangitic carcinomatosis filling pulmonary lymphatic channels and interlobular septa", False, "Lymphangitic carcinomatosis causes smooth or nodular interlobular septal thickening, not centrilobular tree-in-bud impaction."),
            ("Alveolar filling by periodic acid-Schiff (PAS) positive surfactant phospholipids", False, "Surfactant filling causes the 'Crazy-Paving' pattern seen in Pulmonary Alveolar Proteinosis (PAP)."),
            ("Aneurysmal dilation of bronchial arteries surrounding a tuberculous cavity (Rasmussen aneurysm)", False, "Rasmussen aneurysm is a vascular dilation inside a cavity wall that causes massive hemoptysis, not tree-in-bud.")
        ],
        "pearl": "Classic HRCT Chest Patterns: 1. TREE-IN-BUD APPEARANCE: Anatomy: Centrilobular branching linear structures with terminal nodules. Pathophysiology: Small airway obstruction caused by mucus, pus, or granulomatous debris filling and dilating respiratory bronchioles and alveolar ducts. Etiology: ACTIVE ENDOBRONCHIAL SPREAD OF TUBERCULOSIS (most common), non-tuberculous mycobacteria (MAC), bacterial aspiration bronchiolitis, and cystic fibrosis. 2. CRAZY-PAVING PATTERN: Ground-glass attenuation with superimposed thickened interlobular septa and intralobular reticular lines. Etiology: Pulmonary Alveolar Proteinosis (PAP, classic PAS-positive surfactant accumulation), Pneumocystis jirovecii pneumonia, Lipoid pneumonia, ARDS, and COVID-19. 3. SIGNET-RING SIGN: Dilated bronchus larger than its adjacent pulmonary artery branch, diagnostic of BRONCHIECTASIS.",
        "citation": "Webb's High-Resolution CT of the Lung, 5th Ed; Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 15.",
        "difficulty": "medium"
    },
    {
        "subject": "Radiodiagnosis",
        "concept_name": "Intracranial Hemorrhages: Epidural vs Subdural vs Subarachnoid",
        "stem": (
            "A 21-year-old college student is hit on the right side of the head with a cricket bat at the pterion. He is initially knocked "
            "unconscious for 2 minutes, but quickly awakens, feels well, and walks off the field ('Lucid Interval'). Three hours later, he becomes "
            "drowsy, develops a severe headache, vomits, and lapses into a coma with an ipsilateral dilated, non-reactive pupil and contralateral hemiparesis. "
            "Emergency non-contrast CT of the brain demonstrates a biconvex (lentiform), hyperdense extra-axial collection along the right temporoparietal convexities that DOES NOT CROSS CRANIAL SUTURES. "
            "What vessel has ruptured to cause this intracranial hematoma?"
        ),
        "options": [
            ("Middle Meningeal Artery", True, None),
            ("Bridging cortical veins crossing into the superior sagittal sinus", False, "Bridging vein rupture causes Subdural Hematoma (SDH), which forms a crescentic collection that crosses cranial sutures."),
            ("Ruptured saccular (berry) aneurysm of the Anterior Communicating Artery", False, "Berry aneurysm rupture causes Subarachnoid Hemorrhage (SAH) with blood filling basal cisterns and sulci."),
            ("Striatocapsular Charcot-Bouchard microaneurysms", False, "Charcot-Bouchard aneurysms cause hypertensive intraparenchymal basal ganglia / putaminal hemorrhages.")
        ],
        "pearl": "Intracranial Hemorrhages Comparison: 1. EPIDURAL HEMATOMA (EDH): Vessel: Middle Meningeal Artery (branch of maxillary artery) torn at the PTERION (where frontal, parietal, temporal, and sphenoid bones meet). Anatomy: Blood collects between inner table of skull and periosteal dura mater. CT Appearance: BICONVEX / LENTICULAR hyperdensity. DOES NOT CROSS SUTURE LINES (dura is firmly adherent to sutures!), but can cross dural attachments (falx/tentorium). Clinical hallmark: Classic LUCID INTERVAL (temporary recovery before rapid deterioration and uncal herniation). 2. SUBDURAL HEMATOMA (SDH): Vessel: BRIDGING CORTICAL VEINS. Anatomy: Between dura and arachnoid. CT Appearance: CRESCENTIC / CONCAVE hyperdensity. CAN CROSS SUTURE LINES, but restricted by dural reflections (falx cerebri). Prevalent in elderly / alcoholics with cerebral atrophy. 3. SUBARACHNOID HEMORRHAGE (SAH): Vessel: Rupture of berry aneurysm (A-Comm > P-Comm > MCA). 'Worst headache of life' (thunderclap), blood fills basal cisterns and Sylvian fissures.",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 53 (CNS Trauma); Greenberg's Handbook of Neurosurgery, 9th Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Radiodiagnosis",
        "concept_name": "Contrast Media & ALARA Principle: Radiation Safety & Contrast Nephropathy",
        "stem": (
            "A 68-year-old diabetic male with chronic kidney disease (baseline serum creatinine 2.4 mg/dL, estimated GFR 28 mL/min/1.73m²) "
            "requires a contrast-enhanced CT scan for suspected mesenteric ischemia. "
            "Which of the following is the single most effective, guideline-recommended preventive measure to reduce the risk of Contrast-Induced Nephropathy (CIN)?"
        ),
        "options": [
            ("Intravenous volume expansion with isotonic (0.9%) sodium chloride solution before and after contrast administration", True, None),
            ("Routine intravenous administration of high-dose N-Acetylcysteine without intravenous fluids", False, "High-dose NAC without hydration failed to demonstrate benefit in large randomized trials (PRESERVE trial)."),
            ("Intravenous Furosemide diuresis immediately following contrast injection", False, "Forced diuresis with furosemide causes intravascular volume depletion and significantly increases CIN risk."),
            ("Prophylactic hemodialysis initiated within 2 hours of contrast exposure", False, "Prophylactic hemodialysis is invasive, does not prevent nephropathy, and is not recommended by KDIGO/ACR guidelines.")
        ],
        "pearl": "Contrast-Induced Acute Kidney Injury (CI-AKI / CIN): Definition: Relative increase in serum creatinine &ge;25% or absolute increase &ge;0.5 mg/dL (44 mcmol/L) from baseline within 48-72 hours after intravascular iodinated contrast administration, in the absence of an alternative etiology. Risk factors: Pre-existing CKD (eGFR <30 mL/min), Diabetic nephropathy, Dehydration, Congestive heart failure, and high contrast volume. GUIDELINE PREVENTIVE PILLARS: 1. IV Hydration with isotonic crystalloids (0.9% NaCl @ 1-1.5 mL/kg/hr for 3-12 hrs before and 6-12 hrs after contrast): The ONLY consistently proven prophylaxis! 2. Minimize contrast volume & use Iso-osmolar (Iodixanol) or Low-osmolar (Iohexol) agents. 3. Withhold Metformin for 48 hours post-procedure in patients with eGFR <60 to prevent fatal lactic acidosis. (Note: N-Acetylcysteine [PRESERVE trial] and bicarbonate do not show superior benefit over standard normal saline).",
        "citation": "American College of Radiology (ACR) Manual on Contrast Media, 2023; KDIGO Clinical Practice Guideline for AKI.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- DERMATOLOGY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Dermatology",
        "concept_name": "Papulosquamous Disorders: Psoriasis Vulgaris vs Lichen Planus",
        "stem": (
            "A 32-year-old male presents with well-demarcated, erythematous plaques covered by thick, silvery-white micaceous scales over both "
            "knees, elbows, and lumbosacral region. On gentle mechanical scraping of the scales, there is a candle-grease appearance, "
            "followed by detachment of a thin, translucent membrane (Burkley's membrane), which immediately reveals multiple pinpoint bleeding spots. "
            "What is this diagnostic clinical phenomenon, and what histopathological change directly produces the bleeding?"
        ),
        "options": [
            ("Auspitz Sign; Thinning of the suprapapillary epidermis with tortuous, dilated dermal capillary loops extending high into the dermal papillae", True, None),
            ("Koebner Phenomenon; Rupture of subepidermal intra-articular microaneurysms", False, "Koebner is the appearance of new lesions at sites of mechanical trauma, not pinpoint bleeding on scraping."),
            ("Nikolsky Sign; Intraepidermal acantholysis with detachment of suprabasal keratinocytes", False, "Nikolsky sign is lateral friction epidermal detachment seen in Pemphigus and SJS/TEN."),
            ("Wickham Striae; Dense band-like lymphocytic infiltrate flattening rete ridges", False, "Wickham striae are white reticular lines on surface of Lichen Planus papules due to focal hypergranulosis.")
        ],
        "pearl": "Psoriasis Vulgaris Clinical Signs: 1. Candle-grease sign: Grattage test yields shiny silvery flakes like scraped candle grease. 2. Burkley's membrane: A thin moist translucent membrane exposed after removing all scales. 3. AUSPITZ SIGN: Peeling Burkley's membrane tears the fragile dilated tortuous capillaries situated high in the elongated dermal papillae (due to suprapapillary epidermal thinning), causing PINPOINT BLEEDING. 4. KOEBNER'S PHENOMENON (Isomorphic response): Development of characteristic psoriatic plaques along lines of physical trauma/scratching (also seen in Lichen Planus, Vitiligo, Warts). HISTOPATHOLOGY OF PSORIASIS: Regular elongation of rete ridges ('test-tubes in a rack'), Hyperkeratosis with PARAKERATOSIS (retained nuclei in stratum corneum), Absent stratum granulosum, MUNRO'S MICROABSCESSES (neutrophils in stratum corneum) & Spongiform Pustules of Kogoj (neutrophils in stratum spinosum).",
        "citation": "Roxburgh's Common Skin Diseases, 18th Ed, Chapter 6; Fitzpatrick's Dermatology in General Medicine, 9th Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Dermatology",
        "concept_name": "Immunobullous Diseases: Pemphigus Vulgaris vs Bullous Pemphigoid",
        "stem": (
            "A 46-year-old female presents with multiple painful oral erosions that preceded the appearance of widespread, flaccid, easily "
            "ruptured blisters on normal-appearing and erythematous skin of her trunk and scalp. When lateral shearing pressure is applied to "
            "perilesional normal skin, the epidermis slides off easily (positive Nikolsky sign). Tzanck smear from the base of a freshly unroofed "
            "bulla demonstrates rounded, detached keratinocytes with hyperchromatic nuclei and a perinuclear halo (Acantholytic / Tzanck cells). "
            "Direct immunofluorescence (DIF) of perilesional skin will demonstrate which characteristic antibody deposition pattern?"
        ),
        "options": [
            ("Intercellular 'fishnet' or 'chicken-wire' pattern of IgG and C3 throughout the epidermal spinous layer targeting Desmoglein-3", True, None),
            ("Linear continuous band of IgG and C3 along the dermoepidermal basement membrane zone targeting BP180", False, "Linear BMZ deposition of IgG/C3 is diagnostic of Bullous Pemphigoid, which features tense blisters with negative Nikolsky sign."),
            ("Granular deposition of IgA clumps concentrated exclusively in dermal papillae tips", False, "Granular IgA at dermal papillae tips is pathognomonic for Dermatitis Herpetiformis (associated with celiac disease)."),
            ("Subepidermal IgG deposition along the type VII collagen anchoring fibrils", False, "Type VII collagen antibodies are found in Epidermolysis Bullosa Acquisita (EBA).")
        ],
        "pearl": "Pemphigus Vulgaris vs Bullous Pemphigoid Master Table: 1. PEMPHIGUS VULGARIS: Autoantibodies: IgG against DESMOGLEIN-3 (mucosa) & DESMOGLEIN-1 (skin) in desmosomes. Blister level: SUPRABASAL INTRAEPIDERMAL acantholysis with 'Row of tombstones' basal layer. Blister type: FLACCID, fragile bullae that rupture into painful raw weeping denuded erosions. Mucosal involvement: In &ge;70-90% (oral erosions often precede skin lesions by months!). Nikolsky Sign: POSITIVE (also positive Asboe-Hansen / bulla-spread sign). Tzanck smear: ACANTHOLYTIC TZANCK CELLS. DIF: INTERCELLULAR 'FISHNET' / 'CHICKEN-WIRE' IgG and C3 in epidermis. 2. BULLOUS PEMPHIGOID: Autoantibodies: IgG against BP180 (type XVII collagen) & BP230 in hemidesmosomes. Blister level: SUBEPIDERMAL. Blister type: TENSE, firm, durable bullae on urticarial base. Mucosal: Rare (<10-20%). Nikolsky Sign: NEGATIVE. DIF: Continuous LINEAR BAND of IgG & C3 along Basement Membrane Zone (BMZ).",
        "citation": "Fitzpatrick's Dermatology in General Medicine, 9th Ed, Chapter 54; IADVL Textbook of Dermatology, 5th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Dermatology",
        "concept_name": "Infectious Dermatology: Leprosy (Hansen's Disease) Spectrum & Reactions",
        "stem": (
            "A 35-year-old male presents with multiple bilateral, symmetrical, poorly defined, shiny, hypopigmented to erythematous macules "
            "and infiltrative nodules on his face, earlobes, and extensor extremities. On examination, there is marked thickening and corrugation "
            "of the facial skin with flattening of the nose giving a 'Leonine Facies', alongside loss of the lateral third of the eyebrows (madarosis). "
            "Sensory loss is patchy and late in onset. Slit-skin smear from the earlobe stained with modified Ziehl-Neelsen (Wade-Fite 5% H2SO4) "
            "reveals sheets and clumps of acid-fast bacilli packed tightly within lipid-laden foamy histiocytes ('globi'). "
            "Where does this patient lie on the Ridley-Jopling classification, and what is the status of his cell-mediated immunity (CMI) and Lepromin skin test?"
        ),
        "options": [
            ("Lepromatous Leprosy (LL); Severely deficient / absent cell-mediated immunity against M. leprae, resulting in a negative Lepromin test (anergy)", True, None),
            ("Tuberculoid Leprosy (TT); Vigorous high cell-mediated immunity with strongly positive Lepromin test", False, "Tuberculoid leprosy presents with 1-2 anesthetic, well-demarcated plaques, nerve thickening, zero bacilli (paucibacillary), and positive Lepromin test."),
            ("Borderline Tuberculoid (BT); Moderate cell-mediated immunity with satellite lesions and positive Mitsuda test", False, "Borderline tuberculoid has asymmetric hypopigmented anesthetic plaques with satellite lesions, not bilateral leonine facies with globi."),
            ("Histoid Leprosy; Hyper-reactive CMI with keloidal nodules arising on tuberculoid background", False, "Histoid leprosy arises in LL or BL patients undergoing irregular dapsone monotherapy, characterized by spindle-shaped histiocytes.")
        ],
        "pearl": "Ridley-Jopling Spectrum of Leprosy (Mycobacterium leprae): 1. TUBERCULOID (TT): CMI: High & vigorous. Lesions: Solitary or few (&le;3) hypopigmented, well-defined, completely ANESTHETIC plaques with raised borders. Peripheral nerve: Early marked asymmetrical thickening (great auricular, ulnar). Slit-skin smear: ZERO bacilli (Bacterial Index 0, Paucibacillary). Lepromin test: STRONGLY POSITIVE (indicates competent delayed hypersensitivity). 2. LEPROMATOUS (LL): CMI: Completely ANERGIC / ABSENT. Lesions: Innumerable bilateral, symmetrical, poorly defined macules, papules, infiltrated nodules. Features: LEONINE FACIES, madarosis (loss of eyebrows), collapsed saddle nose. Slit-skin smear: BACTERIOLOGICALLY POSITIVE (BI 4-6+, GLOBI inside VIRCHOW FOAM CELLS). Lepromin test: NEGATIVE. WHO MULTIDRUG THERAPY (MDT) for Multibacillary (&ge;6 lesions / smear positive): Rifampicin 600 mg once monthly (supervised) + Clofazimine 300 mg once monthly (supervised) & 50 mg daily (unsupervised) + Dapsone 100 mg daily for 12 months.",
        "citation": "IADVL Textbook of Dermatology, 5th Ed, Chapter 24 (Leprosy); Park's Textbook of Preventive and Social Medicine, 26th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Dermatology",
        "concept_name": "Sexually Transmitted Infections: Genital Ulcer Disease Algorithms",
        "stem": (
            "A 27-year-old sexually active male presents with a solitary, painless genital sore on the coronal sulcus of the penis that "
            "appeared 3 weeks after an unprotected sexual encounter. Examination reveals a well-circumscribed, indurated, clean-based ulcer "
            "with elevated, rolled margins ('button-like' consistency on palpation) and no purulent exudate. Bilateral painless, discrete, "
            "non-tender, rubbery inguinal lymph nodes ('buboes' without suppuration) are palpated. "
            "Dark-field microscopy of serous exudate reveals corkscrew-shaped spirochetes with regular tight spirals demonstrating active flexing and rotational motility. "
            "What is the diagnosis and the CDC/WHO treatment of choice?"
        ),
        "options": [
            ("Primary Syphilis (Hard Chancre); Benzathine Penicillin G 2.4 million units IM as a single dose", True, None),
            ("Chancroid (Haemophilus ducreyi); Azithromycin 1 g orally single dose", False, "Chancroid produces multiple, extremely PAINFUL, soft, non-indurated ulcers with a ragged, undermined border and purulent base."),
            ("Genital Herpes (HSV-2); Valacyclovir 1000 mg twice daily for 10 days", False, "Herpes genitalis presents with multiple grouped, excruciatingly painful vesicles on an erythematous base that erode into shallow ulcers."),
            ("Lymphogranuloma Venereum (Chlamydia trachomatis L1-L3); Doxycycline 100 mg twice daily for 21 days", False, "LGV presents with a transient, tiny painless papule followed by painful suppurative matted inguinal adenopathy with Groove sign.")
        ],
        "pearl": "Genital Ulcer Disease Differential Diagnosis: 1. PRIMARY SYPHILIS (Hard Chancre / Ulcus durum): Organism: Treponema pallidum. Incubation: 9-90 days (avg 21 days). Lesion: CLASSICALLY SINGLE, PAINLESS, indurated ('button-like' cartilaginous hardness), clean base, non-purulent. Inguinal nodes: Bilateral, painless, non-tender, non-suppurative, rubbery. Dark-field: Corkscrew spirochetes. Serology: VDRL/RPR becomes positive 1-3 weeks after chancre appears (FTA-ABS is positive earlier). TREATMENT OF CHOICE: Benzathine Penicillin G 2.4 million units IM single dose! (If penicillin-allergic: Doxycycline 100 mg BID for 14 days). 2. CHANCROID (Soft Chancre): Haemophilus ducreyi. MULTIPLE, EXTREMELY PAINFUL, soft, non-indurated, dirty purulent necrotic base with undermined ragged edges. Suppurative, tender unilateral bubo. Gram stain: 'School of fish' appearance.",
        "citation": "CDC STI Treatment Guidelines 2021; Fitzpatrick's Dermatology, 9th Ed, Chapter 173.",
        "difficulty": "easy"
    },
    {
        "subject": "Dermatology",
        "concept_name": "Severe Cutaneous Adverse Reactions: SJS vs TEN & SCORTEN",
        "stem": (
            "A 42-year-old male with newly diagnosed epilepsy was started on Carbamazepine 3 weeks ago. He presents to the ICU with high fever, "
            "painful stinging red eyes, difficulty swallowing, and a rapidly spreading morbilliform eruption with atypical dusky purpuric targets. "
            "Over 48 hours, extensive sheet-like flaccid epidermal detachment occurs, leaving raw, denuded dermis resembling a second-degree scalding burn. "
            "Two distinct mucosal surfaces (lips/oral cavity with hemorrhagic crusting and severe conjunctival sloughing) are severely ulcerated. "
            "Total detached and detachable body surface area (BSA) is calculated at 38%. "
            "What is the diagnosis, and which prognostic scoring scale is validated to predict in-hospital mortality?"
        ),
        "options": [
            ("Toxic Epidermal Necrolysis (TEN); SCORTEN prognostic score calculated within the first 24-48 hours", True, None),
            ("Stevens-Johnson Syndrome (SJS); APACHE II score", False, "BSA detachment >30% classifies as TEN. SJS is limited to <10% BSA detachment; SCORTEN is the validated prognostic tool."),
            ("Staphylococcal Scalded Skin Syndrome (SSSS); Wallace Rule of Nines", False, "SSSS is mediated by Exfoliatin A/B in young children, cleaves high at stratum granulosum, spares mucous membranes."),
            ("Erythema Multiforme Major; Wells score", False, "Erythema multiforme features classic acral target lesions with minimal (<1%) epidermal detachment.")
        ],
        "pearl": "Severe Cutaneous Adverse Reactions (SCAR) - SJS vs TEN Spectrum: Pathogenesis: CD8+ T-cell / NK-cell mediated apoptosis of keratinocytes via Granulysin, Fas/Fas-ligand, and Perforin-Granzyme B. Common culprit drugs: Allopurinol, Carbamazepine, Phenytoin, Lamotrigine, Cotrimoxazole, NSAIDs, Nevirapine. BSA DETACHMENT CLASSIFICATION: 1. Stevens-Johnson Syndrome (SJS): <10% total Body Surface Area (BSA) detachment | 2. SJS/TEN Overlap: 10% to 30% BSA detachment | 3. Toxic Epidermal Necrolysis (TEN): >30% BSA detachment! (Mortality >30-50%). SCORTEN PROGNOSTIC SCORE (7 Independent Risk Factors, 1 point each, measured in first 24h): 1. Age &ge;40 years | 2. Heart rate &ge;120 bpm | 3. Presence of malignancy | 4. BSA detached &ge;10% on day 1 | 5. Serum urea >28 mg/dL (>10 mmol/L) | 6. Serum bicarbonate <20 mmol/L | 7. Serum glucose >252 mg/dL (>14 mmol/L). (Score 0-1: mortality <4%; Score &ge;5: mortality >90%).",
        "citation": "Fitzpatrick's Dermatology in General Medicine, 9th Ed, Chapter 43; Bastuji-Garin S et al., SCORTEN, J Invest Dermatol.",
        "difficulty": "hard"
    },
    {
        "subject": "Dermatology",
        "concept_name": "Parasitic Infestations: Scabies Diagnosis, Dermoscopy & Eradication",
        "stem": (
            "A 19-year-old medical student living in a college hostel complains of intense, agonizing generalized itching that worsens "
            "dramatically at night, preventing sleep. His roommate has developed similar symptoms. "
            "Examination reveals discrete excoriated papules, vesicles, and thin, thread-like grayish, wavy serpiginous tracks (burrows) "
            "concentrated in the interdigital web spaces of the fingers, flexor aspect of the wrists, anterior axillary folds, periumbilical area, "
            "and on the shaft and glans of the penis (nodular lesions). "
            "Handheld dermoscopy of a burrow reveals the pathognomonic 'Delta-Wing Jet / Hang-Glider Sign'. "
            "What is the first-line topical treatment and essential application protocol?"
        ),
        "options": [
            ("Permethrin 5% cream applied thoroughly from the neck down to the soles of the feet, left on for 8-14 hours, repeated after 7 days; treat all household/hostel room contacts simultaneously", True, None),
            ("Topical Clobetasol propionate 0.05% ointment applied to itchy areas twice daily", False, "Topical corticosteroids suppress local immunity, exacerbating mite proliferation and converting into Crusted (Norwegian) Scabies."),
            ("Single application of topical Benzyl Benzoate 25% to burrows only for 1 hour", False, "Treatment must be applied neck-to-toe over the whole body, not just to visible burrows, to prevent re-infestation."),
            ("Topical Clotrimazole 1% cream combined with oral cetirizine for 14 days", False, "Clotrimazole is an antifungal and has zero acaricidal activity against Sarcoptes scabiei.")
        ],
        "pearl": "Scabies (Sarcoptes scabiei var. hominis): Transmission: Direct prolonged skin-to-skin contact (hostels, prisons, nursing homes). Cardinal feature: Severe INTRACTABLE NOCTURNAL PRURITUS (Type IV delayed hypersensitivity to mite feces / scybala). Pathognomonic lesion: BURROW (stratum corneum channel excavated by the adult female mite). Sites of predilection (Circle of Hebra): Interdigital webs, flexor wrists, elbows, axillary folds, waistline, buttocks, genitalia (nodular scabies on penis/scrotum is pathognomonic!). Note: Face and scalp are spared in adults, but INVOLVED IN INFANTS. Dermoscopy sign: 'DELTA-WING JET' / 'HANG-GLIDER' sign (dark triangular anterior body/mouthparts of mite at the end of burrow track). TREATMENT OF CHOICE: PERMETHRIN 5% DERMAL CREAM. Application: Apply neck down to soles (including under fingernails!), leave overnight for 8-14 hours, wash off. MUST REPEAT AFTER 7 DAYS (Permethrin kills mites but not all eggs; second dose kills newly hatched nymphs). MANDATORY RULE: Treat all cohabiting contacts simultaneously!",
        "citation": "Roxburgh's Common Skin Diseases, 18th Ed, Chapter 4; CDC Parasites - Scabies Guidelines.",
        "difficulty": "easy"
    }
]
