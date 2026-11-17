"""
Authentic High-Yield NEET-PG Clinical Questions for Pediatrics
References: Nelson Textbook of Pediatrics (21st Ed), OP Ghai Essential Pediatrics (10th Ed)
"""

PEDIATRICS_QUESTIONS = [
    {
        "concept_name": "Core Principles: Motor & Social Developmental Milestones",
        "stem": (
            "A 9-month-old infant is brought to the well-child clinic for a routine developmental checkup. "
            "On physical examination, the infant sits steadily without support, transfers an object from one hand to the other, "
            "and babbles repetitive consonant-vowel combinations ('ba-ba', 'da-da'). When a small raisin is placed on the examination table, "
            "which of the following grasps is developmentally appropriate for this child's age?"
        ),
        "options": [
            ("Mature neat pincer grasp using fingertips", False, "Mature neat pincer grasp (using distal tips of thumb and index finger) develops at 12 months."),
            ("Inferior / crude pincer grasp using pads of index finger and thumb", True, None),
            ("Palmar grasp using the entire hand", False, "Crude palmar grasp is characteristic of 5-6 months of age."),
            ("Ulnar palmar grasp with thumb adducted", False, "Ulnar grasp is seen earliest at 4 months of age.")
        ],
        "pearl": "Developmental Milestones: 6 months: Palmar grasp & transfers objects | 9 months: Crude/inferior pincer grasp & sits unsupported | 12 months: Mature neat pincer grasp & walks with one hand held.",
        "citation": "OP Ghai Essential Pediatrics, 10th Ed, Chapter 2 (Development), p. 28-34.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Motor & Social Developmental Milestones",
        "stem": (
            "A concerned mother brings her 18-month-old toddler to the pediatric OPD. On developmental testing, the child can walk independently, "
            "runs stiffly, and builds a tower of 3 cubes. However, the mother is worried because the child only speaks 4 single words and cannot speak "
            "2-word meaningful sentences. At what chronological age should a normal child be able to construct 2-word phrases with a subject and verb?"
        ),
        "options": [
            ("15 months", False, "At 15 months, a child typically uses 4-6 words and points to demands."),
            ("18 months", False, "At 18 months, vocabulary is ~10-20 words, but joining words into phrases is not yet expected."),
            ("24 months (2 years)", True, None),
            ("36 months (3 years)", False, "At 36 months (3 years), a child speaks full sentences and tells their name/age/gender.")
        ],
        "pearl": "Language Milestones: 12 months: 1-2 words with meaning | 18 months: 8-10 words | 24 months (2 yrs): 2-word telegraphic phrases ('want milk') | 36 months (3 yrs): 3-word sentences & speaks gender/age.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 15 (Developmental Assessment), p. 88-94.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Assessment of Short Stature",
        "stem": (
            "A 14-year-old boy is brought by his parents because he is significantly shorter than all his classmates. Physical examination shows a height "
            "below the 3rd percentile for age. Upper-to-lower segment ratio is normal. Systemic examination is unremarkable, and sexual maturity rating is Tanner Stage 1. "
            "Left wrist radiograph reveals a bone age of 11.5 years (delayed by 2.5 years compared to chronological age). His annual growth velocity is 5.2 cm/year (normal). "
            "His father had a late growth spurt during college. What is the most likely diagnosis?"
        ),
        "options": [
            ("Constitutional Delay of Growth and Puberty (CDGP)", True, None),
            ("Familial / Genetic Short Stature", False, "In Familial Short Stature, bone age matches chronological age (Bone Age = Chronological Age) and final adult height remains below target."),
            ("Growth Hormone Deficiency", False, "Growth Hormone deficiency typically features subnormal growth velocity (<4 cm/year), truncal adiposity, and micropenis."),
            ("Achondroplasia", False, "Achondroplasia is a disproportionate short stature condition with rhizomelic limb shortening and prominent frontal bossing.")
        ],
        "pearl": "Short Stature Golden Rule: Constitutional Delay: Bone Age < Chronological Age, normal growth velocity, late bloomer history, adult height normal. Familial Short Stature: Bone Age = Chronological Age, normal velocity, adult height short.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 581 (Disorders of Growth), p. 2871-2878.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Assessment of Short Stature",
        "stem": (
            "A 10-year-old girl is evaluated for short stature (height <3rd percentile). Clinical examination reveals a low posterior hairline, broad chest with widely spaced nipples, "
            "cubitus valgus deformity, and a high-arched palate. She has no intellectual disability. Transthoracic echocardiography is ordered as part of her diagnostic workup. "
            "Which cardiovascular lesion is most frequently associated with this patient's underlying condition?"
        ),
        "options": [
            ("Ventricular Septal Defect (VSD)", False, "VSD is the most common overall congenital heart disease, but not specific for Turner syndrome."),
            ("Bicuspid Aortic Valve and Coarctation of the Aorta", True, None),
            ("Tetralogy of Fallot", False, "Tetralogy of Fallot is classically associated with DiGeorge syndrome (22q11 deletion) and Down syndrome."),
            ("Endocardial Cushion Defect (AVSD)", False, "Atrioventricular septal defect is pathognomonic for Trisomy 21 (Down syndrome).")
        ],
        "pearl": "Turner Syndrome (45,X0): Most common cardiac anomaly overall: Bicuspid Aortic Valve (30-50%); Most characteristic/tested structural lesion: Coarctation of Aorta; Renal: Horseshoe kidney.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 594 (Turner Syndrome), p. 2932-2936.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Severe Acute Malnutrition (SAM) Protocols",
        "stem": (
            "A 2-year-old child weighing 6.8 kg is brought to the malnutrition treatment center with severe wasting (weight-for-height < -3 Z-scores) and bilateral pitting pedal edema. "
            "On admission, the child is lethargic with a rectal temperature of 35.1°C (hypothermia). According to WHO guidelines for the initial stabilization phase of Severe Acute Malnutrition (SAM), "
            "which of the following initial management steps is CONTRAINDICATED?"
        ),
        "options": [
            ("Administration of 10% dextrose orally or by nasogastric tube", False, "10% dextrose is essential immediately to prevent fatal hypoglycemia (<54 mg/dL)."),
            ("Immediate active rewarming with skin-to-skin contact or a warm blanket", False, "Active rewarming is crucial for hypothermia (rectal temp <35.5°C)."),
            ("Empiric oral iron supplementation during the first 48 hours", True, None),
            ("Empiric broad-spectrum antibiotic therapy with ampicillin and gentamicin", False, "All SAM children have occult infections and must receive empiric antibiotics on admission.")
        ],
        "pearl": "WHO 10 Steps for SAM: Step 1: Hypoglycemia -> Step 2: Hypothermia -> Step 3: Dehydration (ReSoMal) -> Step 4: Electrolytes -> Step 5: Infection (Antibiotics). NEVER GIVE IRON IN STABILIZATION PHASE; iron is toxic to the stressed liver and promotes bacterial proliferation. Start iron only in the rehabilitation phase!",
        "citation": "OP Ghai Essential Pediatrics, 10th Ed, Chapter 6 (Nutrition), p. 112-118.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Severe Acute Malnutrition (SAM) Protocols",
        "stem": (
            "A 15-month-old child with severe acute malnutrition is being treated in the stabilization phase with starter formula F-75. "
            "Why is F-75 formula specifically designed with low protein (0.9 g/100 mL) and low sodium compared to standard catch-up feeds (F-100)?"
        ),
        "options": [
            ("Because children with SAM cannot digest lipids", False, "Lipids are tolerated; protein and sodium are restricted to avoid overload."),
            ("To prevent congestive cardiac failure and acute osmotic shifts due to impaired renal and hepatic reserve", True, None),
            ("To promote rapid hyperplastic muscle mass hypertrophy", False, "F-75 is NOT for rapid weight gain; F-100 is the catch-up growth formula in the rehabilitation phase."),
            ("Because lactose induces severe hypoglycemia in malnourished children", False, "Lactose intolerance can occur, but low sodium/protein is to prevent fatal congestive heart failure.")
        ],
        "pearl": "F-75 vs F-100: F-75 (Stabilization phase): 75 kcal/100 mL, 0.9 g protein/100 mL, low sodium. Designed for maintenance without overloading heart or kidneys. F-100 (Catch-up phase): 100 kcal/100 mL, 2.9 g protein/100 mL, promotes rapid weight gain.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 57 (Malnutrition), p. 342-348.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Neonatal Resuscitation Program (NRP) Guidelines",
        "stem": (
            "A full-term infant is delivered by emergency cesarean section due to fetal distress. At birth, the baby is limp, apneic, and cyanotic. "
            "The resuscitation team completes the initial steps (warm, dry, stimulate, clear secretions) within 30 seconds. The heart rate is evaluated by auscultation "
            "and found to be 72 beats/min. What is the single most appropriate immediate next step according to the Neonatal Resuscitation Program (NRP 8th edition) guidelines?"
        ),
        "options": [
            ("Initiate Positive Pressure Ventilation (PPV) with room air (21% O2)", True, None),
            ("Immediately begin synchronized chest compressions at a 3:1 ratio", False, "Chest compressions are indicated ONLY if heart rate remains <60 bpm after 30 seconds of effective PPV with chest movement."),
            ("Administer intravenous epinephrine 0.02 mg/kg via umbilical venous catheter", False, "Epinephrine is indicated only if HR <60 bpm despite effective PPV + chest compressions."),
            ("Apply continuous positive airway pressure (CPAP) at 5 cm H2O", False, "CPAP is used for spontaneously breathing infants with respiratory distress, NOT for an apneic infant with HR <100 bpm.")
        ],
        "pearl": "NRP Golden Rule: If newborn is apneic/gasping OR Heart Rate < 100 bpm after 30s initial steps -> START PPV immediately! Chest compressions are only started if HR < 60 bpm after 30s of effective PPV with chest rise. Compression:Ventilation ratio = 3:1.",
        "citation": "American Heart Association / AAP Neonatal Resuscitation Guidelines (8th Ed), 2021 / Nelson Ch 114.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Neonatal Resuscitation Program (NRP) Guidelines",
        "stem": (
            "During neonatal resuscitation of a preterm infant (28 weeks gestation), effective positive pressure ventilation has been delivered for 30 seconds, "
            "followed by 60 seconds of coordinated chest compressions with 100% oxygen. The heart rate remains persistent at 48 beats/min. "
            "Which drug, route, and concentration is recommended by current NRP guidelines?"
        ),
        "options": [
            ("Atropine 0.02 mg/kg via endotracheal tube", False, "Atropine is not used in neonatal resuscitation; bradycardia in neonates is almost exclusively hypoxic in origin."),
            ("Epinephrine (1:10,000 / 0.1 mg/mL) 0.02 mg/kg intravenously or intraosseously", True, None),
            ("Sodium bicarbonate 1 mEq/kg rapid IV push", False, "Sodium bicarbonate is not routinely recommended and can worsen intracellular acidosis."),
            ("Calcium chloride 20 mg/kg via peripheral vein", False, "Calcium is indicated only in documented hypocalcemia, hyperkalemia, or hypermagnesemia.")
        ],
        "pearl": "NRP Medication: Epinephrine 1:10,000 (0.1 mg/mL) IV/IO dose: 0.02 mg/kg (0.2 mL/kg), followed by 3 mL normal saline flush. Endotracheal route is less effective and requires higher dose (0.05-0.1 mg/kg) only while IV access is being obtained.",
        "citation": "AHA/AAP NRP Guidelines 8th Edition, Circulation 2021; Nelson Ch 114.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Respiratory Distress Syndrome & Surfactant",
        "stem": (
            "A preterm male infant is born at 29 weeks of gestation to a 24-year-old primigravida who received no antenatal corticosteroids. "
            "Within 30 minutes of life, the neonate develops tachypnea (respiratory rate 76/min), prominent subcostal and intercostal retractions, "
            "expiratory grunting, and central cyanosis. Chest radiography reveals diffuse reticulogranular 'ground-glass' opacities with prominent air bronchograms "
            "and low lung volumes. What is the primary biochemical deficiency underlying this neonate's respiratory failure?"
        ),
        "options": [
            ("Alpha-1 antitrypsin deficiency", False, "Alpha-1 antitrypsin deficiency causes emphysema in young adults and neonatal cholestasis, not neonatal RDS."),
            ("Dipalmitoylphosphatidylcholine (surfactant lecithin) deficiency produced by Type II pneumocytes", True, None),
            ("Type I collagen cross-linking failure in alveolar basement membranes", False, "Type I collagen defects cause osteogenesis imperfecta."),
            ("Ciliary dynein arm deficiency causing impaired mucociliary clearance", False, "Dynein arm defects cause Primary Ciliary Dyskinesia / Kartagener syndrome.")
        ],
        "pearl": "Neonatal RDS (Hyaline Membrane Disease): Prematurity (<32 weeks) -> Type II pneumocytes fail to synthesize surfactant (Dipalmitoylphosphatidylcholine) -> alveolar collapse (atelectasis) -> CXR: Ground glass haziness + Air bronchograms. Antenatal prevention: Betamethasone 12 mg IM 24h apart.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 120 (Hyaline Membrane Disease), p. 892-898.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Respiratory Distress Syndrome & Surfactant",
        "stem": (
            "A 28-week preterm neonate with severe respiratory distress syndrome is maintained on nasal continuous positive airway pressure (nCPAP). "
            "Despite CPAP of 6 cm H2O and FiO2 of 0.45, arterial blood gas demonstrates worsening hypoxemic respiratory acidosis. "
            "The team decides to administer exogenous natural surfactant using the LISA (Less Invasive Surfactant Administration) technique. "
            "What is the key clinical advantage of LISA over the traditional INSURE (Intubate-Surfactant-Extubate) method?"
        ),
        "options": [
            ("Eliminates the requirement for radiant warmers", False, "Radiant warmers are always required for thermoregulation in preterm infants."),
            ("Avoids endotracheal mechanical positive pressure ventilation, thereby reducing ventilator-induced lung injury (VILI) and bronchopulmonary dysplasia (BPD)", True, None),
            ("Permits simultaneous administration of oral broad-spectrum antibiotics", False, "Surfactant is instilled intratracheally, not related to oral antibiotics."),
            ("Guarantees permanent closure of the ductus arteriosus within 6 hours", False, "Surfactant reduces pulmonary vascular resistance, which may actually increase left-to-right ductal shunting temporarily.")
        ],
        "pearl": "LISA (Less Invasive Surfactant Administration): Surfactant instilled via a thin catheter into the trachea while the infant remains breathing spontaneously on CPAP. Avoids endotracheal intubation and mechanical ventilation, significantly reducing Bronchopulmonary Dysplasia (BPD).",
        "citation": "European Consensus Guidelines on Management of RDS (2022 Update) / Nelson Ch 120.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Neonatal Jaundice: Phototherapy & Exchange",
        "stem": (
            "A healthy full-term female neonate (birth weight 3.2 kg) is born to an O-negative mother and an A-positive father. "
            "At 18 hours of life, the neonate is noticed to have deep yellowish discoloration of the face, trunk, and lower limbs. "
            "Serum total bilirubin is 14.8 mg/dL with a direct fraction of 0.6 mg/dL. Direct Antiglobulin (Coombs) test is strongly positive. "
            "What is the most likely diagnosis and the single most appropriate initial management step?"
        ),
        "options": [
            ("Physiological jaundice; advise frequent breastfeeding and observe", False, "Jaundice appearing within the FIRST 24 HOURS of life is ALWAYS PATHOLOGICAL, never physiological!"),
            ("ABO / Rh hemolytic disease of the newborn; initiate intensive double-surface phototherapy immediately", True, None),
            ("Breast milk jaundice; discontinue breastfeeding for 48 hours", False, "Breast milk jaundice appears in the late 1st or 2nd week of life, never in the first 24 hours."),
            ("Biliary atresia; arrange urgent exploratory laparotomy and Kasai portoenterostomy", False, "Biliary atresia presents with conjugated (direct) hyperbilirubinemia, pale acholic stools, and dark urine after 2-4 weeks of life.")
        ],
        "pearl": "Neonatal Jaundice Golden Rules: Jaundice < 24 hours of life = ALWAYS PATHOLOGICAL (most common cause: Rh or ABO hemolytic disease). Phototherapy: Blue-green light (wavelength 460-490 nm) converts toxic unconjugated bilirubin into water-soluble Lumirubin via structural isomerization.",
        "citation": "OP Ghai Essential Pediatrics, 10th Ed, Chapter 8 (Neonatal Disorders), p. 182-190.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Neonatal Jaundice: Phototherapy & Exchange",
        "stem": (
            "A 3-day-old neonate with severe Rh hemolytic disease has a total serum bilirubin of 26 mg/dL despite intensive phototherapy for 6 hours. "
            "The infant exhibits lethargy, poor feeding, high-pitched crying, and intermittent retrocollis/opisthotonus (early signs of acute bilirubin encephalopathy). "
            "Double-volume exchange transfusion is scheduled immediately. Which blood product combination should be selected for exchange transfusion in this infant?"
        ),
        "options": [
            ("O-negative packed red cells suspended in AB-positive fresh frozen plasma", True, None),
            ("Mother's own whole blood crossmatched against the baby", False, "Mother's blood contains anti-Rh antibodies that would destroy remaining baby RBCs."),
            ("Baby's own blood group (A-positive) whole blood", False, "A-positive RBCs would be rapidly hemolyzed by circulating maternal anti-Rh and anti-A antibodies."),
            ("AB-negative whole blood without crossmatching", False, "AB red cells contain A and B antigens which would react with maternal antibodies.")
        ],
        "pearl": "Exchange Transfusion Blood Selection: For Rh incompatibility: O-negative RBCs suspended in AB plasma (or Rh-negative blood compatible with mother). For ABO incompatibility: O-group RBCs (Rh compatible with infant) in AB plasma. Exchange volume = 2 x blood volume = 2 x 80 mL/kg = 160 mL/kg.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 123 (Hyperbilirubinemia), p. 918-925.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Measles, Mumps & Rubella Complications",
        "stem": (
            "A 3-year-old unimmunized child is brought with high fever (103°F), coryza, conjunctivitis with marked photophobia, and a barking cough for 4 days. "
            "On physical examination, the pediatrician notices tiny 1-mm bluish-white spots surrounded by an erythematous areola on the buccal mucosa opposite the lower molars. "
            "Over the next 24 hours, a maculopapular blanching rash erupts beginning behind the ears and at the hairline, spreading downward to the face, trunk, and extremities. "
            "Which of the following interventions has been proven to significantly reduce morbidity and mortality from this infection in children?"
        ),
        "options": [
            ("Intravenous Acyclovir 10 mg/kg/dose every 8 hours", False, "Acyclovir is an anti-herpetic agent with no antiviral activity against the Measles paramyxovirus."),
            ("High-dose oral Vitamin A supplementation on days 1 and 2", True, None),
            ("Empiric oral Oseltamivir 30 mg twice daily for 5 days", False, "Oseltamivir is a neuraminidase inhibitor effective only against Influenza viruses."),
            ("Intravenous immunoglobulin (IVIG) 2 g/kg over 12 hours", False, "Routine IVIG is not standard therapy for acute measles; Vitamin A is the WHO standard of care.")
        ],
        "pearl": "Measles (Rubeola): 3 Cs: Cough, Coryza, Conjunctivitis | Koplik spots (pathognomonic): buccal mucosa opposite lower 2nd molars | Rash: Cephalocaudal spread, fades with desquamation/hyperpigmentation. WHO Management: Vitamin A (50,000 IU <6mo; 100,000 IU 6-11mo; 200,000 IU ≥12mo) on 2 consecutive days reduces mortality by 50%!",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 271 (Measles), p. 1622-1628.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Measles, Mumps & Rubella Complications",
        "stem": (
            "A 9-year-old boy is brought to the neurology clinic due to progressive intellectual decline, behavioral outbursts, and recurrent myoclonic jerks over the past 4 months. "
            "He had a severe bout of natural measles at 11 months of age. Electroencephalogram (EEG) shows periodic high-voltage complexes (Radermecker complexes) recurring every 4-10 seconds. "
            "Lumbar puncture demonstrates elevated anti-measles IgG antibodies in the cerebrospinal fluid. What is the diagnosis?"
        ),
        "options": [
            ("Post-measles acute disseminated encephalomyelitis (ADEM)", False, "ADEM occurs within 1-2 weeks after the acute exanthem as an autoimmune demyelinating process, not 8 years later."),
            ("Subacute Sclerosing Panencephalitis (SSPE)", True, None),
            ("Subacute Combined Degeneration of the spinal cord", False, "Subacute combined degeneration is caused by Vitamin B12 deficiency affecting dorsal and lateral columns."),
            ("Herpes simplex virus (HSV-1) encephalitis", False, "HSV-1 encephalitis presents acutely with fever, temporal lobe seizures, and hemorrhagic necrosis.")
        ],
        "pearl": "SSPE (Dawson Disease): Delayed neurodegenerative complication of measles (latent period 6-8 years). Defective measles virus persists in CNS. Triad: Intellectual decline + Myoclonic jerks + Periodic slow complexes on EEG (Radermecker complexes) + High CSF measles antibody titers.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 271, p. 1628; Ghai Ch 12.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Kawasaki Disease Diagnostic Criteria",
        "stem": (
            "A 3-year-old girl presents with high spiking fevers (up to 104°F) refractory to paracetamol and ibuprofen for the past 6 days. "
            "On physical examination, the physician notes bilateral non-purulent bulbar conjunctival injection, a prominent 'strawberry tongue' with fissured erythematous lips, "
            "firm indurative edema of the hands and feet, a polymorphous maculopapular rash over the trunk, and a single enlarged tender anterior cervical lymph node measuring 2.2 cm. "
            "What is the most critical coronary complication to prevent, and what is the definitive first-line therapeutic regimen?"
        ),
        "options": [
            ("Coronary artery aneurysms; Intravenous Immunoglobulin (IVIG 2 g/kg single infusion) plus high-dose Aspirin", True, None),
            ("Mitral valve prolapse; Oral Prednisolone 2 mg/kg/day for 6 weeks", False, "Corticosteroids alone as initial therapy are not standard and may increase aneurysm rupture if used without IVIG."),
            ("Aortic valve stenosis; Intravenous Ampicillin plus Gentamicin for 14 days", False, "Kawasaki disease is an acute systemic necrotizing vasculitis, not a bacterial infection."),
            ("Constrictive pericarditis; Intravenous Infliximab alone as first-line monotherapy", False, "Infliximab is reserved for IVIG-resistant refractory Kawasaki disease, not as the primary first-line therapy.")
        ],
        "pearl": "Kawasaki Disease (Mucocutaneous Lymph Node Syndrome): Diagnosis requires Fever ≥5 days + at least 4 of 5 (CRASH): Conjunctivitis (bilateral painless limbal sparing) | Rash (polymorphous non-vesicular) | Adenopathy (cervical >1.5 cm, usually unilateral) | Strawberry tongue/lip erythema | Hand/foot changes (indurative edema/periungual desquamation). Treatment: IVIG (2 g/kg) + Aspirin within 10 days reduces coronary aneurysms from 25% to <4%!",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 198 (Kawasaki Disease), p. 1248-1254.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Pediatric Nephrotic Syndrome & Steroid Regimens",
        "stem": (
            "A 4-year-old boy presents with progressive generalized swelling that began as morning periorbital puffiness 2 weeks ago and progressed to bilateral pitting pedal edema and ascites. "
            "Blood pressure is normal (96/60 mmHg). Urinalysis demonstrates 4+ proteinuria without hematuria (no RBCs or RBC casts). "
            "24-hour urine protein is 68 mg/m2/hour (nephrotic range >40 mg/m2/h). Serum albumin is 1.6 g/dL and serum total cholesterol is 380 mg/dL. Renal function tests are normal. "
            "What is the most likely renal pathology and the standard first-line treatment regimen recommended by Indian Academy of Pediatrics (IAP) / KDIGO guidelines?"
        ),
        "options": [
            ("Membranous nephropathy; Intravenous Cyclophosphamide pulses", False, "Membranous nephropathy is rare in young children; typical in adults."),
            ("Minimal Change Disease; Oral Prednisolone at 60 mg/m2/day (or 2 mg/kg/day, max 60 mg) for 6 weeks, followed by 40 mg/m2 alternate days for 6 weeks", True, None),
            ("Post-streptococcal glomerulonephritis; Oral Furosemide plus Penicillin V for 10 days", False, "PSGN presents with nephritic syndrome: gross hematuria (coca-cola urine), hypertension, and oliguria, not pure nephrotic syndrome."),
            ("Focal Segmental Glomerulosclerosis; Immediate renal biopsy prior to starting any medical therapy", False, "In children aged 1-8 years with steroid-responsive nephrotic features, routine initial renal biopsy is NOT indicated because >85% have Minimal Change Disease.")
        ],
        "pearl": "Pediatric Nephrotic Syndrome: Minimal Change Disease (MCD) accounts for 85-90% of cases in children aged 1-8 years. Electron microscopy shows diffuse effacement of visceral epithelial podocyte foot processes. Standard IAP Regimen: Oral Prednisolone 60 mg/m2/day (single morning dose) x 6 weeks -> 40 mg/m2 alternate days x 6 weeks. Total initial course = 12 weeks.",
        "citation": "IAP Consensus Guidelines on Management of Steroid-Sensitive Nephrotic Syndrome / Ghai Ch 17, p. 488-496.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Pediatric Sepsis & Febrile Seizures",
        "stem": (
            "A 20-month-old previously healthy boy is brought to the emergency department following a generalized tonic-clonic convulsion that lasted approximately 3 minutes. "
            "The seizure occurred during a rapid rise in body temperature to 102.8°F caused by an acute viral upper respiratory infection. "
            "In the casualty, the child is fully conscious, playful, and neurologically normal. There is no neck stiffness or Kernig sign, and the anterior fontanelle is closed. "
            "This is his first seizure episode. Which of the following features confirms the diagnosis of a Simple (Typical) Febrile Seizure?"
        ),
        "options": [
            ("Focal seizure onset with post-ictal Todd's paresis lasting 6 hours", False, "Focal features or post-ictal neurological deficits classify the seizure as Complex (Atypical), not simple."),
            ("Generalized onset, duration <15 minutes, non-recurrent within 24 hours, and complete return to normal baseline within minutes", True, None),
            ("Prolonged duration >20 minutes requiring rectal diazepam", False, "Duration >15 minutes is a criteria for Complex Febrile Seizure / febrile status epilepticus."),
            ("Family history of Dravet syndrome and abnormal interictal EEG", False, "Simple febrile seizures require no routine EEG or neuroimaging.")
        ],
        "pearl": "Simple vs Complex Febrile Seizures: Simple: Generalized, <15 minutes duration, occurs once in 24 hours, no neurological deficit. Complex: Focal onset, prolonged >15 minutes, repeats within 24 hours, or has post-ictal Todd's palsy. Simple febrile seizures carry an excellent prognosis; routine LP/EEG/CT is NOT indicated.",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 610 (Febrile Seizures), p. 3085-3088.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Congenital Infections (TORCH)",
        "stem": (
            "A newborn infant delivered at 37 weeks is found to be small for gestational age (birth weight 1.9 kg). "
            "Physical examination reveals microcephaly, hepatosplenomegaly, jaundice, and a diffuse petechial/purpuric 'blueberry muffin' skin rash. "
            "Sensorineural hearing loss is detected on automated auditory brainstem response (AABR). Non-contrast cranial computed tomography (CT) reveals "
            "extensive periventricular intracranial calcifications outlining the lateral ventricles. What is the most likely causative pathogen?"
        ),
        "options": [
            ("Toxoplasma gondii", False, "Congenital Toxoplasmosis typically causes DIFFUSE, scattered parenchymal calcifications + Chorioretinitis + Hydrocephalus (Classic Sabin Triad)."),
            ("Cytomegalovirus (CMV)", True, None),
            ("Rubella virus", False, "Congenital Rubella Triad: Cataracts/Microphthalmia + Sensorineural deafness + Congenital heart defect (Patent Ductus Arteriosus / Pulmonary artery stenosis)."),
            ("Herpes Simplex Virus (HSV-2)", False, "Congenital/neonatal HSV typically causes vesicular skin lesions, keratoconjunctivitis, and hemorrhagic temporal lobe encephalitis.")
        ],
        "pearl": "TORCH Calcifications Key Differential: CMV (most common congenital infection): PERIVENTRICULAR calcifications + Microcephaly + Sensorineural deafness. Toxoplasmosis: DIFFUSE/SCATTERED intracranial calcifications + Hydrocephalus + Chorioretinitis (Sabin Triad).",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 260 (Cytomegalovirus), p. 1564-1570.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Acyanotic vs Cyanotic Congenital Heart Diseases",
        "stem": (
            "A 2-year-old boy is brought to the pediatric clinic by his mother because he frequently assumes a squatting posture after running in the playground. "
            "The mother also reports episodes where the child becomes acutely agitated, deeply blue, and breathes heavily ('tet spells'). "
            "On cardiac auscultation, there is a harsh single second heart sound and a grade 3/6 ejection systolic murmur loudest at the upper left sternal border. "
            "Chest radiography reveals a boot-shaped heart (coeur en sabot) with pulmonary oligemia. By what physiological mechanism does squatting alleviate hypoxemia during a cyanotic spell?"
        ),
        "options": [
            ("Decreases systemic venous return to the right atrium", False, "Squatting increases, rather than decreases, systemic venous return."),
            ("Increases Systemic Vascular Resistance (SVR), thereby reducing right-to-left shunting across the VSD and forcing more blood through the stenotic pulmonary outflow tract", True, None),
            ("Causes acute dilatation of the infundibular pulmonary stenosis", False, "Squatting has no direct muscular relaxant effect on the infundibular myocardium; beta-blockers reduce infundibular spasm."),
            ("Decreases left ventricular afterload, promoting rapid peripheral pooling", False, "Decreased LV afterload would worsen right-to-left shunting and deepen cyanosis.")
        ],
        "pearl": "Tetralogy of Fallot (TOF): 4 Components: 1. Pulmonary infundibular stenosis (determines severity) | 2. RV hypertrophy | 3. Overriding aorta | 4. Large VSD. Squatting increases SVR (systemic vascular resistance) -> Left ventricular pressure exceeds RV pressure -> reduces right-to-left shunt -> forces more desaturated blood through the lungs!",
        "citation": "Nelson Textbook of Pediatrics, 21st Ed, Chapter 458 (Tetralogy of Fallot), p. 2352-2358.",
        "difficulty": "moderate"
    }
]
