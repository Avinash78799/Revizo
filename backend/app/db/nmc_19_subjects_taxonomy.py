"""
Canonical 19-Subject NEET-PG / NMC Curriculum Taxonomy Definition.
Maps the 19 core medical disciplines with official codes, authoritative textbooks, and standard chapters.
"""

NMC_19_SUBJECTS_METADATA = [
    {
        "name": "Anatomy",
        "code": "ANAT",
        "description": "Gross Anatomy, Embryology, Histology, Neuroanatomy & Genetics",
        "order_index": 1,
        "default_source": {
            "title": "Gray's Anatomy for Students",
            "edition": "4th Edition",
            "publisher": "Elsevier",
            "isbn": "978-0323393041",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Upper Limb & Pectoral Girdle", "topics": ["Brachial Plexus & Nerve Injuries", "Shoulder Joint & Rotator Cuff", "Cubital Fossa & Forearm Spaces"]},
            {"name": "Lower Limb", "topics": ["Femoral Triangle & Canal", "Knee Joint & Cruciate Ligaments", "Sciatic Nerve & Gluteal Region"]},
            {"name": "Thorax & Mediastinum", "topics": ["Coronary Circulation & Heart Anatomy", "Bronchopulmonary Segments", "Posterior Mediastinum & Thoracic Duct"]},
            {"name": "Head and Neck", "topics": ["Cranial Nerves & Cavernous Sinus", "Triangles of the Neck", "Larynx & Pharynx Anatomy"]},
            {"name": "Neuroanatomy", "topics": ["Circle of Willis & Stroke Syndromes", "Brainstem & Cranial Nerve Nuclei", "Spinal Cord Tracts & Lesions"]},
            {"name": "Embryology & Genetics", "topics": ["Pharyngeal Arches & Clefts", "Cardiac Embryology & Shunts", "Chromosomal Aneuploidies & Inheritance Patterns"]}
        ]
    },
    {
        "name": "Physiology",
        "code": "PHYS",
        "description": "General, Cellular, Organ System & Environmental Physiology",
        "order_index": 2,
        "default_source": {
            "title": "Guyton and Hall Textbook of Medical Physiology",
            "edition": "14th Edition",
            "publisher": "Elsevier",
            "isbn": "978-0323597128",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "General & Cellular Physiology", "topics": ["Resting Membrane Potential & Action Potential", "Transport Across Cell Membranes", "Acid-Base Balance Regulation"]},
            {"name": "Nerve & Muscle Physiology", "topics": ["Neuromuscular Transmission", "Excitation-Contraction Coupling", "Smooth Muscle vs Skeletal Muscle"]},
            {"name": "Cardiovascular Physiology", "topics": ["Cardiac Cycle & Pressure-Volume Loops", "Cardiac Output & Frank-Starling Law", "Blood Pressure Reflex Regulation"]},
            {"name": "Respiratory Physiology", "topics": ["Ventilation-Perfusion Matching", "Oxygen-Hemoglobin Dissociation Curve", "Lung Volumes & Compliance"]},
            {"name": "Renal Physiology", "topics": ["Glomerular Filtration Rate Regulation", "Countercurrent Multiplier Mechanism", "Renin-Angiotensin-Aldosterone Axis"]},
            {"name": "Endocrine & Reproductive Physiology", "topics": ["Hypothalamic-Pituitary Axis", "Thyroid & Parathyroid Hormone Regulation", "Adrenal Steroidogenesis"]}
        ]
    },
    {
        "name": "Biochemistry",
        "code": "BIOCH",
        "description": "Metabolism, Molecular Biology, Clinical Enzymes & Inborn Errors",
        "order_index": 3,
        "default_source": {
            "title": "Harper's Illustrated Biochemistry",
            "edition": "32nd Edition",
            "publisher": "McGraw Hill Professional",
            "isbn": "978-1260464948",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Carbohydrate Metabolism", "topics": ["Glycolysis & Gluconeogenesis", "Glycogen Storage Diseases", "TCA Cycle & Electron Transport Chain"]},
            {"name": "Lipid Metabolism", "topics": ["Fatty Acid Oxidation & Ketogenesis", "Dyslipidemias & Lipoprotein Metabolism", "Sphingolipidoses & Storage Disorders"]},
            {"name": "Amino Acid & Protein Metabolism", "topics": ["Urea Cycle Disorders", "Inborn Errors of Amino Acid Metabolism", "Porphyrias & Heme Synthesis"]},
            {"name": "Molecular Biology & Genetics", "topics": ["DNA Replication & Repair Mechanisms", "Transcription & Translation Control", "Recombinant DNA Technology & PCR"]},
            {"name": "Vitamins, Minerals & Enzymes", "topics": ["Fat-Soluble & Water-Soluble Vitamin Deficiencies", "Enzyme Kinetics & Lineweaver-Burk Plots", "Trace Elements & Free Radicals"]}
        ]
    },
    {
        "name": "Pharmacology",
        "code": "PHARM",
        "description": "General Principles, Systemic Drugs, Chemotherapy & Toxicology",
        "order_index": 4,
        "default_source": {
            "title": "Goodman & Gilman's: The Pharmacological Basis of Therapeutics",
            "edition": "14th Edition",
            "publisher": "McGraw Hill Professional",
            "isbn": "978-1264258079",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "General Pharmacological Principles", "topics": ["Pharmacokinetics: Half-Life & Clearance", "Receptor Pharmacodynamics & Agonists", "Adverse Drug Reactions & Teratogenicity"]},
            {"name": "Autonomic Nervous System Drugs", "topics": ["Cholinergic Agonists & Anticholinesterases", "Antimuscarinics & Atropine Poisoning", "Adrenergic Agonists & Sympatholytics"]},
            {"name": "Cardiovascular & Renal Drugs", "topics": ["Antihypertensive Drug Classes", "Antiarrhythmic Agents & Vaughan Williams", "Heart Failure Pharmacotherapy & Inotropes"]},
            {"name": "Antimicrobial & Antineoplastic Chemotherapy", "topics": ["Beta-Lactams & Resistance Mechanisms", "Antitubercular Drug Regimens", "Cytotoxic Chemotherapeutic Classes"]},
            {"name": "Central Nervous System Drugs", "topics": ["Antiepileptic Drugs & Mechanisms", "General & Local Anesthetics", "Psychopharmacology: Antidepressants & Antipsychotics"]}
        ]
    },
    {
        "name": "Pathology",
        "code": "PATH",
        "description": "General Pathology, Systemic Pathology, Hematology & Cytopathology",
        "order_index": 5,
        "default_source": {
            "title": "Robbins & Cotran Pathologic Basis of Disease",
            "edition": "10th Edition",
            "publisher": "Elsevier",
            "isbn": "978-0323531139",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "General Pathology", "topics": ["Cell Injury, Necrosis & Apoptosis", "Acute & Chronic Inflammation Mechanisms", "Hemodynamic Disorders, Shock & Thrombi"]},
            {"name": "Neoplasia & Genetics", "topics": ["Oncogenes & Tumor Suppressor Genes", "Hallmarks of Cancer & Metastasis", "Paraneoplastic Syndromes & Tumor Markers"]},
            {"name": "Hematology & Lymphoreticular Pathology", "topics": ["Microcytic & Macrocytic Anemias", "Acute & Chronic Leukemias", "Hodgkin & Non-Hodgkin Lymphomas"]},
            {"name": "Systemic Pathology", "topics": ["Atherosclerosis & Ischemic Heart Disease", "Glomerular Diseases & Nephrotic Syndrome", "Chronic Obstructive Pulmonary Diseases"]}
        ]
    },
    {
        "name": "Microbiology",
        "code": "MICRO",
        "description": "Bacteriology, Virology, Mycology, Parasitology & Immunology",
        "order_index": 6,
        "default_source": {
            "title": "Ananthanarayan and Paniker's Textbook of Microbiology",
            "edition": "12th Edition",
            "publisher": "Universities Press",
            "isbn": "978-9393330345",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "General Immunology", "topics": ["Hypersensitivity Reactions (Types I-IV)", "Complement System & Deficiencies", "Autoimmunity & Immunodeficiency Syndromes"]},
            {"name": "Systematic Bacteriology", "topics": ["Staphylococci & Streptococcal Infections", "Mycobacterium tuberculosis & Leprosy", "Enterobacteriaceae & Typhoid Fever"]},
            {"name": "Virology", "topics": ["Hepatitis Viruses (A-E) Serology", "Human Immunodeficiency Virus (HIV)", "Respiratory Viruses & Rabies"]},
            {"name": "Mycology & Parasitology", "topics": ["Opportunistic Fungal Infections", "Malaria Parasite Life Cycle & Speciation", "Intestinal Nematodes & Cestodes"]}
        ]
    },
    {
        "name": "Forensic Medicine",
        "code": "FMT",
        "description": "Medical Jurisprudence, Thanatology, Mechanical Injuries & Toxicology",
        "order_index": 7,
        "default_source": {
            "title": "The Essentials of Forensic Medicine and Toxicology",
            "edition": "35th Edition",
            "publisher": "Jaypee Brothers Medical Publishers",
            "isbn": "978-9354655616",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Thanatology & Postmortem Changes", "topics": ["Rigor Mortis & Algor Mortis", "Postmortem Hypostasis & Decomposition", "Suspended Animation & Brain Death Criteria"]},
            {"name": "Mechanical Injuries & Asphyxial Deaths", "topics": ["Firearm Wounds & Ballistics", "Hanging vs Strangulation Differences", "Drowning Findings & Diatom Test"]},
            {"name": "Medical Jurisprudence & Ethics", "topics": ["Medical Negligence & Res Ipsa Loquitur", "Informed Consent & Professional Secrecy", "Plea of Insanity & McNaughten Rule"]},
            {"name": "Clinical & Forensic Toxicology", "topics": ["Organophosphate & Aluminium Phosphide Poisoning", "Heavy Metal Poisoning: Lead & Arsenic", "Plant Poisons: Dhatura & Strychnine"]}
        ]
    },
    {
        "name": "Community Medicine",
        "code": "PSM",
        "description": "Epidemiology, Biostatistics, National Health Programs & Demography",
        "order_index": 8,
        "default_source": {
            "title": "Park's Textbook of Preventive and Social Medicine",
            "edition": "27th Edition",
            "publisher": "Banarsidas Bhanot Publishers",
            "isbn": "978-9382219194",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Epidemiology & Study Designs", "topics": ["Cohort vs Case-Control Studies & Odds Ratio", "Sensitivity, Specificity & Predictive Values", "Levels of Prevention (Primordial to Tertiary)"]},
            {"name": "Biostatistics & Public Health", "topics": ["Parametric vs Non-Parametric Tests", "Normal Distribution & Standard Error", "Measures of Central Tendency & Dispersion"]},
            {"name": "National Health Programs (India)", "topics": ["National Tuberculosis Elimination Program (NTEP)", "National Vector Borne Disease Control Program", "Universal Immunization Program (UIP) Schedule"]},
            {"name": "Environmental Health & Nutrition", "topics": ["Water Purification & Disinfection", "Biomedical Waste Management Guidelines", "Nutritional Deficiencies & Anthropometry"]}
        ]
    },
    {
        "name": "General Medicine",
        "code": "MED",
        "description": "Cardiology, Pulmonology, Gastroenterology, Nephrology, Neurology, Rheumatology & Endocrinology",
        "order_index": 9,
        "default_source": {
            "title": "Harrison's Principles of Internal Medicine",
            "edition": "21st Edition",
            "publisher": "McGraw Hill Professional",
            "isbn": "978-1264268504",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Cardiology & Vascular Medicine", "topics": ["Acute Coronary Syndromes & Biomarkers", "Heart Failure Guideline-Directed Therapy", "Valvular Heart Disease & Endocarditis"]},
            {"name": "Pulmonology & Critical Care", "topics": ["COPD & Asthma Stepwise Management", "Community-Acquired Pneumonia & CURB-65", "Acute Respiratory Distress Syndrome (ARDS)"]},
            {"name": "Endocrinology & Metabolism", "topics": ["Diabetic Ketoacidosis & Hyperglycemic States", "Thyroid Storm & Myxedema Coma", "Adrenal Insufficiency & Cushing Syndrome"]},
            {"name": "Nephrology & Electrolytes", "topics": ["Acute Kidney Injury KDIGO Staging", "Hyponatremia & Hyperkalemia Management", "Glomerulonephritis Clinical Syndromes"]},
            {"name": "Neurology & Stroke", "topics": ["Acute Ischemic Stroke & Thrombolysis", "Epilepsy Syndromes & Status Epilepticus", "Bacterial Meningitis & CSF Analysis"]}
        ]
    },
    {
        "name": "Pediatrics",
        "code": "PED",
        "description": "Growth & Development, Neonatology, Pediatric Nutrition, Genetics & Infections",
        "order_index": 10,
        "default_source": {
            "title": "Nelson Textbook of Pediatrics",
            "edition": "21st Edition",
            "publisher": "Elsevier",
            "isbn": "978-0323529501",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Growth, Development & Milestones", "topics": ["Motor & Social Developmental Milestones", "Assessment of Short Stature", "Severe Acute Malnutrition (SAM) Protocols"]},
            {"name": "Neonatology & Perinatal Care", "topics": ["Neonatal Resuscitation Program (NRP) Guidelines", "Respiratory Distress Syndrome & Surfactant", "Neonatal Jaundice: Phototherapy & Exchange"]},
            {"name": "Pediatric Infectious Diseases", "topics": ["Measles, Mumps & Rubella Complications", "Congenital Infections (TORCH)", "Pediatric Sepsis & Febrile Seizures"]},
            {"name": "Pediatric Cardiology & Nephrology", "topics": ["Acyanotic vs Cyanotic Congenital Heart Diseases", "Pediatric Nephrotic Syndrome & Steroid Regimens", "Kawasaki Disease Diagnostic Criteria"]}
        ]
    },
    {
        "name": "Dermatology",
        "code": "DERM",
        "description": "Dermatoses, Sexually Transmitted Infections, Leprosy & Mycotic Infections",
        "order_index": 11,
        "default_source": {
            "title": "Rook's Textbook of Dermatology",
            "edition": "9th Edition",
            "publisher": "Wiley-Blackwell",
            "isbn": "978-1118441190",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Papulosquamous & Bullous Disorders", "topics": ["Psoriasis Vulgaris & Nail Changes", "Pemphigus Vulgaris vs Bullous Pemphigoid", "Lichen Planus Pathognomonic Features"]},
            {"name": "Infectious Dermatology & Leprosy", "topics": ["Ridley-Jopling Leprosy Classification & Reactions", "Cutaneous Tuberculosis Variants", "Superficial Fungal Dermatophytoses"]},
            {"name": "Sexually Transmitted Infections", "topics": ["Syphilis Stages & Serology", "Genital Ulcer Disease Syndromic Management", "Gonococcal vs Non-Gonococcal Urethritis"]}
        ]
    },
    {
        "name": "Psychiatry",
        "code": "PSYCH",
        "description": "Psychotic Disorders, Mood Disorders, Anxiety, Neurodevelopmental & Substance Abuse",
        "order_index": 12,
        "default_source": {
            "title": "Kaplan and Sadock's Synopsis of Psychiatry",
            "edition": "12th Edition",
            "publisher": "Wolters Kluwer",
            "isbn": "978-1975145941",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Psychotic & Mood Disorders", "topics": ["Schizophrenia First-Rank Symptoms & Management", "Bipolar Disorder & Lithium Therapy", "Major Depressive Disorder & SSRIs"]},
            {"name": "Anxiety, Stress & Somatoform Disorders", "topics": ["Panic Disorder & Agoraphobia", "Obsessive-Compulsive Disorder", "Post-Traumatic Stress Disorder (PTSD)"]},
            {"name": "Substance Use & Neurocognitive Disorders", "topics": ["Alcohol Withdrawal & Delirium Tremens", "Opioid Toxicity & Naloxone", "Delirium vs Dementia Differential"]}
        ]
    },
    {
        "name": "Radiodiagnosis",
        "code": "RAD",
        "description": "X-Ray, Ultrasound, CT, MRI, Nuclear Medicine & Interventional Radiology",
        "order_index": 13,
        "default_source": {
            "title": "Grainger & Allison's Diagnostic Radiology",
            "edition": "7th Edition",
            "publisher": "Elsevier",
            "isbn": "978-0702075247",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Thoracic & Cardiovascular Radiology", "topics": ["Chest X-Ray Signs (Sail, Silhouette, Deep Sulcus)", "High-Resolution CT (HRCT) Chest Patterns", "Aortic Dissection & Pulmonary Embolism CT"]},
            {"name": "Neuro & Abdominal Imaging", "topics": ["Non-Contrast Head CT in Stroke & Hemorrhage", "Abdominal Ultrasound & Biliary Imaging", "MRI Sequences (T1, T2, FLAIR, DWI)"]}
        ]
    },
    {
        "name": "Anesthesiology",
        "code": "ANES",
        "description": "General Anesthesia, Regional Blocks, Airway Management & Critical Care Resuscitation",
        "order_index": 14,
        "default_source": {
            "title": "Morgan and Mikhail's Clinical Anesthesiology",
            "edition": "7th Edition",
            "publisher": "McGraw Hill Professional",
            "isbn": "978-1260473797",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "General Anesthesia & Inhalation Agents", "topics": ["Minimum Alveolar Concentration (MAC) & Potency", "Intravenous Anesthetic Agents: Propofol & Ketamine", "Malignant Hyperthermia Diagnosis & Dantrolene"]},
            {"name": "Airway Management & Regional Anesthesia", "topics": ["Mallampati Classification & Difficult Airway Algorithm", "Spinal vs Epidural Anesthesia Differences", "Local Anesthetic Systemic Toxicity (LAST) & Lipid Emulsion"]}
        ]
    },
    {
        "name": "General Surgery",
        "code": "SURG",
        "description": "Trauma, Acute Abdomen, Oncology, Gastrointestinal, Breast, Thyroid & Wound Healing",
        "order_index": 15,
        "default_source": {
            "title": "Bailey & Love's Short Practice of Surgery",
            "edition": "28th Edition",
            "publisher": "CRC Press",
            "isbn": "978-0367683290",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Principles of Surgery & Trauma", "topics": ["ATLS Primary Survey & Hemorrhagic Shock", "Burns Assessment: Rule of Nines & Parkland Formula", "Surgical Nutrition & Wound Dehiscence"]},
            {"name": "Endocrine & Breast Surgery", "topics": ["Thyroid Nodules & Bethesda Classification", "Breast Cancer Staging & Triple Assessment", "Salivary Gland Tumors: Pleomorphic Adenoma"]},
            {"name": "Gastrointestinal & Abdominal Surgery", "topics": ["Acute Appendicitis & Alvarado Score", "Intestinal Obstruction & Volvulus", "Gallstone Disease & Laparoscopic Cholecystectomy"]}
        ]
    },
    {
        "name": "Orthopedics",
        "code": "ORTHO",
        "description": "Traumatology, Joint Pathology, Bone Tumors, Pediatric Orthopedics & Spine",
        "order_index": 16,
        "default_source": {
            "title": "Apley & Solomon's System of Orthopaedics and Trauma",
            "edition": "10th Edition",
            "publisher": "CRC Press",
            "isbn": "978-1498751674",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Traumatology & Fractures", "topics": ["Upper Limb Fractures (Colles, Smith, Galeazzi, Monteggia)", "Hip Fractures: Intracapsular vs Extracapsular", "Compartment Syndrome Diagnosis & Fasciotomy"]},
            {"name": "Orthopedic Infections & Bone Tumors", "topics": ["Acute Osteomyelitis in Children", "Osteosarcoma vs Ewing Sarcoma Radiological Signs", "Tuberculosis of Spine (Pott's Disease)"]}
        ]
    },
    {
        "name": "Otorhinolaryngology (ENT)",
        "code": "ENT",
        "description": "Ear, Nose, Paranasal Sinuses, Oral Cavity, Pharynx & Larynx",
        "order_index": 17,
        "default_source": {
            "title": "Diseases of Ear, Nose and Throat & Head and Neck Surgery",
            "edition": "8th Edition",
            "publisher": "Elsevier",
            "isbn": "978-8131264256",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Otology & Neurotology", "topics": ["Chronic Suppurative Otitis Media (CSOM) Variants", "Otosclerosis & Carhart's Notch", "Meniere's Disease Diagnostic Triad"]},
            {"name": "Rhinology & Laryngology", "topics": ["Epistaxis: Little's Area & Management", "Juvenile Nasopharyngeal Angiofibroma (JNA)", "Laryngeal Carcinoma & Vocal Cord Nodules"]}
        ]
    },
    {
        "name": "Ophthalmology",
        "code": "OPHTH",
        "description": "Cornea, Lens, Glaucoma, Retina, Uvea, Neuro-Ophthalmology & Strabismus",
        "order_index": 18,
        "default_source": {
            "title": "Kanski's Clinical Ophthalmology",
            "edition": "9th Edition",
            "publisher": "Elsevier",
            "isbn": "978-0702077111",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Anterior Segment & Glaucoma", "topics": ["Primary Open-Angle vs Angle-Closure Glaucoma", "Cataract Types & Surgical Techniques (Phaco)", "Corneal Ulcers: Bacterial vs Fungal vs Viral"]},
            {"name": "Posterior Segment & Neuro-Ophthalmology", "topics": ["Diabetic Retinopathy Classification (ETDRS)", "Retinal Detachment: Rhegmatogenous vs Exudative", "Optic Neuritis & Papilledema Differentials"]}
        ]
    },
    {
        "name": "Obstetrics & Gynecology",
        "code": "OBGYN",
        "description": "Antenatal Care, Intrapartum Management, Gynecologic Oncology, Infertility & Contraception",
        "order_index": 19,
        "default_source": {
            "title": "DC Dutta's Textbook of Obstetrics",
            "edition": "9th Edition",
            "publisher": "Jaypee Brothers Medical Publishers",
            "isbn": "978-9352709977",
            "source_type": "STANDARD_TEXTBOOK"
        },
        "chapters": [
            {"name": "Obstetrics & Perinatology", "topics": ["Preeclampsia & Eclampsia Management (Magnesium Sulfate)", "Postpartum Hemorrhage (PPH) Management Protocol", "Antepartum Hemorrhage: Placenta Previa vs Abruptio"]},
            {"name": "Gynecology & Gynecologic Oncology", "topics": ["Cervical Cancer Screening & FIGO Staging", "Ovarian Tumors & RMI Scoring", "Polycystic Ovary Syndrome (Rotterdam Criteria)"]}
        ]
    }
]
