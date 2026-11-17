"""
Authentic High-Yield NEET-PG Clinical Questions for Obstetrics & Gynecology
References: DC Dutta's Textbook of Obstetrics (9th Ed), DC Dutta's Textbook of Gynecology (8th Ed)
"""

OBGYN_QUESTIONS = [
    {
        "concept_name": "Core Principles: Preeclampsia & Eclampsia Management (Magnesium Sulfate)",
        "stem": (
            "A 24-year-old primigravida at 34 weeks of gestation presents to the labor casualty with sudden-onset severe throbbing frontal headache, "
            "blurring of vision, and epigastric pain. Her blood pressure is 174/112 mmHg on two measurements taken 15 minutes apart. "
            "Urine dipstick shows 3+ proteinuria. Deep tendon reflexes are brisk (4+ patellar reflex with sustained clonus). "
            "While being transferred to the labor room, she develops generalized tonic-clonic convulsions. "
            "What is the immediate anticonvulsant drug of choice to terminate the seizure and prevent recurrences, and what is the standard loading regimen?"
        ),
        "options": [
            ("Intravenous Diazepam 10 mg slow bolus followed by oral Phenytoin", False, "Collaborative Eclampsia Trial proved Magnesium Sulfate is vastly superior to Diazepam and Phenytoin with significantly lower maternal/fetal mortality."),
            ("Magnesium Sulfate (Pritchard regimen: 4 g IV over 5-10 min + 10 g deep IM, 5 g in each buttock)", True, None),
            ("Intravenous Sodium Valproate 1000 mg infusion", False, "Valproate is not indicated for eclamptic convulsions and is highly teratogenic."),
            ("Intravenous Propofol 2 mg/kg with rapid endotracheal intubation", False, "Propofol is used for general anesthesia, not standard bedside anticonvulsant therapy for eclampsia.")
        ],
        "pearl": "Eclampsia Management: Anticonvulsant of Choice: MAGNESIUM SULFATE (MgSO4). Pritchard Regimen: Loading: 4 g IV (20% solution) over 5-10 min PLUS 10 g deep IM (50% solution, 5 g in each buttock with 1 mL 2% lidocaine). Maintenance: 5 g IM every 4 hours in alternate buttocks (or Zuspan IV regimen: 1-2 g/hour IV infusion). Continue for 24 hours after delivery or 24 hours after last seizure (whichever is later).",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 17 (Hypertensive Disorders in Pregnancy), p. 218-232.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Preeclampsia & Eclampsia Management (Magnesium Sulfate)",
        "stem": (
            "A woman with severe preeclampsia is receiving maintenance Magnesium Sulfate therapy. Before administering the next scheduled 4-hourly dose, "
            "the resident physician performs mandatory clinical bedside monitoring. Which of the following findings indicates the EARLIEST sign of Magnesium toxicity "
            "requiring immediate discontinuation of MgSO4 and administration of the specific antidote?"
        ),
        "options": [
            ("Loss of Patellar (Knee-Jerk) Deep Tendon Reflex (serum Mg 8-10 mEq/L)", True, None),
            ("Respiratory arrest with bradypnea <12 breaths/min (serum Mg 12-15 mEq/L)", False, "Respiratory depression is a LATER sign of magnesium toxicity occurring after loss of deep tendon reflexes."),
            ("Cardiac arrest in asystole (serum Mg >25 mEq/L)", False, "Cardiac arrest is the terminal manifestation of magnesium toxicity (>25-30 mEq/L)."),
            ("Transient facial flushing and sensation of warmth", False, "Facial flushing and warmth are common physiologic side effects of peripheral vasodilation, not dangerous toxicity.")
        ],
        "pearl": "Magnesium Sulfate Toxicity Progression: Therapeutic range: 4-7 mEq/L (or 4.8-8.4 mg/dL). 1. LOSS OF PATELLAR REFLEX (Knee jerk): 8-10 mEq/L (EARLIEST SIGN). 2. Respiratory depression (<12/min): 12-15 mEq/L. 3. Cardiac arrest: >25-30 mEq/L. 3 Golden Clinical Checks before every dose: 1. Patellar reflex present | 2. Respiratory rate ≥12/min | 3. Urine output ≥30 mL/hr (100 mL/4 hrs). SPECIFIC ANTIDOTE: 10 mL of 10% Calcium Gluconate IV slow push over 10 minutes.",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 17, p. 228-230.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Postpartum Hemorrhage (PPH) Management Protocol",
        "stem": (
            "A 28-year-old grand multipara delivers a 4.1 kg infant via uneventful normal vaginal delivery. "
            "Ten minutes following delivery of the placenta by controlled cord traction, torrential vaginal bleeding occurs, "
            "with blood loss rapidly exceeding 900 mL. On abdominal palpation, the uterus is soft, flabby, boggy, and distended up to the xiphisternum. "
            "Bimanual uterine compression and oxytocin infusion (20 IU in 500 mL normal saline) are initiated. "
            "The patient's blood pressure is 150/98 mmHg. Which of the following uterotonic agents is STRICTLY CONTRAINDICATED in this hypertensive patient?"
        ),
        "options": [
            ("Methylergonovine (Methergine 0.2 mg IM)", True, None),
            ("15-methyl Prostaglandin F2-alpha (Carboprost 250 mcg IM)", False, "Carboprost is safe in hypertension, but strictly contraindicated in BRONCHIAL ASTHMA."),
            ("Misoprostol (800 mcg sublingual or per-rectal)", False, "Misoprostol is a PGE1 analogue safe in hypertension."),
            ("Tranexamic acid (1 g IV over 10 minutes)", False, "Tranexamic acid is an antifibrinolytic indicated in all cases of PPH within 3 hours of onset.")
        ],
        "pearl": "PPH Uterotonics Contraindications (Crucial NEET-PG Trap): 1. Methylergonovine (Methergine / Ergometrine): CONTRAINDICATED in HYPERTENSION, Preeclampsia, and Heart Disease (causes severe peripheral vasoconstriction and hypertensive stroke). 2. Carboprost (PGF2-alpha / Hemabate): CONTRAINDICATED in BRONCHIAL ASTHMA (causes potent bronchoconstriction). 3. Misoprostol (PGE1): Safe in both hypertension and asthma.",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 29 (Postpartum Hemorrhage), p. 410-422.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Postpartum Hemorrhage (PPH) Management Protocol",
        "stem": (
            "In a refractory case of severe atonic postpartum hemorrhage that fails to respond to multiple uterotonics, bimanual compression, "
            "and intrauterine balloon tamponade (Bakri balloon), the patient is taken to the operating theater for emergency laparotomy. "
            "The obstetrician decides to place a uterine compression brace suture that compresses the anterior and posterior uterine walls together "
            "without occluding the uterine cavity or ligating major vessels. What is the name of this brace suture technique?"
        ),
        "options": [
            ("B-Lynch brace suture", True, None),
            ("Shirodkar cerclage suture", False, "Shirodkar suture is a cervical cerclage placed for cervical incompetence in the 2nd trimester."),
            ("Kronig incision", False, "Kronig is a low vertical uterine incision for cesarean delivery."),
            ("Pomeroy ligation", False, "Pomeroy is a tubal ligation sterilization technique.")
        ],
        "pearl": "Surgical Management of Atonic PPH: Conservative Surgical Step 1: B-Lynch Brace Suture (or Hayman / Cho square sutures) compresses anterior and posterior uterine walls. Step 2: Bilateral Uterine Artery Ligation (O'Leary stitches). Step 3: Bilateral Internal Iliac Artery Ligation (anterior division). Definitive Last Resort: Subtotal or Total Emergency Peripartum Hysterectomy.",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 29, p. 418-422.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Antepartum Hemorrhage: Placenta Previa vs Abruptio",
        "stem": (
            "A 30-year-old gravida 3 para 2 at 32 weeks of gestation presents to the emergency room with sudden-onset, painless, causeless, recurrent bright red vaginal bleeding "
            "that began while she was resting in bed. She reports normal active fetal movements and denies abdominal pain. "
            "On physical examination, the abdomen is soft, relaxed, and non-tender. The fetal head is floating high above the pelvic brim. "
            "Fetal heart rate is reassuring at 142 beats/min. What is the single most important clinical rule and investigation in the initial management of this patient?"
        ),
        "options": [
            ("Digital Per-Vaginal (PV) examination is strictly contraindicated; perform Transabdominal / Transvaginal Ultrasound immediately", True, None),
            ("Perform an immediate sterile digital vaginal examination to palpate the internal cervical os", False, "DIGITAL PV EXAMINATION IS STRICTLY FORBIDDEN before ultrasound in antepartum hemorrhage; it can tear the placenta previa and induce fatal torrential hemorrhage within minutes!"),
            ("Immediate artificial rupture of membranes (ARM) and oxytocin induction", False, "ARM in major placenta previa causes rapid fetal and maternal exsanguination."),
            ("Immediate emergent hysteroscopy under general anesthesia", False, "Hysteroscopy is strictly contraindicated during third-trimester pregnancy.")
        ],
        "pearl": "Placenta Previa vs Abruptio Placentae: Placenta Previa: Painless, causeless, recurrent, bright red bleeding. Uterus soft, relaxed, non-tender. Fetal parts easily palpable, malpresentation common, FHR usually normal. DIGITAL PV EXAMINATION IS STRICTLY CONTRAINDICATED until placenta previa is ruled out by Ultrasound! Abruptio Placentae: Painful, dark red bleeding, continuous severe abdominal pain. Uterus tense, tender, 'woody hard'. Fetal parts difficult to palpate, fetal distress / demise common.",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 18 (Antepartum Hemorrhage), p. 238-250.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Antepartum Hemorrhage: Placenta Previa vs Abruptio",
        "stem": (
            "A 28-year-old pregnant woman at 35 weeks gestation presents with acute, continuous, agonizing abdominal pain and moderate dark vaginal bleeding. "
            "On abdominal examination, the uterus is intensely hypertonic, 'woody hard', and exquisitely tender to light palpation. "
            "Fetal heart sounds are absent on Doppler. Emergency cesarean delivery is performed, delivering a fresh stillborn fetus. "
            "Upon inspection of the uterus, the obstetrician observes widespread patchy, bluish-purple, purpuric extravasation of blood into the uterine myometrium "
            "and beneath the peritoneal serosa. What is the pathognomonic eponym for this uterine condition?"
        ),
        "options": [
            ("Couvelaire Uterus (Uteroplacental Apoplexy)", True, None),
            ("Bandl's Pathological Retraction Ring", False, "Bandl's ring is a pathological hyper-retraction ring forming between upper and lower uterine segments in obstructed labor."),
            ("Aschoff's myometrial nodule", False, "Aschoff bodies are pathognomonic granulomas of Acute Rheumatic Fever in the myocardium."),
            ("Arias-Stella phenomenon", False, "Arias-Stella reaction is hypersecretory atypical glandular changes in the endometrium seen in ectopic pregnancy.")
        ],
        "pearl": "Couvelaire Uterus (Uteroplacental Apoplexy): Severe complication of concealed Abruptio Placentae. Massive retroplacental hematoma forces blood to dissect between myometrial muscle fibers and beneath the uterine serosa -> uterus appears mottled, dark bluish-purple, and flaccid. Associated with severe Disseminated Intravascular Coagulation (DIC) due to thromboplastin release.",
        "citation": "DC Dutta's Textbook of Obstetrics, 9th Ed, Chapter 18, p. 252-258.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Cervical Cancer Screening & FIGO Staging",
        "stem": (
            "A 42-year-old female undergoes routine cervical cancer screening. High-risk Human Papillomavirus (hrHPV) DNA testing is positive for HPV-16. "
            "Liquid-based cytology demonstrates High-Grade Squamous Intraepithelial Lesion (HSIL). Colposcopy reveals dense, acetowhite epithelium "
            "with coarse punctations and atypical mosaic vascular patterns in the transformation zone. Colposcopy-directed cervical biopsy confirms "
            "Cervical Intraepithelial Neoplasia Grade 3 (CIN-3 / Carcinoma in Situ). What is the definitive management of choice for this patient?"
        ),
        "options": [
            ("Loop Electrosurgical Excision Procedure (LEEP) or Cold Knife Conization", True, None),
            ("Radical Hysterectomy with bilateral pelvic lymphadenectomy (Wertheim operation)", False, "Wertheim radical hysterectomy is indicated for invasive cervical cancer (FIGO Stage IB1-IIA1), not for non-invasive pre-malignant CIN-3!"),
            ("Pelvic external beam radiotherapy (EBRT) plus concurrent Cisplatin chemotherapy", False, "Concurrent chemoradiotherapy is the standard for locally advanced cervical cancer (FIGO Stage IIB-IVA)."),
            ("Topical 5-Fluorouracil vaginal cream for 12 months", False, "Topical 5-FU is not recommended for CIN-3 due to high risk of missed occult invasive carcinoma.")
        ],
        "pearl": "CIN-3 Management: CIN-3 involves full-thickness epithelial dysplasia without breach of the basement membrane. Treatment of choice: Excisional procedure (LEEP / LLETZ or Cold Knife Conization) to completely excise the transformation zone AND provide an intact histological specimen to rule out occult microinvasive carcinoma. High-Risk HPV Types: HPV 16 (most oncogenic, associated with squamous cell carcinoma) and HPV 18 (associated with adenocarcinoma).",
        "citation": "DC Dutta's Textbook of Gynecology, 8th Ed, Chapter 22 (Cervical Cancer), p. 320-332.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Cervical Cancer Screening & FIGO Staging",
        "stem": (
            "A 49-year-old female presents with postcoital bleeding and foul-smelling vaginal discharge. Examination reveals a 3.5 cm ulceroproliferative growth "
            "on the cervix. Clinical and radiological staging reveals that the tumor extends into the upper two-thirds of the vagina, but does NOT involve "
            "the lower third of the vagina, and does NOT extend to the pelvic sidewalls or parametrium. Rectal and bladder mucosa are normal. "
            "According to the 2018 FIGO Staging of Carcinoma Cervix, what is the stage of this disease?"
        ),
        "options": [
            ("Stage IIA1 (involves upper 2/3 of vagina, tumor ≤4 cm, no parametrial invasion)", True, None),
            ("Stage IIB (parametrial invasion present)", False, "Stage IIB requires invasion into the parametrium, which is explicitly absent here."),
            ("Stage IIIA (involvement of lower third of vagina)", False, "Stage IIIA involves the lower third of the vagina."),
            ("Stage IIIB (extension to pelvic sidewall or hydronephrosis)", False, "Stage IIIB extends to the pelvic sidewall or causes hydronephrosis/non-functioning kidney.")
        ],
        "pearl": "FIGO 2018 Staging of Carcinoma Cervix: Stage I: Confined to cervix (IA: microinvasive ≤5 mm; IB: clinically visible). Stage II: Extends beyond cervix but NOT to pelvic sidewall or lower 1/3 of vagina (IIA: upper 2/3 vagina, no parametrium; IIA1 ≤4 cm, IIA2 >4 cm; IIB: PARAMETRIAL INVASION). Stage III: Involves lower 1/3 of vagina (IIIA) OR Pelvic sidewall / Hydronephrosis (IIIB) OR Pelvic/Para-aortic lymph nodes (IIIC). Stage IV: Bladder/rectal mucosa invasion (IVA) or Distant metastases (IVB). SURGICAL CUT-OFF: Up to Stage IIA1 is operable (Radical Hysterectomy); Stage IIB onwards is treated with CONCURRENT CHEMORADIOTHERAPY (CCRT).",
        "citation": "FIGO Staging for Cervical Cancer (2018) / DC Dutta Gynecology Ch 22, p. 326-330.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Polycystic Ovary Syndrome (Rotterdam Criteria)",
        "stem": (
            "A 23-year-old nulligravida presents with irregular menstrual cycles (oligomenorrhea with 3-4 cycles per year) since menarche at age 13, "
            "moderate facial hirsutism (Ferriman-Gallwey score 12), and severe cystic acne. Her BMI is 29.4 kg/m2. "
            "Transvaginal ultrasonography demonstrates bilateral enlarged ovaries (>10 mL volume) with 18 small subcapsular follicles (2-9 mm) "
            "arranged in a peripheral 'string of pearls' appearance around a dense echogenic stroma. "
            "According to the consensus Rotterdam Diagnostic Criteria for Polycystic Ovary Syndrome (PCOS), how many of the 3 cardinal criteria "
            "must be fulfilled after excluding mimicking endocrinopathies?"
        ),
        "options": [
            ("At least 2 out of the 3 criteria (Oligo-/anovulation, Hyperandrogenism, Polycystic ovarian morphology)", True, None),
            ("All 3 criteria must be strictly present simultaneously", False, "Rotterdam criteria requires only 2 out of 3 features, creating 4 distinct clinical phenotypes."),
            ("Only biochemical hyperandrogenemia is mandatory", False, "Clinical hyperandrogenism (hirsutism/acne) is sufficient; biochemical elevation is not mandatory."),
            ("Requires documented insulin resistance and bilateral ovarian biopsy", False, "Ovarian biopsy is never indicated for PCOS diagnosis.")
        ],
        "pearl": "Rotterdam Criteria for PCOS: Requires AT LEAST 2 OF 3 features (after ruling out Congenital Adrenal Hyperplasia, Cushing's, Hyperprolactinemia, and androgen-secreting tumors): 1. Oligo- or Anovulation (menstrual irregularity) | 2. Clinical and/or biochemical signs of Hyperandrogenism | 3. Polycystic Ovaries on Ultrasound (≥20 follicles per ovary of 2-9 mm size OR ovarian volume ≥10 mL). LH:FSH ratio is typically elevated to >2:1 or 3:1.",
        "citation": "DC Dutta's Textbook of Gynecology, 8th Ed, Chapter 28 (PCOS), p. 410-418.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Polycystic Ovary Syndrome (Rotterdam Criteria)",
        "stem": (
            "A 27-year-old woman with known PCOS and secondary infertility presents desiring to conceive. "
            "She has anovulatory cycles with normal tubal patency on hysterosalpingography and normal partner semen parameters. "
            "According to international evidence-based guidelines (Monash / ASRM 2023 update), what is the first-line oral pharmacological ovulation-induction agent of choice?"
        ),
        "options": [
            ("Letrozole (Aromatase Inhibitor, 2.5 mg daily for 5 days from cycle day 3)", True, None),
            ("Clomiphene Citrate (Selective Estrogen Receptor Modulator)", False, "Letrozole has SUPERSEDED Clomiphene citrate as the first-line oral agent for ovulation induction in PCOS, yielding significantly higher live-birth and ovulation rates with lower multiple pregnancy rates."),
            ("Metformin monotherapy alone", False, "Metformin improves insulin resistance but is inferior to Letrozole for ovulation induction and live-birth rates."),
            ("Intravenous Human Menopausal Gonadotropin (hMG) high-dose protocol", False, "Gonadotropins are second-line therapy due to high risks of Ovarian Hyperstimulation Syndrome (OHSS) and multiple pregnancies.")
        ],
        "pearl": "Ovulation Induction in PCOS: FIRST-LINE DRUG OF CHOICE: LETROZOLE (Aromatase inhibitor). Mechanism: Inhibits estrogen synthesis in ovaries and brain -> removes negative feedback on hypothalamus -> increases pituitary FSH release to stimulate monofollicular development. Superior to Clomiphene (higher live birth rates, no anti-estrogenic effect on endometrium/cervical mucus, lower risk of multiple gestations).",
        "citation": "International Evidence-Based Guideline for the Assessment and Management of PCOS (2023 Update) / DC Dutta Gynecology Ch 28.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Ovarian Tumors & RMI Scoring",
        "stem": (
            "A 58-year-old postmenopausal woman presents with progressive abdominal distension, early satiety, and vague pelvic discomfort for 3 months. "
            "Physical examination reveals a fixed, nodular, non-tender pelvic mass measuring 8 cm in diameter, along with shifting dullness indicative of ascites. "
            "Transvaginal ultrasound demonstrates a multilocular, solid-cystic left ovarian mass with thick internal septations (>3 mm) and papillary projections. "
            "Serum CA-125 level is markedly elevated at 480 U/mL (normal <35 U/mL). What is the most common histological subtype of malignant ovarian neoplasm?"
        ),
        "options": [
            ("Serous Cystadenocarcinoma (High-Grade Serous Carcinoma)", True, None),
            ("Mucinous Cystadenocarcinoma", False, "Mucinous carcinomas account for ~10% and are associated with pseudomyxoma peritonei."),
            ("Granulosa Cell Tumor", False, "Granulosa cell tumor is a sex cord-stromal tumor producing estrogen with Call-Exner bodies."),
            ("Dysgerminoma", False, "Dysgerminoma is a malignant germ cell tumor occurring in young adolescents (elevated LDH).")
        ],
        "pearl": "Ovarian Malignancy Key Facts: Most common overall ovarian cancer (70-80%): Epithelial Ovarian Cancer (EOC) -> Serous Cystadenocarcinoma (High-Grade Serous Carcinoma, HGSC). Originates from the fimbriated end of the Fallopian tube in many cases with TP53 mutations. Tumor Marker: CA-125 (glycoprotein antigen, monitored for recurrence). Risk of Malignancy Index (RMI) combines: Ultrasound score (U) x Menopausal status (M) x Serum CA-125 level (U/mL). RMI > 200 carries high risk of malignancy.",
        "citation": "DC Dutta's Textbook of Gynecology, 8th Ed, Chapter 23 (Ovarian Tumors), p. 340-358.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Ovarian Tumors & RMI Scoring",
        "stem": (
            "A 19-year-old nulliparous female presents with acute severe right iliac fossa pain and low-grade fever. "
            "Emergency pelvic ultrasound reveals a 7 cm well-circumscribed, cystic right ovarian mass containing fluid with hyperechoic lines and dots "
            "('dermoid mesh'), an intensely echogenic mural nodule with posterior acoustic shadowing ('Rokitansky protuberance'), "
            "and a fluid-fat level. What is the most common histological composition of this benign ovarian tumor?"
        ),
        "options": [
            ("Mature Cystic Teratoma (Benign Dermoid Cyst) containing tissues derived from all three germ layers", True, None),
            ("Fibroma with ascites and right pleural effusion (Meigs syndrome)", False, "Fibroma is a solid stromal tumor composed of spindle cells producing collagen."),
            ("Endometrioma (chocolate cyst) lined by endometrial glands and stroma", False, "Endometrioma exhibits diffuse low-level internal echoes ('ground glass' appearance)."),
            ("Serous cystadenoma lined by single-layered ciliated columnar epithelium", False, "Serous cystadenoma is thin-walled unilocular filled with clear watery fluid.")
        ],
        "pearl": "Mature Cystic Teratoma (Dermoid Cyst): Most common benign ovarian germ cell tumor in women aged 20-30 years. Derived from all 3 germ layers (ectoderm, mesoderm, endoderm). Contains hair, sebum, squamous epithelium, teeth, cartilage, and thyroid tissue (struma ovarii). Ultrasound signs: Rokitansky protuberance (dermoid plug) + Tip of the iceberg sign + Dermoid mesh. Most common complication: Torsion (15%). Malignant transformation (<1-2%): Squamous cell carcinoma.",
        "citation": "DC Dutta's Textbook of Gynecology, 8th Ed, Chapter 23, p. 346-350.",
        "difficulty": "moderate"
    }
]
