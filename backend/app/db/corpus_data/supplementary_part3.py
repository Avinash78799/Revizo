"""
Supplementary High-Yield NEET-PG Clinical Questions: Part 3
Covers: Pathology (5), Microbiology (6), Forensic Medicine (6), Community Medicine (6).
"""

SUPPLEMENTARY_PART3 = [
    # =========================================================================
    # --- PATHOLOGY (5 Questions) ---
    # =========================================================================
    {
        "subject": "Pathology",
        "concept_name": "Cellular Injury: Patterns of Tissue Necrosis & Molecular Mechanisms",
        "stem": (
            "A 62-year-old male with long-standing severe peripheral vascular disease and diabetes presents with dry gangrene of his left great toe. "
            "Simultaneously, a 70-year-old female presents with an acute middle cerebral artery stroke resulting in an infarct. "
            "What distinct histological types of tissue necrosis occur in the ischemic great toe versus the ischemic cerebral cortex, and why?"
        ),
        "options": [
            ("Coagulative necrosis in the ischemic toe (denaturation of structural proteins with preserved cellular outlines); Liquefactive necrosis in the brain (rapid enzymatic digestion by microglial hydrolytic enzymes)", True, None),
            ("Liquefactive necrosis in both sites due to bacterial secondary infection and neutrophil infiltration", False, "Dry gangrene is aseptic coagulative necrosis, not liquefactive necrosis; liquefactive necrosis occurs in wet gangrene and the CNS."),
            ("Caseous necrosis in the toe due to lipid accumulation; Fibrinoid necrosis in the cerebral cortex", False, "Caseous necrosis is characteristic of tuberculous granulomas; fibrinoid necrosis occurs in immune vasculitis and malignant hypertension."),
            ("Fat necrosis in the toe with saponification; Coagulative necrosis in the brain", False, "The brain undergoes liquefactive necrosis, NOT coagulative necrosis, due to absence of supporting extracellular connective tissue and abundant lysosomes.")
        ],
        "pearl": "Patterns of Tissue Necrosis: 1. COAGULATIVE NECROSIS: Mechanism: Severe ischemia/hypoxia denatures structural proteins and cellular enzymes, blocking proteolysis. Microscopic hallmark: PRESERVATION OF BASIC ARCHITECTURAL TISSUE OUTLINE FOR SEVERAL DAYS ('GHOST CELLS' / tombstone outlines with loss of nuclei: karyolysis, pyknosis, karyorrhexis). Seen in: Ischemic infarction of ALL SOLID ORGANS (Heart, Kidney, Spleen, Liver, Limb) &mdash; EXCEPT THE BRAIN! 2. LIQUEFACTIVE NECROSIS: Rapid enzymatic digestion of dead cells transforms tissue into a liquid viscous mass (pus/abscess). Seen in: (A) BACTERIAL and FUNGAL FOCAL INFECTIONS (neutrophilic enzymes liquefy tissue into an abscess); (B) HYPOXIC INFARCTION OF THE CENTRAL NERVOUS SYSTEM (Brain and Spinal Cord): Microglial and astrocytic hydrolytic lysosomal enzymes rapidly digest the lipid-rich cerebral tissue into fluid-filled cystic cavities! 3. CASEOUS NECROSIS: Amorphous granular eosinophilic debris surrounded by epithelioid granulomas ('cheesy' gross appearance). Pathognomonic for TUBERCULOSIS. 4. FAT NECROSIS: Enzymatic (acute pancreatitis releases lipases that cleave triglycerides, combining with calcium to form chalky white SAPONIFICATION) vs Traumatic (breast trauma). 5. FIBRINOID NECROSIS: Antigen-antibody immune complexes deposit in arterial walls with fibrin (Polyarteritis nodosa, malignant hypertension).",
        "citation": "Robbins & Cotran Pathologic Basis of Disease, 10th Ed, Chapter 2 (Cell Death), p. 43-48; Harsh Mohan Textbook of Pathology, 8th Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Pathology",
        "concept_name": "Hematologic Malignancies: Acute Promyelocytic Leukemia (APL) & Cytogenetics",
        "stem": (
            "A 28-year-old female presents with spontaneous epistaxis, extensive cutaneous ecchymoses, and gum bleeding. "
            "Complete blood count reveals hemoglobin 7.4 g/dL, platelet count 18,000/mcL, and WBC 4,200/mcL. Coagulation profile shows marked "
            "disseminated intravascular coagulation (DIC) with prolonged PT, prolonged aPTT, severe hypofibrinogenemia (fibrinogen 64 mg/dL), "
            "and markedly elevated D-dimer. Peripheral blood smear and bone marrow aspirate show sheets of immature myeloid cells packed with "
            "heavy, coarse azurophilic granules and bundles of needle-like cytoplasmic inclusions ('Auer rods' in sheaves, forming 'Faggot Cells'). "
            "What specific chromosomal translocation defines this condition, and what targeted differentiation therapy provides a >90% cure rate?"
        ),
        "options": [
            ("t(15;17)(q24;q21) generating the PML-RARA fusion oncogene; All-Trans Retinoic Acid (ATRA) combined with Arsenic Trioxide (ATO)", True, None),
            ("t(9;22)(q34;q11) generating the BCR-ABL1 fusion tyrosine kinase; Imatinib mesylate monotherapy", False, "t(9;22) is the Philadelphia chromosome characteristic of Chronic Myeloid Leukemia (CML) and precursor B-ALL, not APL with Faggot cells."),
            ("t(8;21)(q22;q22) generating the RUNX1-RUNX1T1 fusion; Intensive high-dose Cytarabine consolidation", False, "t(8;21) is AML M2 with maturation, which does not present with faggot cells or severe life-threatening DIC."),
            ("inv(16)(p13q22) generating CBFB-MYH11; Etoposide and Daunorubicin induction", False, "inv(16) is Acute Myelomonocytic Leukemia with abnormal eosinophils (AML M4Eo).")
        ],
        "pearl": "Acute Promyelocytic Leukemia (APL / AML M3): Cytogenetics: Reciprocal balanced translocation t(15;17)(q24;q21). Pathophysiology: Fuses the Promyelocytic Leukemia (PML) gene on chromosome 15 to the Retinoic Acid Receptor Alpha (RARA) gene on chromosome 17 &rarr; PML-RARA FUSION PROTEIN. This chimeric protein acts as a dominant negative repressor, blocking myeloid differentiation at the promyelocyte stage! Morphology: Promyelocytes packed with dense azurophilic granules and BUNDLES OF AUER RODS ('FAGGOT CELLS'). Major Emergency Complication: FULMINANT DISSEMINATED INTRAVASCULAR COAGULATION (DIC) triggered by the release of procoagulant tissue-factor granules and annexin II from neoplastic promyelocytes. TARGETED DIFFERENTIATION THERAPY: ALL-TRANS RETINOIC ACID (ATRA / Tretinoin) + ARSENIC TRIOXIDE (ATO). Mechanism: Pharmacologic doses of ATRA dissociate corepressors and induce degradation of PML-RARA, forcing malignant promyelocytes to differentiate into mature, non-dividing granulocytes! Has converted a previously fatal leukemia into a highly curable malignancy (>95% cure without conventional cytotoxic chemotherapy).",
        "citation": "Robbins & Cotran Pathologic Basis of Disease, 10th Ed, Chapter 13 (Diseases of White Blood Cells), p. 598-605; Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "hard"
    },
    {
        "subject": "Pathology",
        "concept_name": "Glomerular Pathology: Nephrotic vs Nephritic Syndromes on Light & EM",
        "stem": (
            "A 4-year-old boy presents with sudden-onset generalized puffy facial edema (periorbital swelling on waking) and abdominal distension "
            "(ascites). Urinalysis reveals 4+ proteinuria (protein-to-creatinine ratio 8.2 mg/mg) without hematuria or red cell casts. "
            "Serum albumin is 1.8 g/dL and total serum cholesterol is 420 mg/dL. Renal function and complement C3 levels are normal. "
            "Light microscopy of a renal biopsy appears completely normal. Immunofluorescence is negative for immune deposits. "
            "Electron microscopy (EM) reveals which pathognomonic ultrastructural finding?"
        ),
        "options": [
            ("Diffuse, uniform effacement (flattening and retraction) of visceral epithelial cell foot processes (podocytes)", True, None),
            ("Subepithelial electron-dense deposits forming a 'Spike-and-Dome' pattern on the glomerular basement membrane", False, "'Spike-and-dome' subepithelial deposits are pathognomonic for Membranous Nephropathy, seen typically in adults with anti-PLA2R antibodies."),
            ("Large subepithelial electron-dense 'Humps' concentrated on the epithelial side of the basement membrane", False, "Subepithelial humps are characteristic of Post-Streptococcal Glomerulonephritis (PSGN), presenting with nephritic hematuria and low C3."),
            ("Splitting and duplication of the glomerular basement membrane producing a 'Tram-Track' appearance", False, "'Tram-track' double contour is diagnostic of Membranoproliferative Glomerulonephritis (MPGN).")
        ],
        "pearl": "Glomerular Ultrastructure & Nephrotic Disease Master Table: 1. MINIMAL CHANGE DISEASE (MCD / Lipoid Nephrosis): Epidemiology: Most common cause of nephrotic syndrome in children (~80-90%, peak 2-6 years). Triad: Massive SELECTIVE proteinuria (mainly albumin) + Severe Hypoalbuminemia + Hyperlipidemia & Edema. Light Microscopy: NORMAL glomeruli (hence 'minimal change'; lipid accumulation in tubular cells = lipoid nephrosis). Immunofluorescence: NEGATIVE (no immune complexes). Electron Microscopy (EM): DIFFUSE EFFACEMENT OF PODOCYTE FOOT PROCESSES. Excellent response to oral Corticosteroids (>90% complete remission!). 2. MEMBRANOUS NEPHROPATHY: Most common primary nephrotic syndrome in Caucasian adults. Pathogenesis: Antibodies against Phospholipase A2 Receptor (anti-PLA2R, ~70-80%). Silver stain: 'SPIKE-AND-DOME' pattern. EM: Subepithelial immune deposits. IF: Granular IgG and C3 along capillary loops. 3. POST-STREPTOCOCCAL GN (PSGN): Acute nephritic syndrome 1-4 weeks after streptococcal pharyngitis/impetigo. Low C3. EM: LARGE SUBEPITHELIAL 'HUMPS'. IF: 'Lumpy-bumpy' / 'starry-sky' coarse granular deposits.",
        "citation": "Robbins & Cotran Pathologic Basis of Disease, 10th Ed, Chapter 20 (The Kidney), p. 910-928; Harsh Mohan Pathology, 8th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Pathology",
        "concept_name": "Amyloidosis: Classification, Special Stains & Birefringence",
        "stem": (
            "A 68-year-old male with long-standing refractory Multiple Myeloma develops progressive exertional dyspnea, macroglossia "
            "(grossly enlarged tongue with lateral teeth indentations), and bilateral carpal tunnel syndrome. Echocardiography demonstrates "
            "symmetrical concentric biventricular thickening with a speckled, granular 'sparkling' myocardial texture and restrictive diastolic filling. "
            "An abdominal subcutaneous fat pad aspirate is stained with alkaline Congo Red dye. "
            "Under polarized light microscopy, what diagnostic optical phenomenon will be observed?"
        ),
        "options": [
            ("Characteristic Apple-Green Birefringence", True, None),
            ("Intense canary-yellow fluorescence under ultraviolet excitation", False, "Thioflavin T/S produces yellow-green fluorescence, but Congo red under polarized light produces apple-green birefringence."),
            ("Dark Prussian blue cytoplasmic granular precipitation", False, "Prussian blue stains ferric iron in hemosiderosis and hemochromatosis, not amyloid fibrils."),
            ("Magenta-red metachromasia under brightfield transillumination", False, "Methyl violet and crystal violet give metachromatic pink-purple staining, but polarising microscopy with Congo red gives apple-green birefringence.")
        ],
        "pearl": "Amyloidosis Classification & Optical Diagnostics: Definition: Extracellular pathological deposition of insoluble, misfolded, non-branching fibrillar protein aggregates (7.5-10 nm diameter) with a continuous beta-pleated sheet conformation. CLASSIFICATION: 1. AL Amyloidosis (Amyloid Light Chain): Most common systemic type. Derived from immunoglobulin light chains (lambda 3:1 over kappa) produced by clonal plasma cells in Multiple Myeloma or MGUS. Classic features: Macroglossia, periorbital 'raccoon-eye' purpura, restrictive cardiomyopathy, nephrotic syndrome. 2. AA Amyloidosis (Amyloid-Associated): Derived from Serum Amyloid A (SAA, acute-phase reactant synthesized by hepatocytes during chronic inflammation: Rheumatoid arthritis, Ankylosing spondylitis, Bronchiectasis, Osteomyelitis). 3. ATTR Amyloidosis (Transthyretin): Senile cardiac amyloidosis (wild-type TTR, elderly men) and Familial Amyloid Polyneuropathy (mutant TTR). DIAGNOSTIC HISTOCHEMISTRY: Congo Red Stain: Stains amyloid pale salmon-pink under standard light microscopy. POLARIZED LIGHT MICROSCOPY: Demonstrates PATHOGNOMONIC APPLE-GREEN BIREFRINGENCE due to the cross-beta sheet quaternary fibrillar architecture!",
        "citation": "Robbins & Cotran Pathologic Basis of Disease, 10th Ed, Chapter 6 (Diseases of the Immune System), p. 254-261; Harsh Mohan Pathology, 8th Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Pathology",
        "concept_name": "Diagnostic Immunohistochemistry: Cytokeratins, Vimentin & Neuroendocrine Markers",
        "stem": (
            "A 55-year-old heavy smoker presents with hemoptysis, superior vena cava obstruction syndrome, and extensive mediastinal lymphadenopathy. "
            "Bronchoscopic biopsy of a peribronchial mass reveals sheets of small, round-to-oval cells with scant cytoplasm, ill-defined cell borders, "
            "finely granular 'salt-and-pepper' chromatin, absent nucleoli, frequent mitoses, and marked crush artifact with perivascular DNA encrustation (Azzopardi effect). "
            "Which panel of immunohistochemical (IHC) markers will confirm the neuroendocrine lineage of this tumor (Small Cell Lung Carcinoma)?"
        ),
        "options": [
            ("Synaptophysin positive, Chromogranin A positive, and CD56 (NCAM) positive", True, None),
            ("Desmin positive, Myogenin positive, and MyoD1 positive", False, "Desmin, myogenin, and MyoD1 are skeletal muscle lineage markers diagnostic of Rhabdomyosarcoma."),
            ("Cytokeratin 20 positive and CDX2 positive with negative thyroid transcription factor-1 (TTF-1)", False, "CK20 and CDX2 positivity indicates metastatic colorectal adenocarcinoma, not small cell neuroendocrine carcinoma."),
            ("Leukocyte Common Antigen (LCA / CD45) positive and CD20 positive", False, "LCA (CD45) and CD20 are lymphoid markers diagnostic of B-cell non-Hodgkin lymphoma.")
        ],
        "pearl": "Diagnostic Immunohistochemistry (IHC) Master Guide: 1. EPITHELIAL MARKERS (Carcinomas): Cytokeratins (CK AE1/AE3, CK7, CK20, CAM 5.2), Epithelial Membrane Antigen (EMA). 2. MESENCHYMAL MARKERS (Sarcomas): VIMENTIN (broad mesenchymal marker), DESMIN (smooth and skeletal muscle), SMA (Smooth Muscle Actin), Myogenin & MyoD1 (Rhabdomyosarcoma). 3. NEUROENDOCRINE MARKERS: SYNAPTOPHYSIN, CHROMOGRANIN A, and CD56 (NCAM). Positive in: Small Cell Lung Carcinoma (SCLC), Carcinoid tumors, Pheochromocytoma, Neuroblastoma, Medullary Thyroid Carcinoma, and Pancreatic NETs. (SCLC features dense-core neurosecretory granules on electron microscopy!). 4. HEMATOLYMPHOID MARKERS: Leukocyte Common Antigen (LCA / CD45: all lymphomas), CD20 (B-cells), CD3 (T-cells). 5. MELANOMA & NEURAL CREST: S100, HMB-45 (gp100), Melan-A (MART-1), and SOX10. 6. ENDOTHELIAL / VASCULAR: CD31, CD34, Factor VIII-related antigen.",
        "citation": "Robbins & Cotran Pathologic Basis of Disease, 10th Ed, Chapter 7 (Neoplasia), p. 320-330; Sternberg's Diagnostic Surgical Pathology, 6th Ed.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- MICROBIOLOGY (6 Questions) ---
    # =========================================================================
    {
        "subject": "Microbiology",
        "concept_name": "Gram-Negative Non-Fermenters: Pseudomonas aeruginosa Virulence & Resistance",
        "stem": (
            "A 34-year-old female with extensive 40% thermal burns in the ICU develops high-grade fever, chills, and purulent green-blue discharge "
            "with a distinct sweet, fruity grape-like odor beneath her dressings. Over 24 hours, painless, indurated violaceous maculopapules "
            "erupt on her unburned skin, rapidly evolving into black, central necrotic eschars surrounded by erythematous halos (Ecthyma Gangrenosum). "
            "Blood culture yields an obligate aerobe, Gram-negative, motile bacillus that is Oxidase-positive and non-lactose fermenting on MacConkey agar. "
            "What major bacterial exotoxin mediates tissue necrosis in this infection, and what is its molecular mechanism?"
        ),
        "options": [
            ("Exotoxin A; Inactivates Eukaryotic Elongation Factor-2 (eEF-2) by ADP-ribosylation, arresting host cellular protein synthesis", True, None),
            ("Shiga-like toxin (Verotoxin); Cleaves the 28S rRNA of the 60S eukaryotic ribosomal subunit", False, "Shiga toxin cleaves 28S rRNA, produced by Shigella dysenteriae and EHEC/STEC O157:H7."),
            ("Alpha-toxin (Lecithinase); Hydrolyzes sphingomyelin and phosphatidylcholine causing membrane lysis", False, "Lecithinase alpha-toxin is produced by Clostridium perfringens, causing gas gangrene and myonecrosis."),
            ("Endotoxin Lipid A; Direct enzymatic phosphorylation of vascular endothelial cadherins", False, "Lipid A acts via TLR-4 triggering TNF-alpha and IL-1 release; Exotoxin A is the specific ADP-ribosylating toxin.")
        ],
        "pearl": "Pseudomonas aeruginosa Virulence & Clinical Syndromes: Microbiology: Gram-negative motile bacillus, obligate aerobe, non-lactose fermenter, Oxidase POSITIVE (distinguishes from Enterobacteriaceae which are oxidase negative!), Catalase positive. Pigments: PYOCYANIN (blue-green, generates reactive oxygen species) and PYOVERDINE (yellow-green, fluorescent siderophore). Classic fruity / grape-like odor (due to 2-aminoacetophenone). VIRULENCE ARSENAL: 1. EXOTOXIN A: Major virulence factor! Exactly identical mechanism to Diphtheria toxin &mdash; ADP-ribosylates Elongation Factor-2 (eEF-2), halting host cell protein synthesis and causing cell death! 2. Alginate Exopolysaccharide Biofilm: Protects against phagocytosis and antibiotics in Cystic Fibrosis lungs! 3. Elastase (LasB): Degrades elastin in blood vessel walls &rarr; ECTHYMA GANGRENOSUM (pathognomonic hemorrhagic bullae with black necrotic eschar resulting from perivascular bacterial invasion and vascular thrombosis!). High-yield antipseudomonal agents: Piperacillin-tazobactam, Cefepime, Ceftazidime, Meropenem, Ciprofloxacin, Tobramycin, Colistin.",
        "citation": "Ananthanarayan and Paniker's Textbook of Microbiology, 11th Ed, Chapter 38; Jawetz Medical Microbiology, 28th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Microbiology",
        "concept_name": "Anaerobic Spore-Forming Bacilli: Clostridioides difficile Colitis & Toxins",
        "stem": (
            "A 65-year-old male receives a 14-day course of intravenous Clindamycin and Ceftriaxone for a diabetic foot osteomyelitis. "
            "On day 10, he develops 10-12 episodes per day of watery, foul-smelling diarrhea, crampy lower abdominal pain, low-grade fever, "
            "and severe leukocytosis (WBC 28,500/mcL). Flexible sigmoidoscopy reveals numerous raised, punctate, yellowish-white mucosal plaques "
            "coalescing into pseudomembranes over an erythematous, friable colonic mucosa. "
            "What are the two major exotoxins produced by this pathogen, and what is the current FIRST-LINE guideline treatment?"
        ),
        "options": [
            ("Toxin A (Enterotoxin damaging mucosal brush border) and Toxin B (Cytotoxin depolymerizing filamentous actin via Rho-GTPase glucosylation); Oral Fidaxomicin (or Oral Vancomycin)", True, None),
            ("Exfoliative Toxin A and B; Intravenous high-dose Ampicillin-Sulbactam", False, "Exfoliative toxins cause Staphylococcal Scalded Skin Syndrome, not pseudomembranous colitis."),
            ("Tetanospasmin and Tetanolysin; Intramuscular Metronidazole monotherapy", False, "Tetanospasmin is produced by C. tetani. Oral metronidazole is no longer first-line for C. difficile due to inferior cure and higher relapse rates."),
            ("Alpha-toxin and Theta-toxin; Intravenous Ciprofloxacin and Doxycycline", False, "Fluoroquinolones are common triggers for C. difficile (especially the hypervirulent BI/NAP1/027 ribotype).")
        ],
        "pearl": "Clostridioides (Clostridium) difficile Colitis: Pathogenesis: Spore-forming, obligate anaerobic Gram-positive bacillus. Broad-spectrum antibiotics (Clindamycin, Fluoroquinolones, 2nd/3rd gen Cephalosporins) disrupt normal gut microbiota &rarr; C. difficile spores germinate &rarr; produce two potent exotoxins: 1. TOXIN A (Enterotoxin): Binds brush border membranes, causes neutrophil chemotaxis, fluid secretion, and mucosal inflammation. 2. TOXIN B (Cytotoxin): 10-fold more potent than Toxin A! Glucosylates and inactivates small Rho-family GTPases (Rho, Rac, Cdc42), causing DISRUPTION OF CYTOSKELETON (ACTIN DEPOLYMERIZATION), loss of tight junctions, and cell apoptosis. HISTOPATHOLOGY: 'Volcano' or 'mushroom' shaped mucosal lesions composed of fibrinopurulent exudate, necrotic epithelial cells, and neutrophils erupting onto mucosal surface (PSEUDOMEMBRANE). GUIDELINE TREATMENT OF CHOICE (IDSA/SHEA): 1. ORAL FIDAXOMICIN (200 mg BID for 10 days, macrocyclic antibiotic inhibiting RNA polymerase) OR 2. ORAL VANCOMYCIN (125 mg QID for 10 days). (Note: Oral Metronidazole is NO LONGER FIRST-LINE!). Severe refractory/recurrent cases: Fecal Microbiota Transplantation (FMT) or Bezlotoxumab (anti-toxin B mAb).",
        "citation": "IDSA/SHEA Focused Update on Clostridioides difficile Infection in Adults 2021; Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Microbiology",
        "concept_name": "Medical Parasitology: Malaria Speciation, Gametocytes & Hypnozoite Eradication",
        "stem": (
            "A 30-year-old traveler returns from a rural agricultural area with tertian fever (paroxysms recurring every 48 hours), shaking chills, "
            "and profuse drenching sweats. Giemsa-stained thick and thin blood smears demonstrate enlarged, pale, parasitized erythrocytes "
            "containing fine pinkish-red cytoplasmic stippling (Schüffner's dots), amoeboid trophozoites, and round, compact gametocytes. "
            "Blood smear for Plasmodium falciparum is negative. "
            "What species is responsible, and which pharmacological agent is MANDATORY to eliminate the dormant liver hypnozoites and prevent relapse?"
        ),
        "options": [
            ("Plasmodium vivax; Primaquine (or Tafenoquine) for 14 days after ruling out G6PD deficiency", True, None),
            ("Plasmodium falciparum; Artemether-Lumefantrine for 3 days", False, "P. falciparum has crescent-shaped gametocytes, Maurer's dots, infects RBCs of all ages, and DOES NOT HAVE DORMANT LIVER HYPNOZOITES."),
            ("Plasmodium malariae; Chloroquine monotherapy for 3 days without tissue schizonticides", False, "P. malariae has a 72-hour quartan cycle, Ziemann's dots, band-form trophozoites, and lacks hypnozoites."),
            ("Plasmodium ovale; Intravenous Artesunate followed by Mefloquine", False, "P. ovale features oval RBCs with fimbriated ragged borders and James dots, and intravenous artesunate is reserved for severe complicated malaria.")
        ],
        "pearl": "Malaria Species Comparison Master Table: 1. PLASMODIUM VIVAX: Red blood cells: Invades RETICULOCYTES (young RBCs only); parasitized RBCs are ENLARGED and pale. Stippling: SCHÜFFNER'S DOTS. Trophozoite: Irregular, AM举报EBOID. Gametocytes: Round/oval. Fever periodicity: Benign Tertian (48 hrs). DORMANT LIVER STAGE: HYPNOZOITES! (Persist in hepatocytes for months/years &rarr; cause RELAPSE!). Anti-relapse therapy: PRIMAQUINE (0.25-0.5 mg/kg daily for 14 days) or TAFENOQUINE. CRITICAL SAFETY RULE: MUST SCREEN FOR G6PD DEFICIENCY BEFORE PRESCRIBING PRIMAQUINE/TAFENOQUINE (causes massive acute intravascular hemolysis!). 2. PLASMODIUM FALCIPARUM: Red blood cells: Invades ALL ERYTHROCYTES of any age (causes heavy, lethal parasitemia >5%). Stippling: MAURER'S CLEFTS. Smear features: MULTIPLE delicate ring forms per RBC, ACCOLÉ / APPLIQUÉ marginal forms, and CRESCENT / BANANA-SHAPED GAMETOCYTES. NO hypnozoites (causes RECRUDESCENCE due to sub-patent erythrocytic cycle, NOT relapse!). Virulence mechanism: PfEMP-1 knobs adhere to CD36 and ICAM-1 &rarr; microvascular sequestration &rarr; CEREBRAL MALARIA, Blackwater fever, ARDS, and acute renal failure.",
        "citation": "Ananthanarayan and Paniker's Textbook of Microbiology, 11th Ed, Chapter 45 (Malaria); WHO Malaria Guidelines 2023.",
        "difficulty": "medium"
    },
    {
        "subject": "Microbiology",
        "concept_name": "Diagnostic Virology: Hepatitis B Serological Profile & Window Period",
        "stem": (
            "A 24-year-old healthcare worker sustains a needlestick injury from a known hepatitis B carrier. Baseline viral serology is drawn. "
            "Her results show: HBsAg is NEGATIVE, Anti-HBs is NEGATIVE, HBeAg is NEGATIVE, Anti-HBe is POSITIVE, "
            "and Anti-HBc IgM is STRONGLY POSITIVE. "
            "In what stage of Hepatitis B virus infection is this healthcare worker, and what is the clinical significance of this serological profile?"
        ),
        "options": [
            ("The 'Window Period' (Core Window) of acute Hepatitis B infection; Anti-HBc IgM is the sole serological marker of active infection when HBsAg has disappeared but Anti-HBs has not yet risen to detectable levels", True, None),
            ("Successful immunization with recombinant Hepatitis B vaccine", False, "Vaccine-induced immunity produces Anti-HBs ONLY; Anti-HBc is an antibody against internal core protein, produced exclusively by natural infection!"),
            ("Chronic inactive carrier state with viral clearance", False, "Chronic carriage is defined by persistence of HBsAg for >6 months and Anti-HBc IgG, not acute Anti-HBc IgM."),
            ("Occult Hepatitis B infection with mutant S gene escape", False, "The window period is the classic textbook explanation for HBsAg negative with isolated Anti-HBc IgM positivity.")
        ],
        "pearl": "Hepatitis B Virus (HBV) Serological Markers Guide: 1. HBsAg (Surface Antigen): Earliest marker to appear in acute infection (1-6 weeks). Persistence >6 months defines CHRONIC HBV INFECTION! 2. Anti-HBs (Surface Antibody): Neutralizing protective antibody. Appears after clearance of HBsAg. Indicates IMMUNITY. Sole positive marker in VACCINATED INDIVIDUALS! 3. HBeAg (Envelope Antigen): Marker of active viral replication, high infectivity, and transmission risk. 4. Anti-HBe: Indicates seroconversion, decreased viral replication, and lower infectivity. 5. Anti-HBc IgM: First antibody to appear against the nucleocapsid core. MARKS ACUTE INFECTION! 6. THE 'WINDOW PERIOD' (Core Window): The temporal gap between the disappearance of HBsAg and the appearance of protective Anti-HBs. During this window, HBsAg is negative and Anti-HBs is negative. THE ONLY DETECTABLE SEROLOGICAL MARKER OF INFECTION DURING THE WINDOW PERIOD IS ANTI-HBc IgM! (Screening blood donations with HBsAg alone misses window-period blood; HBV DNA NAT testing prevents this). 7. Anti-HBc IgG: Persists for life after NATURAL infection. (Absent after vaccination).",
        "citation": "Ananthanarayan and Paniker's Textbook of Microbiology, 11th Ed, Chapter 56 (Hepatitis Viruses); Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Microbiology",
        "concept_name": "Medical Mycology: Thermal Dimorphism & Histoplasmosis vs Cryptococcus",
        "stem": (
            "A 42-year-old spelunker (cave explorer) presents with subacute fever, non-productive cough, chest pain, and weight loss 3 weeks "
            "after exploring bat-inhabited caves. Chest CT reveals bilateral reticulonodular infiltrates with mediastinal and hilar lymphadenopathy. "
            "Bone marrow aspirate and bronchoalveolar lavage reveal tiny, oval, intracellular yeast cells measuring 2 to 4 mcm packed tightly "
            "within the cytoplasm of histiocytes and alveolar macrophages. Each yeast cell demonstrates narrow-based single budding with a "
            "pseudo-halo (shrinkage artifact). On Sabouraud's Dextrose Agar at 25°C, it grows as a white-brown mold producing large, "
            "spherical, tuberculate macroconidia with thick finger-like projections. "
            "What is the pathogen, and what defines its thermal dimorphism?"
        ),
        "options": [
            ("Histoplasma capsulatum; Exists as a mycelial mold producing tuberculate macroconidia at 25°C in soil/guano, but transitions into an intracellular budding yeast at 37°C in host tissues", True, None),
            ("Blastomyces dermatitidis; Broad-based single budding yeast with thick double-contoured walls at both temperatures", False, "Blastomyces forms large (8-15 mcm) yeasts with broad-based budding and a refractile double-contoured cell wall."),
            ("Cryptococcus neoformans; Monomorphic encapsulated yeast surrounded by a thick polysaccharide capsule visible on India ink", False, "Cryptococcus is monomorphic (always yeast, never mold), encapsulated, stained by India ink and mucicarmine."),
            ("Coccidioides immitis; Endospore-filled thick-walled spherules at 37°C and barrel-shaped arthroconidia at 25°C", False, "Coccidioides produces massive 20-100 mcm spherules containing endospores, not tiny intracellular yeasts within macrophages.")
        ],
        "pearl": "Systemic Dimorphic Fungi Master Table: Thermal Dimorphism Rule: 'MOLD IN THE COLD (25°C, environmental saprophytic phase) &rarr; YEAST IN THE BEAST (37°C, host tissue parasitic phase)'. 1. HISTOPLASMA CAPSULATUM: Habitat: Soil contaminated with BIRD OR BAT GUANO (caves, chicken coops, spelunking!). Endemic in Ohio and Mississippi River valleys, and Gangetic plains in India. Tissue form (37°C): TINY INTRACELLULAR YEASTS (2-4 mcm) PACKED INSIDE MACROPHAGES with narrow-based budding (no true capsule; halo is fixation artifact!). Culture form (25°C): TUBERCULATE MACROCONIDIA (thick-walled with finger-like projections). Target organ: Reticuloendothelial system (hepatosplenomegaly, pancytopenia, adrenal enlargement). 2. BLASTOMYCES DERMATITIDIS: BROAD-BASED BUDDING YEAST (size matches bud; thick refractile double wall). 3. COCCIDIOIDES IMMITIS: Arthroconidia at 25°C &rarr; LARGE SPHERULES FILLED WITH ENDOSPORES (20-100 mcm) at 37°C! (Desert Southwest US). 4. PARACOCCIDIOIDES BRASILIENSIS: Multiple budding yeasts resembling 'MARINER'S / CAPTAIN'S WHEEL' or 'Mickey Mouse ears'. (Latin America).",
        "citation": "Ananthanarayan and Paniker's Textbook of Microbiology, 11th Ed, Chapter 61 (Medical Mycology); Jawetz Medical Microbiology, 28th Ed.",
        "difficulty": "hard"
    },
    {
        "subject": "Microbiology",
        "concept_name": "Clinical Virology: HIV Replication Cycle & Opportunistic Prophylaxis Thresholds",
        "stem": (
            "A 36-year-old male with untreated HIV infection presents with progressive exertional dyspnea, dry non-productive cough, and fever "
            "for 3 weeks. His CD4+ T-cell count is 110 cells/mcL. Arterial blood gas on room air shows: pH 7.46, PaO2 54 mmHg (marked hypoxemia), "
            "and PaCO2 31 mmHg. Chest radiograph demonstrates diffuse bilateral symmetric perihilar ground-glass interstitial infiltrates. "
            "Induced sputum stained with Gomori Methenamine Silver (GMS) demonstrates cup-shaped, crushed ping-pong ball cysts with central dark spots. "
            "What is the organism, the first-line treatment of choice, and the mandatory adjuvant therapy indicated for his PaO2 level?"
        ),
        "options": [
            ("Pneumocystis jirovecii; Intravenous Trimethoprim-Sulfamethoxazole (TMP-SMX) PLUS adjuvant systemic Corticosteroids (Prednisone)", True, None),
            ("Mycobacterium avium complex (MAC); Clarithromycin plus Ethambutol", False, "MAC presents with fever, night sweats, diarrhea, and weight loss in patients with CD4 <50 cells/mcL, treated with macrolides."),
            ("Cytomegalovirus (CMV) pneumonitis; Intravenous Ganciclovir monotherapy", False, "CMV pneumonitis shows intranuclear 'owl's-eye' inclusion bodies, seen at CD4 <50 cells/mcL."),
            ("Cryptococcus neoformans; Liposomal Amphotericin B plus Flucytosine", False, "Cryptococcus causes subacute meningitis with gelatinous pseudocysts, not classic cup-shaped GMS cysts in pulmonary alveoli.")
        ],
        "pearl": "Pneumocystis jirovecii Pneumonia (PCP) & HIV Opportunistic Timeline: Microbiology: Atypical unicellular fungus (formerly P. carinii). Lacks ergosterol in cell membrane (cholesterol instead; resistant to amphotericin B and azoles!). Silver stain (GMS): CUP-SHAPED or CRUSHED PING-PONG BALL CYSTS with central dark bracket. High-yield marker: Elevated Serum 1,3-beta-D-Glucan and LDH. CD4 THRESHOLD TIMELINE FOR PROPHYLAXIS: 1. CD4 < 200 cells/mcL (or oral candidiasis): PNEUMOCYSTIS JIROVECII. Primary Prophylaxis: Oral TMP-SMX (double strength daily). 2. CD4 < 100 cells/mcL (and positive IgG): TOXOPLASMA GONDII. Prophylaxis: Oral TMP-SMX (also covers PCP!). 3. CD4 < 50 cells/mcL: MYCOBACTERIUM AVIUM COMPLEX (MAC). Prophylaxis: Azithromycin 1200 mg weekly (if not on ART). TREATMENT OF ACTIVE PCP: 1. Drug of choice: High-dose IV Trimethoprim-Sulfamethoxazole (TMP 15-20 mg/kg/day + SMX 75-100 mg/kg/day) for 21 days. 2. ADJUVANT CORTICOSTEROIDS: INDICATED IF PaO2 < 70 mmHg on room air OR Alveolar-arterial (A-a) gradient &ge; 35 mmHg! (Significantly reduces mortality and prevents early respiratory deterioration from inflammatory lysis).",
        "citation": "CDC/NIH/HIVMA Guidelines for the Prevention and Treatment of Opportunistic Infections in Adults with HIV 2023; Harrison's Internal Medicine, 21st Ed.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- FORENSIC MEDICINE (6 Questions) ---
    # =========================================================================
    {
        "subject": "Forensic Medicine",
        "concept_name": "Mechanical Injuries: Firearm Ballistics & Entry vs Exit Wounds",
        "stem": (
            "A medicolegal autopsy is conducted on a 30-year-old male who sustained a gunshot injury to the chest. "
            "Examination of the entry wound reveals a circular skin defect with inverted margins, surrounded by a narrow concentric rim of "
            "epidermal stripping and contusion (abrasion and contusion collar) and a dark ring of lubricant and barrel grease (grease/dirt collar). "
            "Importantly, there is NO flame burn, NO hair singeing, and NO particulate unburned gunpowder grains embedded into the dermis (NO tattooing/stippling). "
            "Based on wound ballistics, what was the range of firing, and what differentiates tattooing from soot deposition?"
        ),
        "options": [
            ("Distant / Far range (>2 to 3 feet); Tattooing is the permanent mechanical embedding of unburnt gunpowder particles into the dermis that cannot be washed off with water, unlike superficial soot which washes off easily", True, None),
            ("Hard Contact wound; Muzzle impression stamp on the bone", False, "Hard contact wounds feature a muzzle impression stamp, star-shaped lacerated tears from expanding gases, and bright red carboxyhemoglobin in tissue."),
            ("Close range within 6 inches; Singeing of skin hairs by burning muzzle flash", False, "Close range features burning, singeing, and dense superficial soot deposition around the wound."),
            ("Intermediate range (6 to 24 inches); Microscopic stippling confined to the stratum corneum", False, "Intermediate range is characterized specifically by prominent tattooing / stippling; its complete absence defines a distant wound.")
        ],
        "pearl": "Firearm Wound Ballistics & Range of Firing: 1. CONTACT WOUND: Weapon held firmly against skin. Characteristics: Muzzle impression / stamp on skin. Expanding muzzle gases enter subcutaneous plane and rebound against underlying flat bone &rarr; STELLATE / STAR-SHAPED lacerated wound edges. Cherry-red tissue coloration beneath wound due to CARBOXYHEMOGLOBIN formation from carbon monoxide. 2. CLOSE RANGE (Within 6 to 12 inches): (A) Flame burn / singeing of hair (within 2-6 inches) | (B) Blackening / Soot deposition: Amorphous carbon smoke deposits superficially on skin; CAN BE WASHED OFF with wet sponge or water! 3. INTERMEDIATE RANGE (1 to 3 feet): TATTOOING / STIPPLING: Unburnt and partially burnt gunpowder flakes accelerate like tiny missiles, penetrating into the viable epidermis and DERMIS. CANNOT BE WASHED OFF! (True ante-mortem vital reaction). 4. DISTANT RANGE (>3 feet): Bullet travels alone; flame, soot, and powder disperse before reaching victim. ONLY features: Circular entry defect + ABRASION COLLAR (loss of epithelium from spinning bullet) + GREASE / DIRT COLLAR (bullet wipe). (Inverted margins for entry vs Everted ragged margins for exit!).",
        "citation": "Reddy's Essentials of Forensic Medicine and Toxicology, 34th Ed, Chapter 11 (Firearm Injuries), p. 210-230; Parikh's Textbook of Medical Jurisprudence.",
        "difficulty": "medium"
    },
    {
        "subject": "Forensic Medicine",
        "concept_name": "Clinical & Forensic Toxicology: Organophosphate Poisoning & Aging of Enzyme",
        "stem": (
            "A 32-year-old agricultural worker is brought to the casualty 4 hours after accidentally spilling an undiluted organophosphate "
            "insecticide (Malathion) over his bare skin and inhaling the aerosol. He is comatose, salivating excessively, and incontinent of urine and feces. "
            "Examination reveals pinpoint, non-reactive pupils, diffuse coarse bilateral crackles throughout all lung fields ('pulmonary edema / drowning in own secretions'), "
            "heart rate 42 bpm, and generalized fasciculations of the tongue, face, and calf muscles. "
            "What is the pharmacological mechanism of PRALIDOXIME (2-PAM), and why must it be administered before 'aging' of the phosphorylated enzyme occurs?"
        ),
        "options": [
            ("Pralidoxime acts as a nucleophilic reactivator that breaks the organophosphate-acetylcholinesterase ester bond; 'aging' involves non-enzymatic loss of an alkyl group from the phosphorylated enzyme, rendering it permanently resistant to chemical reactivation", True, None),
            ("Pralidoxime directly blocks postsynaptic muscarinic acetylcholine receptors like atropine", False, "Pralidoxime is an oxime reactivator of acetylcholinesterase at nicotinic sites; atropine blocks muscarinic receptors."),
            ("Pralidoxime accelerates the renal elimination of intact malathion molecules", False, "Pralidoxime works by chemical dephosphorylation of acetylcholinesterase, not by promoting renal clearance."),
            ("Aging represents the oxidative transformation of malathion into malaoxon in hepatic microsomes", False, "Oxidative activation to malaoxon occurs earlier in the liver; 'aging' refers specifically to conformational dealkylation of the phosphorylated AChE enzyme.")
        ],
        "pearl": "Organophosphate Poisoning & The 'Aging' Phenomenon: Mechanism: Organophosphates (OP compounds: Malathion, Diazinon, Chlorpyrifos) phosphorylate the esteratic site of ACETYLCHOLINESTERASE (AChE), causing irreversible enzyme inhibition and massive accumulation of ACETYLCHOLINE at: 1. Muscarinic synapses: SLUDGEM (Salivation, Lacrimation, Urination, Defecation, GI cramps, Emesis, Miosis) + Bronchorrhea and Bronchospasm ('killer B's'). 2. Nicotinic synapses: Fasciculations, muscle twitching, weakness, and diaphragmatic respiratory paralysis! 3. CNS: Coma, seizures, respiratory depression. TREATMENT CORNERSTONES: 1. ATROPINE: Competitive muscarinic receptor antagonist. Reverses life-threatening bronchorrhea, bronchospasm, and bradycardia! DOSE TITRATION ENDPOINTS: DRY BRONCHIAL SECRETIONS (clear lung fields on auscultation), heart rate >80 bpm, and dry axillae (NOT pupillary dilation!). 2. PRALIDOXIME (2-PAM) / OXIMES: Nucleophilic agent that attacks the phosphorylated serine residue, freeing the active enzyme. MUST BE GIVEN EARLY BEFORE 'AGING': Aging is the non-enzymatic spontaneous cleavage of an alkyl side chain from the phosphorylated enzyme over 24-48 hours, leaving a negatively charged phosphate that cannot be attacked by oximes (permanent chemical inactivation!).",
        "citation": "Reddy's Essentials of Forensic Medicine and Toxicology, 34th Ed, Chapter 27 (Agrochemical Poisons), p. 485-498; Goldfrank's Toxicologic Emergencies, 11th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Forensic Medicine",
        "concept_name": "Asphyxial Deaths: Hanging vs Strangulation & Post-Mortem Signs",
        "stem": (
            "During a medicolegal post-mortem examination of an asphyxial death, the forensic pathologist observes the following neck findings: "
            "A ligature mark that is completely CONTINUOUS, encircling the neck horizontally at the level of the lower border of the thyroid cartilage "
            "and cricoid cartilage, with uniform depth throughout its circumference. There are extensive petechial hemorrhages (Tardieu spots) in the "
            "conjunctivae and facial skin, marked venous congestion above the neck mark, and a bilateral transverse fracture of the thyroid cartilage horns. "
            "What is the mode of death indicated by these findings?"
        ),
        "options": [
            ("Ligature Strangulation (Homicidal until proven otherwise)", True, None),
            ("Ante-mortem Judicial Hanging (Suicidal hanging)", False, "Hanging produces an OBLIQUE, NON-CONTINUOUS ligature mark placed HIGH in the neck above the thyroid cartilage, with apex at the suspension knot."),
            ("Post-mortem suspension of a dead body (Simulated hanging)", False, "Post-mortem suspension shows zero vital reaction, no subcutaneous extravasation of blood, and no intimal tears in carotid arteries."),
            ("Traumatic asphyxia (Burking) without neck compression", False, "Burking combines chest compression (overlaying) with occlusion of mouth and nostrils, lacking a circular continuous ligature mark.")
        ],
        "pearl": "Hanging vs Ligature Strangulation Master Table: 1. HANGING (Typically Suicidal): Ligature Mark: OBLIQUE, NON-CONTINUOUS (incomplete circle; deficient at the site of knot / nape of neck). Level: HIGH in the neck (ABOVE the thyroid cartilage, between larynx and chin). Base of mark: Pale, hard, dry, grooved, 'parchment-like' with inverted edges. Laryngeal fractures: Rare in young individuals (hyoid fracture occurs in ~15-20% of elderly hanging). Bleeding in neck muscles: Minimal or absent. Carotid Intimal Tears: Amussat's sign (transverse intimal tears of common carotids). 2. LIGATURE STRANGULATION (Typically Homicidal): Ligature Mark: HORIZONTAL, COMPLETELY CONTINUOUS (complete unbroken ring encircling entire neck). Level: LOW in the neck (AT or BELOW the thyroid cartilage). Base of mark: Soft, reddish, congested, often with ecchymoses and fingernail scratches from struggle. Petechial Hemorrhages: ABUNDANT and prominent in conjunctivae, eyelids, and facial skin (due to prolonged venous obstruction). Laryngeal fractures: COMMON (thyroid cartilage horns and cricoid cartilage fractured by direct transverse crushing force).",
        "citation": "Reddy's Essentials of Forensic Medicine and Toxicology, 34th Ed, Chapter 14 (Asphyxial Deaths), p. 305-328; Modi's Medical Jurisprudence.",
        "difficulty": "easy"
    },
    {
        "subject": "Forensic Medicine",
        "concept_name": "Post-Mortem Changes: Algor, Rigor & Livor Mortis Stages & Fixation",
        "stem": (
            "A body is discovered in a locked apartment with an ambient temperature of 22°C. On examination at 8:00 AM, the forensic officer "
            "notes that post-mortem lividity (hypostasis) is dark purplish-blue and distributed over the dependent dorsal aspects of the back, "
            "buttocks, and calves, but blenches completely when firm digital pressure is applied with the thumb. "
            "Rigor mortis is well-established in the jaw and neck muscles, but the limbs remain flaccid. "
            "What is the estimated time since death (post-mortem interval), and what does the blanching of lividity signify?"
        ),
        "options": [
            ("Time since death is approximately 3 to 6 hours; Lividity is not yet 'fixed' because blood remains uncoagulated within capillary vessels and has not yet hemolyzed or diffused into the extravascular dermis", True, None),
            ("Time since death is greater than 18 to 24 hours; Blanching indicates secondary muscular flaccidity", False, "After 18-24 hours, lividity is completely fixed and does not blanch, and rigor mortis would be passing off."),
            ("Time since death is less than 30 minutes; Blanching is caused by active arteriolar vasoconstriction", False, "Lividity takes at least 1-2 hours to become visibly apparent; it does not appear within 30 minutes."),
            ("Time since death is exactly 12 hours; Rigor mortis is fully set in all voluntary and involuntary muscle groups", False, "Rigor mortis progresses according to Nysten's law from jaw down to limbs; presence in jaw only with flaccid limbs indicates early onset (2-4 hrs).")
        ],
        "pearl": "Post-Mortem Changes & Post-Mortem Interval (PMI): 1. LIVOR MORTIS (Hypostasis / Suggilation): Gravitational pooling of blood in capillaries and venules of dependent, uncompressed parts of the body. Begins: 1 to 2 hours after death. Coalesces into patches: 2 to 4 hours. Digital pressure blanching: BLANCHES EASILY UP TO 6 HOURS (blood is still liquid inside intact vessels). FIXATION OF LIVOR MORTIS: Occurs at 6 to 8 HOURS (hemolysis occurs; hemoglobin stains perivascular dermal tissues &rarr; lividity CANNOT BE BLANCHED and does not shift if body position is altered!). Color variations: Normal: Purplish-blue | Carbon Monoxide: CHERRY-RED (carboxyhemoglobin) | Cyanide: BRIGHT PINK / BRICK-RED | Methemoglobin: CHOCOLATE-BROWN | Refrigeration: Bright pink. 2. RIGOR MORTIS (Post-mortem rigidity): Molecular cause: Loss of ATP production prevents detachment of myosin heads from actin filaments (actin-myosin complex locked). NYSTEN'S LAW (Rule of progression): Involuntary heart &rarr; Eyelids &rarr; Lower jaw &rarr; Neck &rarr; Thorax &rarr; Upper limbs &rarr; Abdomen &rarr; Lower limbs &rarr; Fingers and toes. Rule of 12s in temperate climates: Takes 12 hours to develop, persists for 12 hours, takes 12 hours to pass off (disappears in same order due to autolysis).",
        "citation": "Reddy's Essentials of Forensic Medicine and Toxicology, 34th Ed, Chapter 7 (Post-Mortem Changes), p. 135-160; Parikh's Medical Jurisprudence.",
        "difficulty": "medium"
    },
    {
        "subject": "Forensic Medicine",
        "concept_name": "Forensic Toxicology: Plant Neurotoxins - Datura vs Strychnine",
        "stem": (
            "A 40-year-old traveler on a long-distance night train accepts a sweet peda from a friendly co-passenger. Two hours later, "
            "he is found wandering the train corridor completely disoriented, staggering as if intoxicated, and plucking imaginary threads "
            "from the air and his clothes (carphologia and floccillation). On physical examination, his skin is dry, flushed, and scarlatiniform, "
            "his mouth is parched with an inability to swallow, body temperature is 39.2°C (102.5°F), and pupils are widely dilated, equal, and non-reactive to light. "
            "What plant poison was used as a stupefying agent, and what is the specific pharmacological antidote?"
        ),
        "options": [
            ("Datura stramonium / fastuosa (Dhatura); Physostigmine salicylate (1 to 2 mg slow IV)", True, None),
            ("Strychnos nux-vomica (Strychnine); Intravenous Flumazenil", False, "Strychnine causes spinal tetanic convulsions and risus sardonicus without anticholinergic delirium or mydriasis; flumazenil reverses benzodiazepines."),
            ("Cannabis sativa (Bhang / Ganja); Intramuscular Naloxone", False, "Cannabis produces conjunctival injection, euphoria, and giggling; naloxone reverses opioids."),
            ("Aconitum napellus (Monkshood); High-dose Atropine sulfate", False, "Aconite is a cardiac poison activating voltage-gated sodium channels, causing tingling, numbness, and arrhythmias; atropine worsens anticholinergic toxicity!")
        ],
        "pearl": "Plant Poisons: Datura vs Strychnine: 1. DATURA (Datura fastuosa / D. stramonium - 'Devil's trumpet' / 'Road poison'): Active alkaloids: Hyoscine (Scopolamine), Hyoscyamine, Atropine. Forensic use: STUPEFYING POISON (crushed seeds mixed in food/prasad to rob train travelers). Classic Anticholinergic Mnemonic: 'Blind as a bat' (cycloplegic mydriasis) + 'Mad as a hatter' (delirium, CARPHOLOGIA / picking at bedclothes) + 'Red as a beet' (cutaneous flushing) + 'Hot as a hare' (hyperthermia due to anhidrosis) + 'Dry as a bone' (parched dry mouth). Key differentiating sign: Datura seeds have a double-collared bitter edge and look like chilli seeds (chilli seeds are pungent, yellow, with a single sharp curved edge). SPECIFIC ANTIDOTE: PHYSOSTIGMINE SALICYLATE (tertiary amine that crosses the blood-brain barrier to inhibit acetylcholinesterase and restore central ACh). 2. STRYCHNOS NUX-VOMICA (Strychnine): Active alkaloid: Strychnine. Mechanism: Competitive antagonist of GLYCINE at postsynaptic receptors in spinal cord anterior horn cells. Clinical features: VIOLENT REFLEX SPINAL TETANIC CONVULSIONS triggered by slightest sensory stimulus (sound, light, touch). Characteristic features: RISUS SARDONICUS (spasm of facial muscles) + OPISTHOTONUS (bridging back arch). Patient REMAINS FULLY CONSCIOUS AND EXPERIENCES EXCRUCIATING PAIN until death from asphyxia!",
        "citation": "Reddy's Essentials of Forensic Medicine and Toxicology, 34th Ed, Chapter 30 (Plant Poisons), p. 520-538; Modi's Medical Jurisprudence.",
        "difficulty": "easy"
    },
    {
        "subject": "Forensic Medicine",
        "concept_name": "Medical Jurisprudence: Informed Consent, Bolam Principle & Jacob Mathew Ruling",
        "stem": (
            "A licensed general surgeon performs an elective open cholecystectomy on a 44-year-old male for symptomatic gallstones after "
            "obtaining valid written informed consent. During dissection of Calot's triangle, severe anomalous arterial bleeding is encountered. "
            "The surgeon executes standard hemostatic maneuvers and ligates the bleeding branch in accordance with established surgical principles "
            "practiced by a responsible body of general surgeons. Postoperatively, a small bile leak occurs, requiring ERCP stent placement. "
            "The patient files a criminal negligence lawsuit under the Bharatiya Nyaya Sanhita (formerly Section 304A IPC) alleging gross negligence. "
            "Under the landmark Supreme Court ruling in Jacob Mathew v. State of Punjab and the historic Bolam Principle, which standard determines criminal medical negligence?"
        ),
        "options": [
            ("A medical practitioner cannot be held criminally liable for an error of judgment or unanticipated complication if they acted in accordance with a practice accepted as proper by a responsible body of medical peers; criminal negligence requires 'gross negligence' (mens rea or reckless disregard)", True, None),
            ("Any unexpected postoperative complication or deviation from perfection constitutes prima facie evidence of criminal negligence", False, "The law explicitly distinguishes an error of clinical judgment or adverse complication from culpable criminal negligence."),
            ("The doctrine of Res Ipsa Loquitur automatically applies to all surgical bleeding complications regardless of anatomy", False, "Res ipsa loquitur only applies where obvious non-technical blunders occur (e.g., operating on the wrong leg or leaving a sponge inside)."),
            ("A general surgeon is held to the legal standard of the world's most accomplished laparoscopic hepato-pancreato-biliary authority", False, "The Bolam test measures competence against the ordinary skilled practitioner exercising reasonable skill, not the highest possible specialist.")
        ],
        "pearl": "Medical Negligence & Judicial Doctrines: 1. THE BOLAM PRINCIPLE (Bolam v. Friern Hospital Management Committee, 1957): A doctor is not guilty of negligence if they acted in accordance with a practice ACCEPTED AS PROPER BY A RESPONSIBLE BODY OF MEDICAL MEN SKILLED IN THAT PARTICULAR ART. 2. RES IPSA LOQUITUR ('The thing speaks for itself'): Rule of evidence where negligence is inferred from the very nature of the event without direct proof: (A) Leaving a surgical mop / instrument inside abdominal cavity; (B) Operating on the wrong limb / organ; (C) Transfusing mismatched ABO blood. 3. JACOB MATHEW v. STATE OF PUNJAB (Supreme Court of India, 2005 Landmark Judgment on Criminal Negligence): Key holdings: (A) A mere error of clinical judgment, accident, or therapeutic misadventure DOES NOT AMOUNT TO CRIMINAL NEGLIGENCE! (B) To prosecute a doctor under criminal law (formerly Section 304A IPC, now Section 106 BNS), the negligence must be GROSS NEGLIGENCE ('reckless disregard of life and safety') &mdash; not simple civil negligence! (C) Investigating police officers CANNOT ARREST a medical doctor on an allegation of negligence without first obtaining an independent medical opinion from an expert government medical committee.",
        "citation": "Reddy's Essentials of Forensic Medicine and Toxicology, 34th Ed, Chapter 2 (Medical Law and Ethics), p. 25-45; Supreme Court of India: Jacob Mathew v. State of Punjab (2005) 6 SCC 1.",
        "difficulty": "medium"
    },

    # =========================================================================
    # --- COMMUNITY MEDICINE (6 Questions) ---
    # =========================================================================
    {
        "subject": "Community Medicine",
        "concept_name": "Epidemiology: Observational Study Designs & Risk Measures (RR vs OR)",
        "stem": (
            "An epidemiologist investigates the association between maternal consumption of valproic acid during the first trimester of pregnancy "
            "and congenital neural tube defects (spina bifida, anencephaly). Because neural tube defects occur in only ~1 to 2 per 1,000 live births "
            "(a rare disease), which observational epidemiological study design is the MOST METHODOLOGICALLY EFFICIENT and cost-effective, "
            "and what measure of association does it calculate?"
        ),
        "options": [
            ("Case-Control Study; Calculates the Odds Ratio (OR)", True, None),
            ("Prospective Cohort Study; Calculates the Relative Risk (RR)", False, "Cohort studies require immense sample sizes and years of follow-up for rare outcomes, making them inefficient and prohibitively expensive for rare diseases."),
            ("Cross-Sectional Analytic Survey; Calculates Point Prevalence", False, "Cross-sectional studies measure exposure and disease simultaneously, cannot establish temporal sequence, and suffer from survivor bias."),
            ("Ecological Correlation Study; Calculates the Attributable Risk Fraction", False, "Ecological studies analyze aggregate population-level data, subject to the ecological fallacy, and cannot assess individual exposure.")
        ],
        "pearl": "Epidemiological Study Designs: 1. CASE-CONTROL STUDY: Design: Retrospective (proceeds from OUTCOME / DISEASE back to EXPOSURE). Subjects: Cases (diseased individuals) and Controls (matched healthy individuals). ADVANTAGES: IDEAL FOR RARE DISEASES! Fast, inexpensive, small sample size required. Major Limitation: Recall bias & selection bias; cannot measure incidence directly! MEASURE OF ASSOCIATION: ODDS RATIO (OR = ad/bc; cross-product ratio). (When disease is rare, Odds Ratio approximates Relative Risk!). 2. COHORT STUDY: Design: Proceeds from EXPOSURE forward to OUTCOME (Prospective or Retrospective). Subjects: Exposed group vs Unexposed group, followed longitudinally over time. ADVANTAGES: IDEAL FOR RARE EXPOSURES! Can establish TEMPORALITY (exposure precedes disease), can study multiple outcomes from a single exposure, directly calculates INCIDENCE! Major Limitation: Expensive, long duration, loss to follow-up (attrition bias). MEASURE OF ASSOCIATION: RELATIVE RISK (RR = Incidence in exposed / Incidence in unexposed = [a/(a+b)] / [c/(c+d)]) and ATTRIBUTABLE RISK (AR = Incidence in exposed - Incidence in unexposed).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 3 (Principles of Epidemiology), p. 55-80; Gordis Epidemiology, 6th Ed.",
        "difficulty": "easy"
    },
    {
        "subject": "Community Medicine",
        "concept_name": "Screening & Diagnostic Testing: Sensitivity, Specificity & Prevalence Dynamics",
        "stem": (
            "A new rapid antigen lateral flow test is developed for screening dengue fever. In a validation cohort of 1,000 individuals "
            "evaluated against RT-PCR gold standard, the test exhibits a fixed Sensitivity of 90% and Specificity of 95%. "
            "The test is first deployed in a high-prevalence tertiary fever clinic (dengue prevalence = 20%), and then subsequently "
            "deployed for community mass screening during an inter-epidemic period (dengue prevalence = 1%). "
            "How do the Positive Predictive Value (PPV) and Negative Predictive Value (NPV) change when the test is moved from the high-prevalence to the low-prevalence setting?"
        ),
        "options": [
            ("The Positive Predictive Value (PPV) drops dramatically, while the Negative Predictive Value (NPV) increases; Sensitivity and Specificity remain unchanged", True, None),
            ("Both Sensitivity and Positive Predictive Value decrease in direct proportion to prevalence", False, "Sensitivity and Specificity are INTRINSIC properties of the diagnostic test itself; they DO NOT CHANGE with disease prevalence!"),
            ("The Positive Predictive Value increases because false positives decrease in the low-prevalence population", False, "In low prevalence, false positives outnumber true positives, causing PPV to plummet."),
            ("The Negative Predictive Value decreases because true negatives diminish in a low-prevalence setting", False, "NPV rises towards 100% in low-prevalence populations because almost all negative results are true negatives.")
        ],
        "pearl": "Diagnostic Testing & Disease Prevalence Dynamics: 1. CORE DEFINITIONS: Sensitivity = True Positive Rate = a / (a + c) [Ability to detect true disease; rules OUT disease when negative: SNOUT]. Specificity = True Negative Rate = d / (b + d) [Ability to correctly identify disease-free individuals; rules IN disease when positive: SPIN]. Positive Predictive Value (PPV) = a / (a + b) [Probability that a patient with a positive test actually has the disease]. Negative Predictive Value (NPV) = d / (c + d) [Probability that a patient with a negative test is truly disease-free]. 2. THE PREVALENCE RULE (Crucial NEET-PG Concept!): Sensitivity and Specificity are INTRINSIC test characteristics &mdash; THEY NEVER CHANGE WITH PREVALENCE! However, Predictive Values are EXTRINSIC and VARY DRAMATICALLY WITH PREVALENCE: As Disease Prevalence INCREASES &rarr; PPV INCREASES & NPV DECREASES! As Disease Prevalence DECREASES &rarr; PPV PLUMMETS & NPV APPROACHES 100%! (Why? When a disease is rare, even a 5% false-positive rate generates far more false positives than the tiny pool of true positives!).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 3 (Screening for Disease), p. 130-145; Gordis Epidemiology, 6th Ed.",
        "difficulty": "medium"
    },
    {
        "subject": "Community Medicine",
        "concept_name": "National Immunization Schedule: Vaccines, Doses, Routes & Cold Chain",
        "stem": (
            "A healthy mother brings her 6-week-old infant to the Primary Health Centre for routine immunization under India's Universal "
            "Immunization Programme (UIP). "
            "According to the current National Immunization Schedule (NIS), which complete set of vaccines, exact doses, and anatomical "
            "routes should this 6-week-old infant receive today?"
        ),
        "options": [
            ("Pentavalent-1 (0.5 mL IM anterolateral thigh), Oral Polio Vaccine OPV-1 (2 drops oral), Rotavirus-1 (5 drops oral), Pneumococcal Conjugate PCV-1 (0.5 mL IM opposite thigh), and Fractional Inactivated Polio Vaccine fIPV-1 (0.1 mL Intradermal right deltoid)", True, None),
            ("DPT-1 (0.5 mL IM gluteal region), Measles-Rubella MR-1 (0.5 mL SC), and BCG booster (0.1 mL ID)", False, "DPT has been replaced by Pentavalent (DPT+HepB+Hib) in infants, MR is given at 9 months, and gluteal injections are prohibited in infants due to sciatic nerve injury risk!"),
            ("BCG (0.05 mL ID), Hepatitis B birth dose (0.5 mL IM), and OPV-0 (2 drops oral)", False, "BCG, Hep B-0, and OPV-0 are given at BIRTH, not at the 6-week milestone visit."),
            ("Pentavalent-1 (0.5 mL SC) and full-dose intramuscular IPV (0.5 mL IM left arm) without rotavirus", False, "Pentavalent must be given Intramuscularly (not SC), and India's UIP uses fractional intradermal IPV (0.1 mL ID) with oral rotavirus.")
        ],
        "pearl": "National Immunization Schedule (NIS / UIP India): 1. AT BIRTH: BCG (0.05 mL ID left deltoid; if >1 month: 0.1 mL) + OPV '0' dose (2 drops oral) + Hepatitis B birth dose (0.5 mL IM anterolateral thigh within 24 hours of birth!). 2. AT 6, 10, AND 14 WEEKS: Pentavalent (DPT + Hep B + Hib: 0.5 mL IM anterolateral mid-thigh) + OPV 1, 2, 3 (2 drops oral) + Rotavirus (5 drops oral) + fIPV-1 at 6 wks and fIPV-2 at 14 wks (Fractional IPV: 0.1 mL INTRADERMAL right deltoid) + PCV-1 at 6 wks, PCV-2 at 14 wks, and PCV Booster at 9 months (0.5 mL IM anterolateral thigh). 3. AT 9 COMPLETED MONTHS: Measles-Rubella MR-1 (0.5 mL SC right upper arm) + JE-1 (in endemic districts: 0.5 mL SC) + Vitamin A (1st dose: 1 lakh IU = 1 mL oral) + PCV Booster. 4. COLD CHAIN: Ice-Lined Refrigerator (ILR): Keeps temperature between +2°C and +8°C (most critical equipment at PHC). Deep Freezer (-15°C to -25°C): Used to freeze ice packs and store OPV/MR. Most heat-sensitive vaccine: OPV. Most freeze-sensitive vaccine: Hep B / Td / Pentavalent (Shake test detects freezing damage!).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 7 (Health Programmes in India), p. 430-452; UIP Guidelines MoHFW India.",
        "difficulty": "medium"
    },
    {
        "subject": "Community Medicine",
        "concept_name": "Biomedical Waste Management Rules 2016: Color-Coded Segregation & Disposal",
        "stem": (
            "Following an uneventful spontaneous vaginal delivery in the labor room, a staff nurse needs to dispose of the following items: "
            "1. An intact human placenta | 2. A disposable plastic IV infusion set and empty normal saline bottle | 3. A disposable suture needle | 4. A broken glass vial of oxytocin. "
            "According to India's Biomedical Waste Management Rules 2016 (amended 2018/2019), into which colored containers must items 1, 2, 3, and 4 be segregated?"
        ),
        "options": [
            ("Placenta in YELLOW bag; IV infusion set in RED bag; Suture needle in WHITE translucent puncture-proof container; Broken glass vial in BLUE marked cardboard box", True, None),
            ("Placenta in RED bag; IV set in YELLOW bag; Suture needle in BLUE box; Glass vial in BLACK bin", False, "Human anatomical waste (placenta) must go into yellow for incineration; recyclable plastic (IV tubing) goes into red."),
            ("Placenta in YELLOW bag; IV set in BLUE box; Suture needle in RED bag; Glass vial in WHITE container", False, "Sharps (needles) must go into the white translucent puncture-proof container to prevent needlestick injuries."),
            ("All items into YELLOW chlorinated plastic bags for centralized high-temperature autoclaving", False, "Chlorinated bags are banned, and non-segregated disposal violates BMW 2016 statutory guidelines.")
        ],
        "pearl": "Biomedical Waste Management Rules (2016 / Amendments): 1. YELLOW BAG (Non-chlorinated, Incinerable): Category: Human & Animal Anatomical Waste (placenta, amputated limbs, biopsy specimens), Soiled Cotton/Gauze, Expired/Discarded Cytotoxic Drugs, Chemical Waste, Microbiological cultures. Treatment: INCINERATION or Plasma Pyrolysis. 2. RED BAG (Recyclable Contaminated Plastic): Category: Contaminated plastic tubing, IV bottles, IV sets, Catheters, Urine bags, Syringes WITHOUT needles, Gloves. Treatment: AUTOCLAVING / Hydroclaving followed by SHREDDING and recycling. 3. WHITE TRANSLUCENT CONTAINER (Puncture-proof, Tamper-proof): Category: METALLIC SHARPS &mdash; Needles, Syringes with fixed needles, Scalpel blades, Suture needles, Lumbar puncture needles. Treatment: Autoclaving/Dry Heat followed by Shredding or Encapsulation in concrete. 4. BLUE MARKED BOX / CARDBOARD BOX: Category: GLASSWARE & METALLIC IMPLANTS &mdash; Broken glass ampoules, medicine vials, glassware, orthopedic implants. Treatment: Disinfection (1-2% Sodium Hypochlorite) followed by Autoclaving.",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 19 (Hospital Waste Management), p. 810-822; Ministry of Environment, Forest and Climate Change BMW Rules 2016.",
        "difficulty": "easy"
    },
    {
        "subject": "Community Medicine",
        "concept_name": "Demography & Vital Statistics: IMR, MMR, TFR & Demographic Transition",
        "stem": (
            "According to the Sample Registration System (SRS) and international public health standards, what is the exact formula for "
            "calculating the Maternal Mortality Ratio (MMR), and what demographic metric represents the average number of children that would "
            "be born alive to a woman during her entire reproductive lifespan (Total Fertility Rate, TFR) required to achieve exact population replacement?"
        ),
        "options": [
            ("MMR = (Number of maternal deaths during pregnancy or within 42 days of termination / Total Live Births in same year) x 100,000; Replacement level TFR is 2.1", True, None),
            ("MMR = (Number of maternal deaths / Total Women of Reproductive Age 15-49) x 1,000; Replacement level TFR is 1.5", False, "Maternal mortality per women of reproductive age is Maternal Mortality Rate, not Ratio; replacement TFR is 2.1."),
            ("MMR = (Number of maternal deaths / Total Registered Pregnancies) x 10,000; Replacement level TFR is 2.5", False, "Denominator of MMR is total LIVE BIRTHS, expressed per 100,000 live births; replacement TFR is 2.1."),
            ("MMR = (Number of infant deaths / Total Live Births) x 1,000; Replacement level TFR is 3.0", False, "Infant deaths per 1,000 live births defines Infant Mortality Rate (IMR), not MMR.")
        ],
        "pearl": "Demographic & Maternal-Child Health Indicators: 1. MATERNAL MORTALITY RATIO (MMR): Definition: Maternal deaths resulting from obstetric causes during pregnancy, labor, or within 42 DAYS of termination of pregnancy, per 100,000 LIVE BIRTHS in the same year! (Expressed per 100,000, NOT per 1,000!). Leading causes of maternal mortality in India: Postpartum Hemorrhage (PPH, ~38%) > Hypertensive disorders/Eclampsia (~14%) > Sepsis (~11%). 2. TOTAL FERTILITY RATE (TFR): Definition: The average number of children that would be born alive to a woman during her lifetime if she passes through her childbearing years (15-49) conforming to current age-specific fertility rates. REPLACEMENT LEVEL FERTILITY: TFR = 2.1! (The 0.1 accounts for infant mortality and skewed sex ratio). India has achieved replacement TFR (NFHS-5: TFR = 2.0!). 3. INFANT MORTALITY RATE (IMR): Number of deaths of infants (<1 year of age) per 1,000 live births in a given year. Recognized globally as the SINGLE BEST SENSITIVE INDICATOR OF SOCIOECONOMIC DEVELOPMENT AND COMMUNITY HEALTH STATUS!",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 9 (Demography and Family Planning), p. 510-535; SRS Bulletin 2023.",
        "difficulty": "medium"
    },
    {
        "subject": "Community Medicine",
        "concept_name": "Vector-Borne Diseases: Mosquito Bionomics & Control in National Programs",
        "stem": (
            "During an urban outbreak of high fever, retro-orbital headache, severe arthralgias ('breakbone fever'), and petechiae, "
            "an entomological survey identifies daytime-biting mosquitoes breeding in domestic clean water storage containers, discarded tires, "
            "and desert room coolers. The mosquito exhibits black-and-white lyre-shaped markings on its thorax ('tiger mosquito') and rests horizontally on walls. "
            "What mosquito vector is responsible, and what larval control measure is recommended for clean drinking water storage tanks under NVBDCP?"
        ),
        "options": [
            ("Aedes aegypti; Application of Temephos 50% EC (Abate @ 1 ppm) or biological control with Gambusia affinis larvivorous fish", True, None),
            ("Anopheles stephensi; Spraying of Malathion thermal fogging into drinking water", False, "Malathion is an organophosphate insecticide for adult outdoor fogging; it is NEVER sprayed directly into drinking water!"),
            ("Culex quinquefasciatus; Pouring waste petroleum engine oil into overhead water tanks", False, "Culex breeds in dirty, foul wastewater/sewage drains; pouring petroleum into domestic drinking water is toxic and prohibited."),
            ("Mansonia annulifera; Application of chemical weedicides without vector surveillance", False, "Mansonia breeds in water bodies with aquatic vegetation (Pistia stratiotes) and transmits Brugian filariasis.")
        ],
        "pearl": "Mosquito Vector Bionomics Master Table: 1. AEDES AEGYPTI ('Tiger Mosquito'): Diseases: DENGUE, CHIKUNGUNYA, ZIKA, YELLOW FEVER. Breeding habitat: ARTIFICIAL CLEAN WATER CONTAINERS (desert coolers, plastic drums, flower pots, discarded tires). Biting habit: DAYTIME BITER (peaks 2 hours after sunrise and before sunset). Resting posture: Sits PARALLEL / HORIZONTAL to the surface. Flight range: Short flight range (<100 meters). Larval chemical control in potable water: TEMEPHOS (Abate @ 1 ppm / 1 mg per liter; safe in drinking water!). 2. ANOPHELES: Diseases: MALARIA. Breeding: CLEAN NATURAL WATER (ponds, river beds, irrigation channels, overhead tanks for A. stephensi). Biting habit: NIGHT BITER. Resting posture: Sits at an ANGULAR (45-degree) inclined posture to the wall. 3. CULEX: Diseases: LYMPHATIC FILARIASIS (Wuchereria bancrofti transmitted by C. quinquefasciatus) and JAPANESE ENCEPHALITIS (C. tritaeniorhynchus). Breeding: DIRTY, POLLUTED, FOUL SEWAGE WASTEWATER, cesspools, open drains.",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 5 (Epidemiology of Communicable Diseases), p. 275-300; NVBDCP Guidelines MoHFW.",
        "difficulty": "easy"
    }
]
