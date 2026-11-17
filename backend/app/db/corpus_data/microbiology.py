"""
Authentic High-Yield NEET-PG Clinical Questions for Microbiology
References: Ananthanarayan and Paniker's Textbook of Microbiology (11th Ed), Jawetz Medical Microbiology (28th Ed)
"""

MICROBIOLOGY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Hypersensitivity Reactions (Types I-IV)",
        "stem": (
            "A 24-year-old female presents to the emergency room with sudden generalized urticaria, periorbital and laryngeal edema, "
            "inspiratory stridor, and severe bronchospasm 10 minutes after receiving an intramuscular injection of Cefazolin. "
            "Her blood pressure drops to 70/40 mmHg. Which immunological mechanism, antibody class, and cellular mediator release "
            "are responsible for this acute Type I (Immediate) hypersensitivity reaction?"
        ),
        "options": [
            ("Cross-linking of allergen-specific IgE bound to high-affinity Fc-epsilon-RI receptors on tissue Mast Cells and Basophils, triggering degranulation of Histamine, Leukotrienes (LTC4, LTD4, LTE4), and Tryptase", True, None),
            ("IgG and IgM antibody binding to cell-surface antigens activating Complement-mediated lysis (Type II)", False, "Type II cytotoxic hypersensitivity involves IgG/IgM against fixed tissue antigens (e.g., autoimmune hemolytic anemia, Goodpasture)."),
            ("Deposition of circulating antigen-antibody Immune Complexes in microvascular beds (Type III)", False, "Type III immune complex hypersensitivity causes Serum Sickness, Arthus reaction, and Post-Streptococcal Glomerulonephritis."),
            ("Antigen-specific CD4+ Th1 and CD8+ T cells secreting Interferon-gamma (Type IV)", False, "Type IV delayed-type hypersensitivity is cell-mediated (e.g., Tuberculin skin test, Contact dermatitis).")
        ],
        "pearl": "Gell and Coombs Hypersensitivity Types (ACID Mnemonic): Type I: ANAPHYLACTIC / Immediate: IgE mediated, Mast cell/Basophil degranulation (Histamine, LTC4/LTD4/LTE4). Treatment: Intramuscular Epinephrine (1:1000) 0.5 mg anterolateral thigh! Type II: CYTOTOXIC: IgG/IgM against cell surfaces (Myasthenia gravis, Goodpasture, Hemolytic transfusion reaction). Type III: IMMUNE COMPLEX: Ag-Ab complexes deposit in tissues (SLE, Serum sickness, PSGN). Type IV: DELAYED / Cell-Mediated: T-cells, macrophages (PPD/Tuberculin test, Contact dermatitis, Nickel allergy).",
        "citation": "Ananthanarayan and Paniker's Textbook of Microbiology, 11th Ed, Chapter 16 (Hypersensitivity), p. 154-166.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Hypersensitivity Reactions (Types I-IV)",
        "stem": (
            "A 45-year-old male receives an intravenous infusion of equine antivenom for a Russell's viper snakebite. "
            "Eight days later, he presents with generalized urticaria, high fever, bilateral symmetrical polyarthralgias, "
            "generalized lymphadenopathy, and facial edema. Urinalysis demonstrates microscopic hematuria and proteinuria, "
            "and serum complement levels (C3 and C4) are markedly depressed. What type of hypersensitivity reaction is Acute Serum Sickness?"
        ),
        "options": [
            ("Type III (Immune Complex-Mediated) Hypersensitivity", True, None),
            ("Type I (IgE-Mediated) Hypersensitivity", False, "Type I occurs within minutes to hours of re-exposure, not 8-10 days later with complement consumption."),
            ("Type II (Antibody-Dependent Cytotoxic) Hypersensitivity", False, "Type II targets specific cellular antigens directly, whereas serum sickness involves systemic circulating immune complex deposition in small arterioles."),
            ("Type IV (Delayed T-Cell Mediated) Hypersensitivity", False, "Type IV does not consume serum complement C3/C4 and does not cause systemic vasculitis.")
        ],
        "pearl": "Acute Serum Sickness (Classic Type III Hypersensitivity): Occurs 7 to 14 days after exposure to foreign protein (e.g., Equine antivenom, Monoclonal antibodies, Penicillin). Circulating IgG/IgM bind foreign antigen -> form soluble immune complexes in slight antigen excess -> deposit in vascular beds of joints, kidneys, and skin -> activate classic complement pathway -> C3a and C5a recruit neutrophils -> acute necrotizing vasculitis, arthritis, and glomerulonephritis. Hallmarks: Fever + Arthralgia + Urticarial rash + LOW SERUM C3 and C4.",
        "citation": "Jawetz Medical Microbiology, 28th Ed, Chapter 8 (Immunology), p. 132-140.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Opportunistic Fungal Infections (Candida, Aspergillus, Mucor)",
        "stem": (
            "A 52-year-old male with poorly controlled Type 2 Diabetes Mellitus presents to the emergency room with Diabetic Ketoacidosis (DKA), "
            "severe right periorbital pain, proptosis, ptosis, complete right ophthalmoplegia, and an anesthetic black necrotic eschar "
            "over the right hard palate and nasal turbinates. Direct Potassium Hydroxide (10% KOH) mount and fungal histopathology "
            "of the necrotic palatal biopsy demonstrate broad, non-septate (aseptate or pauci-septate), ribbon-like hyphae with wide 90-degree right-angle branching. "
            "What is the diagnosis, and what is the definitive emergency management?"
        ),
        "options": [
            ("Rhino-orbito-cerebral Mucormycosis; Urgent surgical debridement of all necrotic tissue combined with high-dose Intravenous Liposomal Amphotericin B", True, None),
            ("Invasive Aspergillosis; Oral Voriconazole monotherapy alone", False, "Voriconazole is the drug of choice for Aspergillosis (septate 45-degree acute-angle hyphae), but has NO activity against Mucorales fungi!"),
            ("Candidal necrotizing stomatitis; Oral Fluconazole", False, "Fluconazole is completely inactive against Mucormycosis."),
            ("Pseudomembranous cellulitis; Intravenous Clindamycin", False, "A black necrotic eschar with ribbon-like aseptate hyphae in DKA is classic fungal mucormycosis, not bacterial cellulitis.")
        ],
        "pearl": "Mucormycosis vs Aspergillosis Key Differentiating Features: 1. MUCORMYCOSIS (Rhizopus, Mucor, Lichtheimia): Associated with Diabetic Ketoacidosis (ferritin/iron excess due to acidosis) and neutropenia/post-COVID. Angioinvasive (thrombosis and infarction) -> BLACK PALATAL/NASAL ESCHAR. Microscopy: BROAD, ASEPTATE (ribbon-like), 90-DEGREE RIGHT-ANGLE branching. DOC: Emergency extensive SURGICAL DEBRIDEMENT + IV LIPOSOMAL AMPHOTERICIN B (Voriconazole is ineffective!). 2. ASPERGILLOSIS (Aspergillus fumigatus): Microscopy: SLENDER, UNIFORMLY SEPTATE, 45-DEGREE DICHOTOMOUS ACUTE-ANGLE branching. DOC: VORICONAZOLE.",
        "citation": "Ananthanarayan and Paniker, 11th Ed, Chapter 58 (Opportunistic Mycoses), p. 612-622.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Opportunistic Fungal Infections (Candida, Aspergillus, Mucor)",
        "stem": (
            "A 38-year-old HIV-infected male with a CD4+ T-cell count of 45 cells/uL presents with subacute headache, low-grade fever, "
            "nausea, and confusion for 2 weeks. Physical examination reveals mild neck stiffness and bilateral sixth cranial nerve (abducens) palsies. "
            "Lumbar puncture reveals elevated opening pressure (320 mm H2O) and clear CSF. "
            "India Ink wet mount preparation of the uncentrifuged CSF demonstrates round to oval budding yeast cells surrounded by a wide, translucent, "
            "unstained gelatinous capsular halo against the dark background. What is the organism and the primary component of its diagnostic capsule?"
        ),
        "options": [
            ("Cryptococcus neoformans; Glucuronoxylomannan (GXM) polysaccharide capsule", True, None),
            ("Candida albicans; Beta-1,3-glucan cell wall", False, "Candida is an unencapsulated yeast forming pseudohyphae and germ tubes, negative on India ink."),
            ("Histoplasma capsulatum; Galactomannan surface protein", False, "Histoplasma is a small intracellular yeast found inside macrophages, lacking a gelatinous capsule."),
            ("Coccidioides immitis; Endospore-filled spherules", False, "Coccidioides forms thick-walled spherules filled with endospores.")
        ],
        "pearl": "Cryptococcus neoformans: Encapsulated yeast; acquired by inhalation of pigeon droppings in immunocompromised patients (HIV CD4 <100). VIRULENCE FACTOR: Large antiphagocytic polysaccharide capsule composed of GLUCURONOXYLOMANNAN (GXM). DIAGNOSTIC TESTS: 1. India Ink / Nigrosin (halo around yeast) | 2. Mucicarmine stain (capsule stains rose-red) | 3. Fontana-Masson stain (melanin in cell wall) | 4. Cryptococcal Antigen (CrAg) Lateral Flow Assay in CSF/serum (>98% sensitive). TREATMENT: Induction with IV Liposomal Amphotericin B + Flucytosine for 2 weeks, followed by oral Fluconazole maintenance.",
        "citation": "Jawetz Medical Microbiology, 28th Ed, Chapter 45 (Medical Mycology), p. 642-650.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Human Immunodeficiency Virus (HIV) Diagnostics",
        "stem": (
            "A healthcare worker sustains a deep percutaneous hollow-bore needle puncture wound contaminated with blood "
            "from an untreated HIV-positive patient with a high viral load. What is the approved standard post-exposure prophylaxis (PEP) regimen "
            "and the mandatory time frame within which PEP should ideally be initiated to prevent seroconversion?"
        ),
        "options": [
            ("Triple-drug antiretroviral regimen (Tenofovir disoproxil fumarate + Lamivudine + Dolutegravir) initiated as soon as possible, ideally within 2 hours and not exceeding 72 hours, continued for 28 days", True, None),
            ("Zidovudine monotherapy started within 7 days and taken for 14 days", False, "Monotherapy is obsolete and ineffective; dual/triple therapy is mandatory."),
            ("Single dose of Nevirapine taken within 24 hours", False, "Single-dose Nevirapine is an obsolete regimen once used for mother-to-child transmission, not occupational PEP."),
            ("Wait 6 weeks for fourth-generation ELISA serology before starting any medications", False, "Waiting allows viral integration into host DNA; PEP must be initiated within 72 hours!")
        ],
        "pearl": "HIV Post-Exposure Prophylaxis (PEP): Window: MUST BE STARTED WITHIN 72 HOURS of exposure (ideally within 2 hours). Ineffective if started after 72 hours! Regimen (WHO/NACO Guidelines): 3-Drug Regimen: Tenofovir (TDF 300 mg) + Lamivudine (3TC 300 mg) [or Emtricitabine] + DOLUTEGRAVIR (DTG 50 mg) once daily. DURATION: Exactly 28 DAYS. Testing schedule: Baseline, 6 weeks, 3 months, and 6 months.",
        "citation": "NACO National Guidelines for HIV Care / Ananthanarayan, 11th Ed, Chapter 55, p. 578-592.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Hepatitis Viruses (A-E) Serology",
        "stem": (
            "A 32-year-old male is evaluated for chronic hepatitis during routine pre-employment health screening. "
            "Serological testing reveals the following hepatitis B panel: "
            "HBsAg: POSITIVE | Anti-HBs: NEGATIVE | Anti-HBc IgM: NEGATIVE | Anti-HBc IgG: POSITIVE | HBeAg: POSITIVE | Anti-HBe: NEGATIVE. "
            "Serum HBV DNA by quantitative PCR is 8.4 x 10^7 IU/mL. What is the correct clinical interpretation of this patient's serological profile?"
        ),
        "options": [
            ("Chronic Hepatitis B infection with high viral replication and high infectivity", True, None),
            ("Acute Hepatitis B infection in the early window period", False, "Acute infection is characterized by high-titer Anti-HBc IgM; negative IgM with positive IgG indicates chronic infection (>6 months)."),
            ("Successful immunization with recombinant Hepatitis B vaccine", False, "Vaccination produces isolated Anti-HBs POSITIVE with all other markers negative (HBsAg negative, Anti-HBc negative)."),
            ("Resolved, past natural Hepatitis B infection with immune recovery", False, "Resolved past infection features Anti-HBs positive and Anti-HBc IgG positive, but HBsAg is NEGATIVE.")
        ],
        "pearl": "Hepatitis B Serology Master Table: 1. HBsAg (Surface Antigen): First marker to appear. Persistence >6 months = CHRONIC INFECTION. 2. Anti-HBs: Neutralizing protective antibody. Indicates IMMUNITY (via vaccination if isolated, or natural recovery if with anti-HBc IgG). 3. HBeAg: Envelope antigen = ACTIVE VIRAL REPLICATION & HIGH INFECTIVITY. 4. Anti-HBe: Indicates reduced viral replication and lower infectivity. 5. Anti-HBc IgM: First antibody; indicates ACUTE INFECTION (positive in 'Window Period' when both HBsAg and Anti-HBs are undetectable!). 6. Anti-HBc IgG: Marker of NATURAL INFECTION (past or chronic; NEVER present in vaccinated individuals!).",
        "citation": "Ananthanarayan and Paniker, 11th Ed, Chapter 49 (Hepatitis Viruses), p. 508-524.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Enterobacteriaceae & Typhoid Fever",
        "stem": (
            "A 22-year-old male presents with a step-ladder pattern remittent fever for 9 days, throbbing frontal headache, dry cough, "
            "and severe constipation followed by pea-soup diarrhea. On physical examination, temperature is 103.4°F with a pulse of 74 bpm "
            "(relative bradycardia / Faget's sign). Inspection of the trunk reveals faint, salmon-colored, blanching maculopapular spots "
            "('rose spots') over the lower chest and abdomen. What is the single most sensitive diagnostic investigation during this FIRST WEEK of Typhoid (Enteric) Fever?"
        ),
        "options": [
            ("Blood Culture in Bile Broth (positive in >90% of cases in week 1)", True, None),
            ("Widal Tube Agglutination test", False, "Widal test detects antibodies that become detectable only at the end of the 2nd week (significant titer: TO ≥1:160, TH ≥1:160)."),
            ("Stool culture on MacConkey agar", False, "Stool culture becomes positive primarily in the 2nd and 3rd weeks when bacteria are shed via the gallbladder into the gut."),
            ("Urine culture on CLED agar", False, "Urine culture becomes positive in the 3rd and 4th weeks.")
        ],
        "pearl": "Enteric Fever (Typhoid) Diagnostic Timeline (BASU Mnemonic): Week 1: BLOOD CULTURE (Bile broth / Castaneda's biphasic medium; 90% sensitivity). Week 2: AGGLUTINATION / WIDAL TEST (Anti-O and Anti-H titers). Week 3: STOOL CULTURE (shedding via bile from gallbladder). Week 4: URINE CULTURE. Bone Marrow Culture: Overall MOST SENSITIVE test (positive even after antibiotic therapy, >95% sensitive). Clinical features: Step-ladder fever + Relative bradycardia (Faget's sign) + Rose spots + Splenomegaly + Leukopenia.",
        "citation": "Ananthanarayan and Paniker, 11th Ed, Chapter 29 (Salmonella), p. 288-300.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Enterobacteriaceae & Typhoid Fever",
        "stem": (
            "In patients recovering from acute typhoid fever, approximately 2-5% become chronic asymptomatic carriers "
            "who continue to excrete Salmonella Typhi in their feces for more than one year. "
            "What is the primary anatomical reservoir site of chronic carriage in the human body?"
        ),
        "options": [
            ("Gallbladder (associated with cholelithiasis and biofilm formation)", True, None),
            ("Spleen pulp", False, "Spleen filters bacteria acutely, but does not serve as the chronic carrier reservoir."),
            ("Appendix lumen", False, "Appendix is not the chronic carriage reservoir."),
            ("Proximal jejunum", False, "Acid and rapid peristalsis prevent colonization; the gallbladder with bile is the classic niche.")
        ],
        "pearl": "Typhoid Carriers: Temporary Carrier: Excretes S. Typhi for 3 months to 1 year. Chronic Carrier: Excretes bacteria for > 1 YEAR. Primary Anatomical Reservoir: GALLBLADDER (Salmonella colonizes gallstones and forms biofilms on the gallbladder mucosa). Urinary carriers: Colonize the urinary bladder (associated with Schistosoma haematobium or renal stones). Screening test for carriers: Detection of anti-Vi antibodies (Vi capsular antigen agglutination test). Definitive treatment for gallbladder carriers: High-dose oral Ciprofloxacin/Ampicillin for 4-6 weeks +/- Cholecystectomy.",
        "citation": "Jawetz Medical Microbiology, 28th Ed, Chapter 15 (Enteric Gram-Negative Rods), p. 235-244.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Complement System & Deficiencies",
        "stem": (
            "A 19-year-old military recruit experiences his third episode of culture-confirmed Neisseria meningitidis bacterial meningitis. "
            "He has no history of recurrent infections with encapsulated pyogenic bacteria such as Streptococcus pneumoniae or Haemophilus influenzae. "
            "An inherited congenital deficiency of which components of the Complement Cascade predisposes individuals specifically "
            "to recurrent, life-threatening invasive infections with Neisseria species?"
        ),
        "options": [
            ("Terminal Membrane Attack Complex (MAC) components: C5, C6, C7, C8, or C9", True, None),
            ("Early classical pathway components: C1q, C1r, or C1s", False, "C1, C2, C4 deficiencies cause failure to clear immune complexes, strongly predisposing to Systemic Lupus Erythematosus (SLE)."),
            ("C3 component deficiency", False, "C3 deficiency causes severe, recurrent, life-threatening infections with all pyogenic encapsulated bacteria (S. pneumoniae, H. influenzae) and severe immune-complex disease."),
            ("Decay-Accelerating Factor (DAF / CD55) and CD59 deficiency", False, "CD55/CD59 deficiency leads to complement-mediated intravascular hemolysis in Paroxysmal Nocturnal Hemoglobinuria (PNH).")
        ],
        "pearl": "Complement Deficiencies & Disease Associations: 1. C5, C6, C7, C8, C9 (Terminal MAC Deficiency): Recurrent invasive NEISSERIA infections (N. meningitidis meningitis, N. gonorrhoeae bacteremia). 2. C1q, C1r, C1s, C4, C2 (Early Classical Pathway): SYSTEMIC LUPUS ERYTHEMATOSUS (SLE) and autoimmune glomerulonephritis (impaired clearance of apoptotic bodies). 3. C3 Deficiency: Severe recurrent pyogenic infections with encapsulated bacteria (opsonization defect). 4. C1 Esterase Inhibitor Deficiency: HEREDITARY ANGIOEDEMA (unregulated bradykinin generation -> non-pruritic, non-pitting laryngeal/facial/GI edema; treated with C1-INH concentrate or Icatibant).",
        "citation": "Ananthanarayan and Paniker, 11th Ed, Chapter 14 (Complement), p. 136-146.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Complement System & Deficiencies",
        "stem": (
            "A 26-year-old female presents with recurrent, episodic attacks of painless, non-pruritic, non-pitting subcutaneous edema "
            "involving her face, lips, tongue, and larynx, accompanied by severe colicky abdominal pain. "
            "She has zero response to high-dose intravenous Epinephrine, Diphenhydramine, and Dexamethasone. "
            "Serum C4 level is persistently undetectable, while C1q is normal. "
            "What is the underlying diagnosis, and which vasoactive peptide mediator is responsible for the vascular hyperpermeability?"
        ),
        "options": [
            ("Hereditary Angioedema (HAE) due to C1 Esterase Inhibitor deficiency; Bradykinin", True, None),
            ("Anaphylaxis; Histamine", False, "Anaphylaxis is histamine-mediated, pruritic with urticaria, and responds to epinephrine and antihistamines."),
            ("Pemphigus vulgaris; Interleukin-6", False, "Pemphigus is an autoimmune blistering disorder."),
            ("Hypocomplementemic urticarial vasculitis; Leukotriene B4", False, "HAE lacks urticarial wheals and is mediated by bradykinin accumulation.")
        ],
        "pearl": "Hereditary Angioedema (HAE): Autosomal dominant mutation in SERPING1 gene -> deficiency (Type 1, 85%) or dysfunction (Type 2, 15%) of C1 ESTERASE INHIBITOR (C1-INH). C1-INH normally inhibits both C1r/C1s and Plasma Kallikrein. Lack of C1-INH -> uninhibited kallikrein cleaves high-molecular-weight kininogen -> massive accumulation of BRADYKININ. Clinical hallmark: NO urticaria, NO pruritus (differentiates from allergic histamine angioedema!). Resistant to antihistamines and steroids! Screen with: Low serum C4. Acute attack treatment: C1-INH concentrate, Icatibant (bradykinin B2 receptor antagonist), or Ecallantide (kallikrein inhibitor).",
        "citation": "Jawetz Medical Microbiology, 28th Ed, Chapter 8, p. 142-146.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Autoimmunity & Immunodeficiency Syndromes",
        "stem": (
            "A 10-month-old male infant presents with his fourth episode of bacterial pneumonia and recurrent otitis media. "
            "Physical examination reveals absent tonsils and unpalpable peripheral lymph nodes. "
            "Serum protein electrophoresis demonstrates profoundly decreased levels of all immunoglobulin classes (IgG <100 mg/dL, IgA and IgM undetectable). "
            "Flow cytometry reveals a complete absence of circulating CD19+ and CD20+ mature B lymphocytes, "
            "with completely normal numbers of CD3+ T lymphocytes. Genetic testing reveals a mutation in the Bruton Tyrosine Kinase (BTK) gene on the X chromosome. "
            "What is this congenital immunodeficiency disorder?"
        ),
        "options": [
            ("X-Linked Agammaglobulinemia (XLA / Bruton's Disease)", True, None),
            ("Common Variable Immunodeficiency (CVID)", False, "CVID presents in young adults (20-30s) with low immunoglobulins but NORMAL numbers of circulating mature B cells."),
            ("DiGeorge Syndrome (22q11.2 deletion)", False, "DiGeorge syndrome features T-cell deficiency due to thymic hypoplasia, with normal B-cell counts and hypocalcemic tetany."),
            ("Severe Combined Immunodeficiency (SCID)", False, "SCID features profound defects in BOTH T cells and B cells (e.g. IL-2RG common gamma chain or ADA deficiency).")
        ],
        "pearl": "Congenital Immunodeficiency Differentials: 1. Bruton's X-Linked Agammaglobulinemia (XLA): Mutation in BTK gene -> pre-B cells fail to mature into B cells -> ABSENT MATURE B CELLS (CD19/CD20 = 0%) + Absent all immunoglobulins + Absent tonsils/germinal centers. Recurrent infections with encapsulated pyogenic bacteria after 6 months (loss of maternal IgG). 2. DiGeorge Syndrome: 3rd and 4th pharyngeal pouch defect (22q11.2 deletion) -> Absent Thymus (T-cell deficiency) + Absent Parathyroids (Hypocalcemia / Tetany) + Conotruncal cardiac defects. 3. SCID: Bubble boy disease; absent both T and B cells (opportunistic fungal, viral, and bacterial infections).",
        "citation": "Ananthanarayan and Paniker, 11th Ed, Chapter 17 (Immunodeficiency), p. 168-180.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Autoimmunity & Immunodeficiency Syndromes",
        "stem": (
            "A 2-year-old boy presents with severe eczema, recurrent sino-pulmonary infections, and spontaneous bleeding from his gums. "
            "Complete blood count reveals profound thrombocytopenia with platelets measuring 18,000/uL. "
            "On peripheral smear, the platelets are characteristically small in size (low mean platelet volume / MPV). "
            "Genetic analysis confirms an X-linked recessive mutation in a gene encoding an actin cytoskeleton-regulating protein. "
            "What is this classic clinical triad of Wiskott-Aldrich Syndrome?"
        ),
        "options": [
            ("Thrombocytopenia with microplatelets, Eczema, and Recurrent pyogenic infections (WATER mnemonic: Wiskott-Aldrich, Thrombocytopenia, Eczema, Recurrent infections)", True, None),
            ("Oculocutaneous albinism, peripheral neuropathy, and giant lysosomal granules", False, "This is Chediak-Higashi syndrome (LYST gene mutation)."),
            ("Ataxia, oculocutaneous telangiectasias, and elevated alpha-fetoprotein", False, "This is Ataxia-Telangiectasia (ATM gene mutation)."),
            ("Delayed umbilical cord separation, recurrent skin infections without pus, and extreme leukocytosis", False, "This is Leukocyte Adhesion Deficiency Type 1 (LAD-1; CD18 integrin defect).")
        ],
        "pearl": "Wiskott-Aldrich Syndrome (WAS): X-linked recessive mutation in WAS gene -> defective actin cytoskeleton assembly in hematopoietic cells. Classic Clinical Triad (WATER Mnemonic): W: Wiskott-Aldrich | A: Actin defect | T: THROMBOCYTOPENIA WITH SMALL (MICRO) PLATELETS | E: ECZEMA | R: RECURRENT INFECTIONS. Immunoglobulins: Low IgM, High IgA and IgE, Normal IgG. High risk of non-Hodgkin lymphoma and autoimmune diseases.",
        "citation": "Jawetz Medical Microbiology, 28th Ed, Chapter 8, p. 146-152.",
        "difficulty": "moderate"
    }
]
