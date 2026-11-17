"""
Authentic High-Yield NEET-PG Clinical Questions for Pathology
References: Robbins and Cotran Pathologic Basis of Disease (10th Ed)
"""

PATHOLOGY_QUESTIONS = [
    {
        "concept_name": "Liquefactive vs Coagulative Necrosis in Hypoxic Ischemic Tissue",
        "stem": (
            "A 68-year-old male with long-standing atrial fibrillation develops an acute thromboembolic ischemic stroke "
            "resulting in right-sided dense hemiplegia and expressive aphasia. He passes away 8 days later from aspiration pneumonia. "
            "At autopsy, neuropathological examination of the brain tissue in the left middle cerebral artery territory demonstrates "
            "enzymatic dissolution of the cerebral parenchyma with cystic, fluid-filled cavitation filled with lipid-laden macrophages. "
            "What type of tissue necrosis is characteristically seen in hypoxic-ischemic death of the Central Nervous System (CNS)?"
        ),
        "options": [
            ("Liquefactive Necrosis", True, None),
            ("Coagulative Necrosis", False, "Coagulative necrosis is characteristic of ischemic infarction in ALL solid organs (heart, kidney, spleen, liver), but NOT the brain!"),
            ("Caseous Necrosis", False, "Caseous necrosis is pathognomonic for tuberculous granulomatous infection ('cheese-like' appearance)."),
            ("Fibrinoid Necrosis", False, "Fibrinoid necrosis occurs in immune vasculitis and malignant hypertension where immune complexes deposit in blood vessel walls.")
        ],
        "pearl": "Necrosis Types Golden Rule: CNS / BRAIN INFARCTION = LIQUEFACTIVE NECROSIS! In the brain, lack of structural extracellular collagen matrix and high concentration of hydrolytic enzymes and lipid content lead to rapid enzymatic dissolution of dead tissue into a soft liquid viscous mass (later forming a cystic cavity). ALL OTHER SOLID VISCERA (Myocardial infarction, Renal infarction, Splenic infarction) = COAGULATIVE NECROSIS (denaturation of structural proteins preserves cell architecture and outlines for days; 'tombstone' appearance).",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 2 (Cell Death), p. 42-48.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Cell Injury, Necrosis & Apoptosis",
        "stem": (
            "During intrinsic (mitochondrial) pathway of apoptosis in response to DNA damage or growth factor deprivation, "
            "which pro-apoptotic protein translocates from the mitochondrial intermembrane space into the cytosol "
            "to bind Apaf-1 (Apoptotic Protease Activating Factor-1) and form the wheel-like 'Apoptosome' complex?"
        ),
        "options": [
            ("Cytochrome c", True, None),
            ("Bcl-2", False, "Bcl-2 is an ANTI-apoptotic protein located in the outer mitochondrial membrane that prevents cytochrome c release."),
            ("Bcl-xL", False, "Bcl-xL is an anti-apoptotic protein that neutralizes pro-apoptotic Bax/Bak."),
            ("Fas Ligand (FasL / CD95L)", False, "Fas Ligand triggers the EXTRINSIC (death receptor) pathway of apoptosis via Caspase-8, not the mitochondrial pathway.")
        ],
        "pearl": "Apoptosis Pathways: 1. Intrinsic (Mitochondrial) Pathway: Major pathway. Pro-apoptotic sensors (BH3-only: Bad, Bim, Bid) activate effector channels (Bax and Bak) -> outer membrane permeabilization -> CYTOCHROME C leaks into cytosol -> binds Apaf-1 -> forms APOPTOSOME -> cleaves Procaspase-9 -> activates executioner Caspase-3 and Caspase-6. Anti-apoptotic gatekeepers: Bcl-2 and Bcl-xL. 2. Extrinsic (Death Receptor) Pathway: Fas (CD95) or TNF-R1 binds FasL -> FADD recruitment -> activates Caspase-8 and Caspase-10.",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 2, p. 52-60.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Acute & Chronic Inflammation Mechanisms",
        "stem": (
            "During the cellular phase of acute inflammation, circulating leukocytes exit the post-capillary venule lumen "
            "to reach the extravascular site of injury. Which family of adhesion molecules expressed on activated endothelial cells "
            "(specifically E-selectin and P-selectin) mediates the initial low-affinity transient 'ROLLING' of leukocytes "
            "by binding to Sialyl-Lewis X glycoproteins on leukocyte microvilli?"
        ),
        "options": [
            ("Selectins (E-selectin, P-selectin, and L-selectin)", True, None),
            ("Integrins (LFA-1, Mac-1, and VLA-4)", False, "Integrins mediate high-affinity FIRM ADHESION and arrest, not initial rolling."),
            ("Immunoglobulin superfamily cell adhesion molecules (ICAM-1 and VCAM-1)", False, "ICAM-1 and VCAM-1 are ligands for integrins mediating firm adhesion."),
            ("PECAM-1 (CD31)", False, "PECAM-1 (CD31) mediates Transmigration / Diapedesis through the endothelial intercellular junction.")
        ],
        "pearl": "Leukocyte Extravasation Sequence: 1. Margination & ROLLING: Mediated by SELECTINS (P-selectin stored in Weibel-Palade bodies, E-selectin induced by TNF/IL-1) binding to Sialyl-Lewis X. (Defective in Leukocyte Adhesion Deficiency Type 2 / LAD-2). 2. FIRM ADHESION & Arrest: Mediated by INTEGRINS on leukocytes (LFA-1 / CD11aCD18, Mac-1) binding to ICAM-1/VCAM-1 on endothelium. (Defective in LAD-1 due to beta-2 integrin / CD18 mutation). 3. TRANSMIGRATION (Diapedesis): Mediated by PECAM-1 (CD31). 4. CHEMOTAXIS: Directed migration along gradient of C5a, LTB4, IL-8, and bacterial formyl peptides.",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 3 (Inflammation), p. 74-88.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Microcytic & Macrocytic Anemias",
        "stem": (
            "A 32-year-old female presents with fatigue, exertional breathlessness, pica (craving to eat raw ice and clay), "
            "and spoon-shaped brittle nails (koilonychia). Complete blood count reveals: Hb 7.2 g/dL, MCV 64 fL (microcytic), "
            "MCH 20 pg, and Red Cell Distribution Width (RDW) is elevated at 18.2% (normal 11.5-14.5%). "
            "Which of the following serum iron profile combinations confirms the diagnosis of Iron Deficiency Anemia (IDA)?"
        ),
        "options": [
            ("Low Serum Ferritin, Low Serum Iron, High Total Iron-Binding Capacity (TIBC), and Low Transferrin Saturation (<15%)", True, None),
            ("High Serum Ferritin, Low Serum Iron, Low TIBC, and Normal Transferrin Saturation", False, "High ferritin with low TIBC is the classic profile of Anemia of Chronic Disease / Inflammation (hepcidin-mediated iron trapping)."),
            ("Normal Serum Ferritin, High Serum Iron, Normal TIBC, and Target cells on peripheral smear", False, "Normal/high ferritin with target cells is characteristic of Beta-Thalassemia Trait (normal RDW <14%)."),
            ("Markedly elevated Serum Ferritin (>1000 ng/mL) with ring sideroblasts in bone marrow", False, "High ferritin with ringed sideroblasts indicates Sideroblastic Anemia or Hemochromatosis.")
        ],
        "pearl": "Iron Deficiency vs Anemia of Chronic Disease: Iron Deficiency Anemia (IDA): Serum Ferritin is LOW (<15-30 mcg/L; most sensitive and specific test!) | Serum Iron is LOW | TIBC is HIGH (liver synthesizes more transferrin) | Transferrin Saturation <15% | RDW is HIGH (>15%). Anemia of Chronic Disease (ACD): Mediated by HEPCIDIN (induced by IL-6). Hepcidin degrades ferroportin -> traps iron in macrophages -> Serum Ferritin is NORMAL or HIGH (acute phase reactant) | TIBC is LOW | Serum Iron is Low.",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 14 (Red Blood Cells), p. 640-652.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Microcytic & Macrocytic Anemias",
        "stem": (
            "A 56-year-old strict vegan presents with progressive paresthesias and numbness in his feet, unsteady gait, and severe fatigue. "
            "Peripheral blood smear reveals macro-ovalocytes, severe anisopoikilocytosis, and prominent hypersegmented neutrophils "
            "(neutrophils with ≥6 nuclear lobes). Serum Vitamin B12 is 92 pg/mL (low). "
            "Which biochemical intermediate is elevated in both serum and urine in Vitamin B12 (Cobalamin) deficiency, "
            "but remains completely NORMAL in pure Folate (Vitamin B9) deficiency?"
        ),
        "options": [
            ("Methylmalonic Acid (MMA)", True, None),
            ("Homocysteine", False, "Homocysteine is elevated in BOTH Vitamin B12 and Folate deficiency, so it cannot distinguish between them."),
            ("Orotic acid", False, "Orotic acid is elevated in Orotic Aciduria and Ornithine Transcarbamylase (OTC) deficiency, not megaloblastic anemia."),
            ("Formiminoglutamic acid (FIGLU)", False, "FIGLU is elevated specifically in Folate deficiency, not B12.")
        ],
        "pearl": "Megaloblastic Anemia: B12 vs Folate: HALLMARK ON SMEAR: Hypersegmented Neutrophils (>5% with 5 lobes or any neutrophil with ≥6 lobes). Biochemical differentiation: 1. Serum Homocysteine: Elevated in BOTH B12 and Folate deficiency (both needed for homocysteine -> methionine via methionine synthase). 2. METHYLMALONIC ACID (MMA): ELEVATED ONLY IN VITAMIN B12 DEFICIENCY! (B12 is required as a cofactor for Methylmalonyl-CoA mutase -> Succinyl-CoA). High MMA leads to abnormal fatty acid incorporation into neuronal myelin -> Subacute Combined Degeneration of the spinal cord (SCD: dorsal columns + lateral corticospinal tracts).",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 14, p. 654-662.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Glomerular Diseases & Nephrotic Syndrome",
        "stem": (
            "A 7-year-old boy presents with periorbital puffiness and facial edema for 1 week. Urinalysis shows 4+ proteinuria "
            "with zero RBCs and zero casts. Serum albumin is 1.8 g/dL and total cholesterol is 360 mg/dL. Renal function is normal. "
            "Light microscopy of a renal biopsy specimen shows completely normal-appearing glomeruli without hypercellularity or basement membrane thickening. "
            "Immunofluorescence is negative for all immunoglobulins and complement components. "
            "What pathognomonic ultrastructural finding is visualized on Electron Microscopy (EM)?"
        ),
        "options": [
            ("Diffuse effacement (flattening and loss) of visceral epithelial podocyte foot processes", True, None),
            ("Subepithelial electron-dense 'dome-and-spike' deposits", False, "Spike and dome subepithelial deposits are pathognomonic of Membranous Nephropathy."),
            ("Large subepithelial electron-dense 'humps'", False, "Subepithelial humps are characteristic of Post-Streptococcal Glomerulonephritis (PSGN)."),
            ("Splitting and lamellation of the glomerular basement membrane ('tram-track' appearance)", False, "Tram-track appearance is seen in Membranoproliferative Glomerulonephritis (MPGN).")
        ],
        "pearl": "Minimal Change Disease (Lipoid Nephrosis): Most common cause of Nephrotic Syndrome in children (85-90%). 1. Light Microscopy: Completely NORMAL glomeruli (hence 'minimal change'). 2. Immunofluorescence: Completely NEGATIVE (no immune complexes). 3. Electron Microscopy: DIFFUSE EFFACEMENT OF PODOCYTE FOOT PROCESSES. Associated with Hodgkin Lymphoma. Responds dramatically to oral corticosteroids (>90% complete remission).",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 20 (The Kidney), p. 910-918.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Glomerular Diseases & Nephrotic Syndrome",
        "stem": (
            "A 46-year-old male presents with adult-onset nephrotic syndrome (proteinuria 7.8 g/24 hr). "
            "Renal biopsy demonstrates diffuse, uniform thickening of the Glomerular Basement Membrane (GBM) throughout all capillary loops on light microscopy. "
            "Silver methenamine stain reveals prominent black 'spikes' protruding from the basement membrane between immune deposits ('spike-and-dome' pattern). "
            "Immunofluorescence demonstrates granular IgG and C3 deposits along all capillary loops. "
            "Autoantibodies against which podocyte cell-surface antigen are responsible for >70-80% of primary/idiopathic cases of this disease?"
        ),
        "options": [
            ("M-type Phospholipase A2 Receptor (anti-PLA2R autoantibodies)", True, None),
            ("Anti-Glomerular Basement Membrane (anti-GBM) antibodies against alpha-3 chain of Type IV collagen", False, "Anti-GBM antibodies cause Goodpasture disease, showing linear smooth IgG staining and crescentic glomerulonephritis."),
            ("Anti-Neutrophil Cytoplasmic Antibodies (c-ANCA / PR3)", False, "c-ANCA is associated with Granulomatosis with Polyangiitis (Wegener's), causing pauci-immune crescentic GN."),
            ("Anti-Streptolysin O (ASO)", False, "ASO titers reflect antecedent group A streptococcal infection in PSGN.")
        ],
        "pearl": "Membranous Nephropathy (MN): Most common cause of primary nephrotic syndrome in non-diabetic white adults. Light microscopy: Diffuse capillary wall thickening without cellular proliferation. Silver stain: 'Spike and Dome' pattern. IF: Granular capillary loop IgG and C3. PRIMARY CAUSE (70-85%): Autoantibodies against Phospholipase A2 Receptor (anti-PLA2R). Secondary causes: Hepatitis B, Hepatitis C, Syphilis, NSAIDs, Gold/Penicillamine, and solid organ malignancies (Carcinoma of lung/colon/breast). High risk of renal vein thrombosis!",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 20, p. 918-925.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Oncogenes & Tumor Suppressor Genes",
        "stem": (
            "Knudson's 'Two-Hit' Hypothesis of oncogenesis explains the familial versus sporadic occurrence of malignant tumors. "
            "According to this model, which classic tumor suppressor gene located on chromosome 13q14 requires the inactivation or loss of function "
            "of BOTH alleles for retinoblastoma and osteosarcoma development?"
        ),
        "options": [
            ("RB1 (Retinoblastoma gene)", True, None),
            ("TP53", False, "TP53 is the 'guardian of the genome' on chromosome 17p, mutated in Li-Fraumeni syndrome."),
            ("APC (Adenomatous Polyposis Coli)", False, "APC is on chromosome 5q, mutated in Familial Adenomatous Polyposis (FAP)."),
            ("BRCA1", False, "BRCA1 is a DNA repair gene on chromosome 17q, linked to hereditary breast and ovarian cancer.")
        ],
        "pearl": "Knudson's Two-Hit Model & RB1: RB1 gene (chromosome 13q14) encodes pRb, the governor of the cell cycle (G1 to S phase checkpoint). Unphosphorylated / hypophosphorylated pRb binds and sequesters E2F transcription factors -> arrests cell in G1. Phosphorylation of pRb by Cyclin D-CDK4/6 releases E2F -> drives S-phase entry. Knudson's Model: Familial Retinoblastoma: 1st hit inherited via germline in all cells; 2nd hit occurs somatically in retina (bilateral tumors, high risk of Osteosarcoma). Sporadic Retinoblastoma: Both hits occur somatically in the same retinal cell (unilateral).",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 7 (Neoplasia), p. 288-302.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Oncogenes & Tumor Suppressor Genes",
        "stem": (
            "A 28-year-old female presents with multiple primary malignancies in her early twenties, including an invasive ductal breast carcinoma, "
            "a soft tissue liposarcoma of the thigh, an adrenocortical carcinoma, and an astrocytoma. Her mother died of early-onset bilateral breast cancer "
            "and her brother died of osteosarcoma at age 14. What familial cancer syndrome is this, and what gene mutation is responsible?"
        ),
        "options": [
            ("Li-Fraumeni Syndrome; Germline mutation in the TP53 tumor suppressor gene on chromosome 17p", True, None),
            ("Lynch Syndrome (Hereditary Non-Polyposis Colorectal Cancer); Germline mutation in DNA mismatch repair genes (MLH1, MSH2)", False, "Lynch syndrome causes colorectal, endometrial, ovarian, and transitional cell urothelial carcinomas."),
            ("Multiple Endocrine Neoplasia Type 1 (MEN 1); Menin gene mutation on chromosome 11q", False, "MEN 1 triad: Parathyroid adenomas, Pituitary adenomas, and Pancreatic neuroendocrine tumors (3 Ps)."),
            ("Von Hippel-Lindau (VHL) Syndrome; VHL gene mutation on chromosome 3p", False, "VHL features hemangioblastomas of cerebellum/retina, clear cell renal cell carcinoma, and pheochromocytoma.")
        ],
        "pearl": "Li-Fraumeni Syndrome: Autosomal dominant germline mutation in TP53 ('guardian of the genome', chromosome 17p13). 25-fold higher risk of cancer by age 50. Classic Tumor Spectrum (SBLA mnemonic): Sarcoma (soft tissue and osteosarcoma) | Breast cancer | Leukemia / Brain tumors | Adrenocortical carcinoma.",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 7, p. 296-304.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Acute & Chronic Leukemias",
        "stem": (
            "A 52-year-old male undergoes a routine health evaluation. He is completely asymptomatic. "
            "On physical examination, he has massive, firm, non-tender splenomegaly extending 14 cm below the left costal margin into the pelvis. "
            "Complete blood count reveals: Total Leukocyte Count (TLC) 184,000/uL with the entire spectrum of myeloid maturation "
            "(myeloblasts <3%, promyelocytes, myelocytes, metamyelocytes, band forms, and segmented neutrophils), with prominent basophilia and eosinophilia. "
            "Leukocyte Alkaline Phosphatase (LAP / NAP) score is markedly DECREASED at 8 (normal 40-100). "
            "What is the pathognomonic cytogenetic abnormality and targeted molecular therapy of choice?"
        ),
        "options": [
            ("t(9;22)(q34;q11.2) creating the BCR-ABL1 fusion oncogene (Philadelphia Chromosome); Imatinib mesylate (Tyrosine Kinase Inhibitor)", True, None),
            ("t(15;17)(q22;q12) PML-RARA fusion; All-Trans Retinoic Acid (ATRA) plus Arsenic Trioxide", False, "t(15;17) is pathognomonic for Acute Promyelocytic Leukemia (APL / AML-M3) characterized by Auer rods and DIC risk."),
            ("t(12;21)(p13;q22) ETV6-RUNX1 fusion; Intravenous Methotrexate", False, "t(12;21) is seen in pediatric B-ALL with excellent prognosis."),
            ("t(8;21)(q22;q22) RUNX1-RUNX1T1 fusion; Cytarabine and Daunorubicin", False, "t(8;21) is seen in AML with maturation (AML-M2).")
        ],
        "pearl": "Chronic Myeloid Leukemia (CML): Myeloproliferative neoplasm characterized by uncontrolled granulocytic proliferation. Hallmarks: 1. Massive Splenomegaly | 2. Extreme leukocytosis with entire spectrum of myeloid precursors (myelocytes/metamyelocytes predominate) + absolute basophilia | 3. LAP / NAP SCORE IS LOW OR ZERO (Differentiates CML from Leukemoid Reaction where LAP is high!). 4. Cytogenetics: PHILADELPHIA CHROMOSOME t(9;22)(q34;q11) -> creates constitutively active BCR-ABL1 receptor tyrosine kinase oncoprotein (p210). FIRST-LINE TARGETED THERAPY: IMATINIB MESYLATE (TKI).",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 13 (Diseases of White Blood Cells), p. 608-618.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Acute & Chronic Leukemias",
        "stem": (
            "A 28-year-old male presents with fever, spontaneous gingival bleeding, epistaxis, and multiple ecchymoses. "
            "Bone marrow aspirate demonstrates 65% abnormal, hypergranular promyelocytes packed with multiple needle-like crystalline cytoplasmic inclusions "
            "arranged in bundles or clusters ('faggot cells'). Coagulation profile reveals prolonged PT and aPTT, elevated D-dimer, and profound hypofibrinogenemia "
            "indicative of fulminant Disseminated Intravascular Coagulation (DIC). What is the diagnosis, and what is the definitive differentiation therapy?"
        ),
        "options": [
            ("Acute Promyelocytic Leukemia (APL, AML-M3); All-Trans Retinoic Acid (ATRA) combined with Arsenic Trioxide (ATO)", True, None),
            ("Chronic Lymphocytic Leukemia (CLL); Fludarabine and Rituximab", False, "CLL features mature-appearing small lymphocytes with smudge/basket cells, not Auer rods or DIC."),
            ("Hairy Cell Leukemia; Cladribine (2-CdA)", False, "Hairy cell leukemia features tartrate-resistant acid phosphatase (TRAP) positive B cells and dry tap."),
            ("Burkitt Lymphoma; CHOP chemotherapy", False, "Burkitt lymphoma exhibits a 'starry-sky' appearance on biopsy.")
        ],
        "pearl": "Acute Promyelocytic Leukemia (APL / AML-M3): Cytogenetics: t(15;17)(q22;q12) -> PML-RARA fusion gene, blocking promyelocyte differentiation. Histology: AUER RODS in bundles ('FAGGOT CELLS'). Clinical emergency: Massive release of procoagulant granules triggers fulminant DIC! DIFFERENTIATION THERAPY: ALL-TRANS RETINOIC ACID (ATRA / Tretinoin) + ARSENIC TRIOXIDE (ATO). ATRA forces malignant promyelocytes to differentiate into mature non-proliferative neutrophils! Curable in >90% without conventional cytotoxic chemotherapy.",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 13, p. 598-605.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Hodgkin & Non-Hodgkin Lymphomas",
        "stem": (
            "A 26-year-old male presents with persistent, painless, rubbery cervical lymphadenopathy for 3 months, accompanied by drenching night sweats "
            "and intermittent cyclical high fevers lasting 1-2 weeks alternating with afebrile periods of similar duration (Pel-Ebstein fever). "
            "Excisional lymph node biopsy reveals broad collagen bands dividing the lymphoid tissue into circumscribed nodules. "
            "Scattered within the nodules are large, binucleated malignant cells with prominent, eosinophilic, inclusion-like nucleoli resembling 'owl-eyes' "
            "(Reed-Sternberg cells), along with 'lacunar cells' retracting inside artifactual clear spaces. "
            "What is the diagnosis, and which immunophenotypic marker profile is characteristic of classic Reed-Sternberg cells?"
        ),
        "options": [
            ("Nodular Sclerosis Hodgkin Lymphoma; CD15 positive, CD30 positive, CD20 negative, and CD45 negative", True, None),
            ("Diffuse Large B-Cell Lymphoma (DLBCL); CD20 positive, CD19 positive, CD15 negative", False, "DLBCL is a diffuse high-grade Non-Hodgkin Lymphoma expressing pan-B-cell markers (CD19, CD20)."),
            ("Follicular Lymphoma; CD10 positive, BCL-2 positive, CD5 negative", False, "Follicular lymphoma features t(14;18) overexpressing BCL-2."),
            ("Burkitt Lymphoma; c-MYC positive, CD15 negative", False, "Burkitt lymphoma is a high-grade B-cell NHL with t(8;14).")
        ],
        "pearl": "Hodgkin Lymphoma (HL) Classification & Markers: Most common subtype in young adults (65-70%): NODULAR SCLEROSIS (NSHL, female = male, collagen bands, LACUNAR REED-STERNBERG CELLS). Pel-Ebstein Fever: Cyclical waxing/waning fever. Alcohol-induced lymph node pain. CLASSIC REED-STERNBERG CELL IMMUNOPHENOTYPE: CD15 POSITIVE | CD30 POSITIVE | CD20 NEGATIVE (or weak) | CD45 (LCA) NEGATIVE. (Mnemonic: '15 x 2 = 30; 20 and 45 are negative'). Exception: Nodular Lymphocyte Predominant HL (NLPHL) features 'Popcorn cells' that are CD20+, CD45+, and CD15-/CD30-.",
        "citation": "Robbins and Cotran Pathologic Basis of Disease, 10th Ed, Chapter 13, p. 620-632.",
        "difficulty": "easy"
    }
]
