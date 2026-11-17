"""
Authentic High-Yield NEET-PG Clinical Questions for Biochemistry
References: Harper's Illustrated Biochemistry (32nd Ed), Vasudevan's Textbook of Biochemistry (9th Ed)
"""

BIOCHEMISTRY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Inborn Errors of Amino Acid Metabolism",
        "stem": (
            "A 6-month-old male infant born of consanguineous parentage is brought to the pediatrician due to developmental delay "
            "and failure to attain milestones. The mother notices a characteristic musty, mousy body and urinary odor. "
            "Physical examination reveals fair skin, blonde hair, and blue eyes in an infant of dark-complexioned Indian parents, "
            "along with microcephaly and infantile eczema. Serum Phenylalanine is markedly elevated at 28 mg/dL (normal <2 mg/dL). "
            "What is the deficient enzyme, and which amino acid becomes nutritionally ESSENTIAL in this child's diet?"
        ),
        "options": [
            ("Phenylalanine Hydroxylase (PAH); Tyrosine becomes an essential amino acid", True, None),
            ("Homogentisate 1,2-Dioxygenase; Phenylalanine becomes essential", False, "Homogentisate oxidase deficiency causes Alkaptonuria (ochronosis, dark urine)."),
            ("Branched-Chain Alpha-Keto Acid Dehydrogenase; Leucine becomes essential", False, "Branched-chain ketoacid dehydrogenase deficiency causes Maple Syrup Urine Disease (MSUD)."),
            ("Dihydropteridine Reductase alone; Tryptophan becomes essential", False, "Malignant PKU (BH4 deficiency) is caused by DHPR, but classic PKU is PAH deficiency.")
        ],
        "pearl": "Phenylketonuria (Classic PKU): Autosomal recessive deficiency of PHENYLALANINE HYDROXYLASE (PAH on chromosome 12q). Converts Phenylalanine -> Tyrosine using Tetrahydrobiopterin (BH4) cofactor. Accumulation of Phenylalanine -> alternate transamination into Phenylpyruvate, Phenyllactate, and Phenylacetate -> MOUSY / MUSTY ODOR. Hypopigmentation (fair skin/blonde hair) occurs because Tyrosine is the precursor for Melanin (competitive inhibition of Tyrosinase by phenylalanine). DIETARY MANAGEMENT: Restrict dietary Phenylalanine; TYROSINE BECOMES CONDITIONALLY ESSENTIAL!",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 29 (Catabolism of Proteins and Amino Acids), p. 280-292.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Inborn Errors of Amino Acid Metabolism",
        "stem": (
            "A 38-year-old male presents with severe chronic lower back pain and stiffness. Physical examination reveals "
            "bluish-black pigmentation of the sclera of both eyes (Osler's sign) and ear cartilages. "
            "Spine radiograph demonstrates dense, widespread calcification of all intervertebral disc spaces with vacuum disc phenomenon. "
            "When the patient's freshly voided normal-colored urine is allowed to stand on the laboratory bench exposed to atmospheric air "
            "for 2 hours, it turns jet-black. What is the deficient enzyme and the accumulating metabolic intermediate?"
        ),
        "options": [
            ("Homogentisate 1,2-Dioxygenase; Homogentisic Acid (Alkaptonuria)", True, None),
            ("Tyrosinase; DOPAquinone (Oculocutaneous Albinism)", False, "Tyrosinase deficiency causes albinism with lack of melanin, not dark urine or ochronosis."),
            ("Fumarylacetoacetate Hydrolase; Succinylacetone (Tyrosinemia Type 1)", False, "Fumarylacetoacetate hydrolase causes Hepatorenal Tyrosinemia Type 1 (cabbage-like odor, liver cirrhosis, Fanconi syndrome)."),
            ("Cystathionine Beta-Synthase; Homocysteine (Homocystinuria)", False, "Cystathionine beta-synthase deficiency causes Homocystinuria (marfanoid habitus, downward ectopia lentis, thrombosis).")
        ],
        "pearl": "Alkaptonuria (Black Urine Disease): First discovered inborn error of metabolism described by Sir Archibald Garrod (1902). Autosomal recessive deficiency of HOMOGENTISATE 1,2-DIOXYGENASE in the tyrosine/phenylalanine degradation pathway. Accumulation: HOMOGENTISIC ACID (HGA). Triad of Alkaptonuria: 1. Homogentisic aciduria: Urine turns JET BLACK on standing or alkalinization (HGA oxidizes to benzoquinone acetate polymer / alkapton pigment). 2. OCHRONOSIS: Bluish-black pigment deposited in cartilages, sclera, pinna, and tendons. 3. Ochronotic Arthritis: Severe degenerative disc calcification in spine and large joints.",
        "citation": "Vasudevan's Textbook of Biochemistry, 9th Ed, Chapter 15 (Amino Acid Metabolism), p. 210-218.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Glycolysis & Gluconeogenesis",
        "stem": (
            "Phosphofructokinase-1 (PFK-1) is the primary rate-limiting, committed regulatory enzyme of the glycolytic pathway in mammals. "
            "Which of the following intracellular allosteric metabolites is the MOST POTENT POSITIVE ALLOSTERIC ACTIVATOR of PFK-1, "
            "overcoming ATP-induced allosteric inhibition and stimulating high glycolytic flux in the well-fed state?"
        ),
        "options": [
            ("Fructose-2,6-Bisphosphate (F-2,6-BP)", True, None),
            ("Citrate", False, "Citrate from the TCA cycle is a powerful NEGATIVE allosteric inhibitor of PFK-1, signaling that energy supplies are abundant."),
            ("Adenosine Triphosphate (ATP)", False, "High ATP is an allosteric INHIBITOR of PFK-1, slowing glycolysis when cellular energy is high."),
            ("Glucose-6-Phosphate", False, "G-6-P inhibits Hexokinase, but does not activate PFK-1.")
        ],
        "pearl": "PFK-1 Allosteric Regulation: Rate-limiting step: Fructose-6-P -> Fructose-1,6-Bisphosphate. MOST POTENT ACTIVATOR: FRUCTOSE-2,6-BISPHOSPHATE (F-2,6-BP). Formed from F-6-P by the bifunctional tandem enzyme PFK-2 / FBPase-2. Insulin DEPHOSPHORYLATES the bifunctional enzyme -> activates PFK-2 -> raises F-2,6-BP -> dramatically stimulates PFK-1 (accelerating glycolysis). Glucagon PHOSPHORYLATES the enzyme via Protein Kinase A -> activates FBPase-2 -> lowers F-2,6-BP -> shuts off PFK-1 and activates FBPase-1 (promoting gluconeogenesis). PFK-1 Allosteric Inhibitors: High ATP, Citrate, H+ (acidosis). Other Activators: AMP, ADP.",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 17 (Glycolysis), p. 156-166.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Glycolysis & Gluconeogenesis",
        "stem": (
            "During prolonged starvation (fasting >48 hours), hepatic gluconeogenesis maintains normoglycemia. "
            "Gluconeogenesis requires bypassing the three irreversible, highly exergonic reactions of glycolysis. "
            "Which mitochondrial enzyme catalyzes the first committed bypass reaction of gluconeogenesis, "
            "converting Pyruvate into Oxaloacetate using Biotin as a cofactor and requiring allosteric activation by Acetyl-CoA?"
        ),
        "options": [
            ("Pyruvate Carboxylase (activated by Acetyl-CoA, requires ATP and Biotin)", True, None),
            ("Phosphoenolpyruvate Carboxykinase (PEPCK)", False, "PEPCK converts oxaloacetate to phosphoenolpyruvate using GTP in the cytosol/mitochondria."),
            ("Fructose-1,6-Bisphosphatase (FBPase-1)", False, "FBPase-1 bypasses PFK-1 in the cytosol (converts F-1,6-BP to F-6-P)."),
            ("Glucose-6-Phosphatase", False, "Glucose-6-phosphatase bypasses hexokinase in the endoplasmic reticulum, releasing free glucose.")
        ],
        "pearl": "Gluconeogenesis 4 Key Bypass Enzymes (ABC Mnemonic): Bypass 1: Pyruvate -> Phosphoenolpyruvate (PEP): Step 1A: PYRUVATE CARBOXYLASE (mitochondrial, requires ATP, Biotin, CO2; ALLISTERICAL ACTIVATED BY ACETYL-CoA from beta-oxidation!). Pyruvate + CO2 -> Oxaloacetate (OAA). Step 1B: PEPCK (requires GTP): OAA -> PEP. Bypass 2: FRUCTOSE-1,6-BISPHOSPHATASE (cytosol): F-1,6-BP -> F-6-P (inhibited by AMP and F-2,6-BP). Bypass 3: GLUCOSE-6-PHOSPHATASE (ER membrane): G-6-P -> Free Glucose (absent in skeletal muscle; hence muscle glycogen CANNOT produce free blood glucose!).",
        "citation": "Vasudevan's Textbook of Biochemistry, 9th Ed, Chapter 10 (Gluconeogenesis), p. 132-140.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Glycogen Storage Diseases",
        "stem": (
            "A 4-month-old infant presents with severe lethargy, sweating, and generalized seizures upon fasting for 3 hours. "
            "Physical examination reveals a massive, soft hepatomegaly, a rounded 'doll-like' facies with chubby cheeks, "
            "and thin extremities. Spleen and heart are completely normal in size. "
            "Laboratory tests show severe fasting hypoglycemia (<25 mg/dL), marked lactic acidosis, hyperuricemia, and severe hyperlipidemia. "
            "Administration of intramuscular Glucagon or Epinephrine causes NO RISE in blood glucose, but triggers a sharp increase in blood lactate. "
            "What is the deficient enzyme in this Glycogen Storage Disease Type I (Von Gierke's Disease)?"
        ),
        "options": [
            ("Glucose-6-Phosphatase (in the endoplasmic reticulum of liver and kidney)", True, None),
            ("Lysosomal Alpha-1,4-Glucosidase (Acid Maltase)", False, "Acid maltase deficiency is Pompe's disease (GSD Type II), presenting with massive cardiomegaly and early infantile death without hypoglycemia."),
            ("Glycogen Debranching Enzyme (Amylo-alpha-1,6-glucosidase)", False, "Debranching enzyme deficiency is Cori's disease (GSD Type III), where gluconeogenesis is intact, fasting hypoglycemia is milder, and blood lactate is normal."),
            ("Muscle Glycogen Phosphorylase", False, "Muscle phosphorylase deficiency is McArdle's disease (GSD Type V), causing exercise-induced muscle cramps and myoglobinuria without hypoglycemia.")
        ],
        "pearl": "Glycogen Storage Diseases (GSDs) Master Table: 1. Type I (VON GIERKE DISEASE): Glucose-6-Phosphatase deficiency. Severe fasting hypoglycemia + Massive Hepatomegaly (steatosis) + Doll-like facies + LACTIC ACIDOSIS (excess G-6-P shunted to glycolysis) + Hyperuricemia (gout) + Hypertriglyceridemia. 2. Type II (POMPE DISEASE): Lysosomal Acid Maltase (alpha-1,4-glucosidase) deficiency -> Glycogen accumulates in lysosomes -> MASSIVE CARDIOMEGALY, hypotonia, death <2 yrs (normal blood glucose). 3. Type III (CORI DISEASE): Debranching enzyme (alpha-1,6-glucosidase) deficiency -> limit dextrin accumulates; gluconeogenesis intact, NORMAL blood lactate. 4. Type V (McARDLE DISEASE): Muscle Phosphorylase deficiency -> painful muscle cramps on exertion, myoglobinuria ('burgundy urine'), no rise in blood lactate after ischemic exercise.",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 18 (Glycogen Metabolism), p. 172-182.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Dyslipidemias & Lipoprotein Metabolism",
        "stem": (
            "A 36-year-old male presents with sudden-onset acute retrosternal chest pain and is diagnosed with extensive anterior myocardial infarction. "
            "Physical examination reveals prominent yellowish nodular xanthomas over his Achilles tendons (tendon xanthomas), "
            "bilateral xanthelasmas around the eyelids, and a premature corneal arcus. His father died of a myocardial infarction at age 39. "
            "Lipid panel reveals: Total Cholesterol 420 mg/dL, LDL-Cholesterol 330 mg/dL (normal <100 mg/dL), Triglycerides 130 mg/dL (normal). "
            "What is the underlying molecular defect responsible for Familial Hypercholesterolemia (Fredrickson Type IIa)?"
        ),
        "options": [
            ("Autosomal dominant mutation in the cell-surface Low-Density Lipoprotein (LDL) Receptor gene on chromosome 19p", True, None),
            ("Apolipoprotein C-II deficiency", False, "ApoC-II deficiency causes Type I Hyperchylomicronemia (triglycerides >1000 mg/dL and recurrent pancreatitis, not isolated hypercholesterolemia)."),
            ("Apolipoprotein E2/E2 homozygous deficiency", False, "ApoE2/E2 causes Type III Dysbetalipoproteinemia (tuberoeruptive and palmar xanthomas)."),
            ("Lipoprotein Lipase (LPL) deficiency", False, "LPL deficiency causes Type I chylomicronemia with eruptive xanthomas and milky fasting serum.")
        ],
        "pearl": "Fredrickson Dyslipidemias Classification: Type I (Familial Hyperchylomicronemia): Defect in Lipoprotein Lipase (LPL) or ApoC-II -> massive CHYLOMICRONS -> Triglycerides >1000 mg/dL -> Recurrent Acute Pancreatitis, Eruptive Xanthomas, Lipemia retinalis (NO premature CAD!). Type IIa (FAMILIAL HYPERCHOLESTEROLEMIA): Defect in LDL RECEPTOR (or ApoB-100 or gain-of-function PCSK9) -> isolated high LDL -> Premature Atherosclerosis / MI before age 40 + TENDON XANTHOMAS (Achilles tendon) + Corneal Arcus. Type III (Dysbetalipoproteinemia): Defect in ApoE (ApoE2 homozygote) -> elevated IDL/chylomicron remnants -> PALMAR XANTHOMAS and tuberoeruptive xanthomas.",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 25 (Lipid Transport), p. 238-250.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Fat-Soluble & Water-Soluble Vitamin Deficiencies",
        "stem": (
            "A 48-year-old chronic alcoholic male is brought to the emergency department in a state of acute confusion, apathy, and drowsiness. "
            "Physical examination reveals horizontal nystagmus, bilateral lateral rectus palsy (sixth nerve palsy causing conjugate gaze palsy), "
            "and severe broad-based cerebellar ataxia. Which vitamin is acutely deficient, and which enzymatic reaction in carbohydrate metabolism "
            "is impaired, causing neurotoxicity?"
        ),
        "options": [
            ("Thiamine (Vitamin B1); Impaired Pyruvate Dehydrogenase, Alpha-Ketoglutarate Dehydrogenase, and Transketolase activity", True, None),
            ("Niacin (Vitamin B3); Impaired NAD+/NADH redox cycling", False, "Niacin deficiency causes Pellagra: 4 Ds (Diarrhea, Dermatitis on Casal necklace, Dementia, Death)."),
            ("Pyridoxine (Vitamin B6); Impaired transamination", False, "B6 deficiency causes sideroblastic anemia, convulsions, and peripheral neuropathy."),
            ("Riboflavin (Vitamin B2); Impaired FAD-dependent succinate dehydrogenase", False, "B2 deficiency causes angular cheilitis, glossitis, and magenta-colored tongue.")
        ],
        "pearl": "Thiamine (Vitamin B1) Deficiency Syndromes: Thiamine Pyrophosphate (TPP) is a required coenzyme for: 1. Pyruvate Dehydrogenase (link reaction) | 2. Alpha-Ketoglutarate Dehydrogenase (TCA cycle) | 3. Branched-Chain Alpha-Ketoacid Dehydrogenase | 4. TRANSKETOLASE (HMP Shunt; erythrocyte transketolase activity is the diagnostic test!). Syndromes: 1. Dry Beriberi: Symmetrical peripheral polyneuropathy (motor and sensory). 2. Wet Beriberi: High-output congestive heart failure + peripheral edema + dilated cardiomyopathy. 3. Wernicke's Encephalopathy: Acute, reversible triad: Confusion (encephalopathy) + Ataxia + Ophthalmoplegia/Nystagmus (mamillary bodies atrophy). 4. Korsakoff Psychosis: Chronic, irreversible: Anterograde amnesia + Confabulation. MANDATORY PROTOCOL: GIVE IV THIAMINE BEFORE GLUCOSE!",
        "citation": "Vasudevan's Textbook of Biochemistry, 9th Ed, Chapter 27 (Vitamins), p. 382-396.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Fat-Soluble & Water-Soluble Vitamin Deficiencies",
        "stem": (
            "A 3-year-old unimmunized child living in a refugee camp presents with night blindness (nyctalopia) and photophobia. "
            "On slit-lamp examination, the conjunctiva appears dry, lusterless, and wrinkled (conjunctival xerosis), "
            "with triangular, foamy, silvery-grey elevated plaques of keratinized desquamated epithelium located near the lateral limbus in the interpalpebral fissure. "
            "What is the name of this pathognomonic sign of Vitamin A deficiency?"
        ),
        "options": [
            ("Bitot's Spots", True, None),
            ("Brushfield's Spots", False, "Brushfield spots are white speckled spots on the iris seen in Down Syndrome (Trisomy 21)."),
            ("Roth's Spots", False, "Roth spots are retinal hemorrhages with pale white centers seen in Subacute Bacterial Endocarditis and leukemia."),
            ("Elschnig's Pearls", False, "Elschnig pearls are proliferations of residual lens epithelial cells after cataract surgery.")
        ],
        "pearl": "Vitamin A (Retinol) Deficiency Stages (WHO Classification): X1A: Conjunctival Xerosis (dryness). X1B: BITOT'S SPOTS (triangular, foamy, pearly-white/silvery plaques of keratinized squamous epithelium, usually bilateral and temporal). X2: Corneal Xerosis (hazy, dull cornea). X3A: Corneal Ulceration involving <1/3 of cornea. X3B: Keratomalacia (liquefactive stromal melting and perforation; irreversible blindness!). XN: Night Blindness (Nyctalopia; earliest functional manifestation due to defective Rhodopsin regeneration in retinal rods). XS: Corneal Scars. WHO Treatment Schedule: 200,000 IU orally on Day 1, Day 2, and Day 14 (100,000 IU for 6-11 months; 50,000 IU for <6 months).",
        "citation": "Park's Textbook of Preventive and Social Medicine, 26th Ed, Chapter 11 (Nutrition), p. 574-582.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Urea Cycle Disorders",
        "stem": (
            "A 3-day-old male newborn becomes progressively lethargic, feeds poorly, and develops rapid breathing (tachypnea) "
            "followed by hypothermia, seizures, and deep coma. Laboratory testing reveals severe hyperammonemia (plasma ammonia 980 umol/L, normal <50 umol/L) "
            "with respiratory alkalosis (pH 7.54, pCO2 24 mmHg). Plasma amino acid chromatography demonstrates markedly decreased serum Citrulline "
            "and undetectable Arginine. Urine organic acid analysis reveals MASSIVE urinary excretion of OROTIC ACID. "
            "What is the deficient enzyme in this most common X-linked Urea Cycle Disorder?"
        ),
        "options": [
            ("Ornithine Transcarbamylase (OTC deficiency, X-linked recessive)", True, None),
            ("Carbamoyl Phosphate Synthetase 1 (CPS-1 deficiency, autosomal recessive)", False, "CPS-1 deficiency presents identically with severe hyperammonemia, but has ZERO / LOW urinary orotic acid because carbamoyl phosphate is never synthesized."),
            ("Argininosuccinate Synthetase (Citrullinemia Type 1)", False, "Argininosuccinate synthetase deficiency causes massively ELEVATED plasma citrulline."),
            ("Arginase (Hyperargininemia)", False, "Arginase deficiency is milder, presenting in childhood with spastic diplegia and high arginine.")
        ],
        "pearl": "Urea Cycle Disorders Key Differential: Most Common UCD: ORNITHINE TRANSCARBAMYLASE (OTC) DEFICIENCY. UNIQUE FEATURE: Only urea cycle disorder that is X-LINKED RECESSIVE (all others are autosomal recessive!). Mechanism: OTC deficiency in mitochondria -> Carbamoyl Phosphate accumulates and spills out into the cytosol -> shunted into the de novo Pyrimidine synthesis pathway -> MASSIVE ACCUMULATION OF OROTIC ACID in urine! Differentiating OTC from CPS-1: OTC deficiency has HIGH URINE OROTIC ACID; CPS-1 deficiency has LOW/ABSENT urine orotic acid. (Both feature severe neonatal hyperammonemia and respiratory alkalosis due to ammonia stimulation of brainstem respiratory centers).",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 28 (Catabolism of Amino Acid Nitrogen), p. 268-278.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Urea Cycle Disorders",
        "stem": (
            "In patients with severe acute hyperammonemic crisis secondary to inborn errors of the urea cycle or decompensated liver disease, "
            "which nitrogen scavenger prodrug is administered intravenously to provide an alternative pathway for non-urea nitrogen excretion "
            "by conjugating with Glycine to form Hippuric Acid (excreted in urine)?"
        ),
        "options": [
            ("Sodium Benzoate", True, None),
            ("Sodium Phenylbutyrate (conjugates with Glutamine to form Phenylacetylglutamine)", False, "Sodium Phenylbutyrate/Phenylacetate conjugates with GLUTAMINE (removing 2 moles of nitrogen), not Glycine."),
            ("Lactulose", False, "Lactulose is an unabsorbable disaccharide in the colon that acidifies gut lumen to trap NH3 as NH4+, not a systemic glycine conjugator."),
            ("L-Carnitine", False, "L-carnitine is a carrier for fatty acid oxidation, not a glycine-conjugating nitrogen scavenger.")
        ],
        "pearl": "Nitrogen Scavenger Therapy in Hyperammonemia: 1. SODIUM BENZOATE: Combines with GLYCINE to form HIPPURATE (hippuric acid) -> cleared rapidly by renal tubular secretion (removes 1 mole of nitrogen per mole of benzoate). 2. SODIUM PHENYLACETATE / PHENYLBUTYRATE: Combines with GLUTAMINE to form PHENYLACETYLGLUTAMINE -> excreted in urine (removes 2 moles of nitrogen per mole of phenylbutyrate!). Dialysis (hemodialysis) is indicated if ammonia >500 umol/L or unresponsive to medical therapy.",
        "citation": "Vasudevan's Textbook of Biochemistry, 9th Ed, Chapter 15, p. 202-208.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Recombinant DNA Technology & PCR",
        "stem": (
            "In the molecular diagnostic technique of Polymerase Chain Reaction (PCR), a specific DNA segment is amplified exponentially. "
            "What is the precise temperature profile and sequence of the three thermal cycles typically executed "
            "in an automated thermocycler using thermostable Taq DNA polymerase?"
        ),
        "options": [
            ("Denaturation at 94°C-96°C -> Primer Annealing at 50°C-65°C -> Primer Extension at 72°C", True, None),
            ("Primer Annealing at 95°C -> Denaturation at 72°C -> Extension at 55°C", False, "High temperature (95°C) would melt primers away from template, preventing annealing."),
            ("Primer Extension at 95°C -> Annealing at 72°C -> Denaturation at 55°C", False, "Incorrect sequence."),
            ("Continuous incubation at 37°C for 24 hours without cycling", False, "Thermal cycling is the foundational mechanism of PCR.")
        ],
        "pearl": "Polymerase Chain Reaction (PCR) Steps: 1. DENATURATION (94-96°C): High temperature breaks hydrogen bonds between complementary base pairs, melting double-stranded DNA into single strands. 2. ANNEALING (50-65°C, typically Tm minus 5°C): Temperature lowered to allow forward and reverse oligonucleotide primers to hybridize specifically to target flanking sequences. 3. EXTENSION / ELONGATION (72°C): Optimum temperature for thermostable TAQ POLYMERASE (isolated from thermophilic bacterium Thermus aquaticus; lacks 3'->5' proofreading exonuclease activity) to synthesize complementary daughter strands in 5'->3' direction. Theoretical amplification after n cycles = 2^n.",
        "citation": "Harper's Illustrated Biochemistry, 32nd Ed, Chapter 39 (Molecular Genetics), p. 430-444.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Recombinant DNA Technology & PCR",
        "stem": (
            "In molecular biology laboratory techniques, different Blotting methods are utilized to detect specific macromolecules. "
            "According to the classic 'SNW DRP' (Snow Drop) mnemonic, which macromolecule is separated by gel electrophoresis "
            "and identified using labeled probes in SOUTHERN BLOT, NORTHERN BLOT, and WESTERN BLOT, respectively?"
        ),
        "options": [
            ("Southern Blot = DNA; Northern Blot = RNA; Western Blot = Protein", True, None),
            ("Southern Blot = RNA; Northern Blot = DNA; Western Blot = Lipids", False, "Southern blot was named after Edward Southern to detect DNA; Northern detects RNA."),
            ("Southern Blot = Protein; Northern Blot = RNA; Western Blot = DNA", False, "Western blot detects proteins using antibodies."),
            ("Southern Blot = Carbohydrates; Northern Blot = Proteins; Western Blot = RNA", False, "Incorrect macromolecular pairings.")
        ],
        "pearl": "Blotting Techniques Mnemonic: 'SNOW DROP' Mnemonic: S: Southern = D: DNA (Uses radiolabeled or fluorescent DNA probe) | N: Northern = R: RNA (Measures gene expression / mRNA levels) | O: (empty) = O: (empty) | W: Western = P: Protein (Uses labeled monoclonal/polyclonal Antibodies). Southwestern Blot: Detects DNA-binding proteins (e.g. Transcription factors like c-Jun, c-Fos, p53) using double-stranded DNA probes. Far-Western: Detects Protein-Protein interactions.",
        "citation": "Vasudevan's Textbook of Biochemistry, 9th Ed, Chapter 44 (Recombinant DNA), p. 580-588.",
        "difficulty": "easy"
    }
]
