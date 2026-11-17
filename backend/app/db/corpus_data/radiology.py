"""
Authentic High-Yield NEET-PG Clinical Questions for Radiodiagnosis
References: Sutton's Textbook of Radiology (7th Ed), Grainger & Allison's Diagnostic Radiology (7th Ed)
"""

RADIOLOGY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Chest X-Ray Signs (Sail, Silhouette, Deep Sulcus)",
        "stem": (
            "A 58-year-old chronic smoker presents with severe cough, hemoptysis, and progressive dyspnea for 6 weeks. "
            "Posteroanterior (PA) chest radiograph reveals right upper lobe atelectasis with elevation of the horizontal (minor) fissure. "
            "The medial aspect of the minor fissure is convex inferiorly due to a centrally located hilar mass, while the lateral aspect is concave superiorly "
            "due to the collapsed right upper lobe parenchyma, producing a characteristic reverse 'S' contour. "
            "What is the classical eponymous radiographic sign demonstrated, and what is the underlying diagnosis?"
        ),
        "options": [
            ("Golden S Sign (Reverse S Sign of Golden); Central Bronchogenic Carcinoma with right upper lobe collapse", True, None),
            ("Westermark Sign; Acute Massive Pulmonary Embolism", False, "Westermark sign is localized oligemia / hyperlucency distal to an occluded pulmonary artery in PE."),
            ("Hampton Hump; Peripheral wedge-shaped pulmonary infarction", False, "Hampton hump is a peripheral, pleural-based wedge-shaped opacity with its rounded apex pointing toward the hilum."),
            ("Silhouette Sign; Right middle lobe consolidation effacing the right heart border", False, "Silhouette sign is loss of a normal cardiac or diaphragmatic contour due to an adjacent soft tissue opacity of identical density.")
        ],
        "pearl": "Golden S Sign of Golden: Seen on PA chest radiograph. Produced by right upper lobe (RUL) collapse around a centrally obstructing hilar mass (most commonly Squamous Cell Carcinoma or Small Cell Carcinoma of the right main/upper bronchus). The minor fissure forms an 'S' shape: Lateral concave part = collapsed RUL; Medial convex part = central hilar tumor mass.",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 5 (Chest Radiology), p. 112-124.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Chest X-Ray Signs (Sail, Silhouette, Deep Sulcus)",
        "stem": (
            "A 32-year-old male involved in a high-speed motor vehicle collision is brought to the emergency trauma bay on a spine board. "
            "He has multiple rib fractures and subcutaneous emphysema over the left chest wall. "
            "Because of spinal precautions, a supine anteroposterior (AP) chest radiograph is obtained. "
            "The radiograph demonstrates a dramatically deepened, lucent, and sharp left costophrenic sulcus extending into the left upper quadrant. "
            "What is this classic supine radiologic sign of pneumothorax?"
        ),
        "options": [
            ("Deep Sulcus Sign", True, None),
            ("Continuous Diaphragm Sign", False, "Continuous diaphragm sign is seen in pneumomediastinum when air outlines the entire superior surface of the central diaphragm beneath the heart."),
            ("Spinnaker Sail Sign (Angel Wing Sign)", False, "Spinnaker sail sign is elevation of the thymic lobes by pneumomediastinum in neonates."),
            ("Fallen Lung Sign", False, "Fallen lung sign is seen in complete tracheobronchial rupture where the collapsed lung falls laterally and dependently into the costophrenic angle.")
        ],
        "pearl": "Supine Pneumothorax Signs: In a supine patient, pleural air does not collect at the lung apex (as it does upright); instead, air rises to the lowest, most non-dependent anterior and inferior costophrenic sulcus -> DEEP SULCUS SIGN (abnormally deepened, lucent, sharp costophrenic angle). Other signs: Double diaphragm sign, sharp pericardial border, hyperlucent hemithorax.",
        "citation": "Sutton's Textbook of Radiology, 7th Ed, Chapter 2 (Trauma Imaging), p. 48-56.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Non-Contrast Head CT in Stroke & Hemorrhage",
        "stem": (
            "A 24-year-old motorcyclist without a helmet collides with a guardrail, loses consciousness for 5 minutes, and then recovers "
            "to normal awareness, conversing lucidly with emergency medical technicians ('lucid interval'). "
            "Two hours later in the emergency observation unit, he rapidly becomes obtunded with a dilated, unreactive right pupil and left hemiparesis. "
            "Emergency Non-Contrast Computed Tomography (NCCT) of the brain reveals a well-defined, hyperdense, biconvex (lenticular) collection "
            "in the right temporoparietal region that DOES NOT cross the cranial suture lines. What is the diagnosis and the ruptured vessel?"
        ),
        "options": [
            ("Epidural Hematoma (EDH); Middle Meningeal Artery tear beneath the Pterion", True, None),
            ("Subdural Hematoma (SDH); Bridging cortical veins", False, "Subdural hematoma appears as a CRESCENTIC, concave collection that CAN cross suture lines and is bounded by dural reflections."),
            ("Subarachnoid Hemorrhage (SAH); Ruptured anterior communicating artery aneurysm", False, "SAH fills the basal cisterns, sylvian fissures, and sulci with hyperattenuating blood."),
            ("Intraventricular Hemorrhage; Choroid plexus angioma", False, "Intraventricular hemorrhage layers within the occipital horns of lateral ventricles.")
        ],
        "pearl": "Intracranial Hemorrhages on NCCT: 1. Epidural Hematoma (EDH): Biconvex / Lenticular, hyperdense, arterial (Middle Meningeal Artery via Foramen Spinosum beneath Pterion), DOES NOT cross suture lines (dura firmly adherent at sutures), can cross midline/falx. Classic: Lucid Interval. 2. Subdural Hematoma (SDH): Crescentic, concave, venous (Bridging cortical veins to Superior Sagittal Sinus), CROSSES suture lines, DOES NOT cross midline/falx.",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 48 (Neuroimaging in Trauma), p. 1290-1305.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Non-Contrast Head CT in Stroke & Hemorrhage",
        "stem": (
            "A 68-year-old male presents to the stroke unit 90 minutes after sudden-onset left hemiplegia and left facial droop. "
            "Immediate Non-Contrast Head CT is performed to determine eligibility for intravenous recombinant tissue plasminogen activator (IV tPA). "
            "Which of the following early ischemic signs on NCCT indicates acute thromboembolic occlusion of the M1 segment of the Middle Cerebral Artery (MCA)?"
        ),
        "options": [
            ("Dense Middle Cerebral Artery Sign (Hyperdense MCA Sign)", True, None),
            ("Periventricular hyperdense halo", False, "Periventricular hyperdensity is not a feature of acute thromboembolism; leukoaraiosis is hypodense on CT."),
            ("Target sign of ring enhancement", False, "Ring enhancement requires intravenous iodinated contrast and indicates subacute infarct, abscess, or tumor."),
            ("Hyperdense temporal horn dilatation", False, "Ventricles are CSF-density (hypodense ~0-10 HU); acute blood in ventricles indicates IVH, not MCA clot.")
        ],
        "pearl": "Early NCCT Signs of Acute Ischemic Stroke (<6 hours): 1. Hyperdense MCA Sign (direct visualization of acute thromboembolus in M1 vessel lumen; earliest sign) | 2. Loss of insular ribbon (blurring of gray-white junction of insular cortex) | 3. Obscuration / loss of lentiform nucleus margins | 4. Sulcal effacement due to cytotoxic edema. Remember: NCCT is primarily performed to EXCLUDE intracranial hemorrhage before administering IV tPA (<4.5 hours)!",
        "citation": "Sutton's Textbook of Radiology, 7th Ed, Chapter 42 (Stroke Imaging), p. 1180-1192.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: MRI Sequences (T1, T2, FLAIR, DWI)",
        "stem": (
            "A 55-year-old female presents with acute right-sided numbness and aphasia that started 45 minutes ago. "
            "Non-contrast CT of the brain shows no hemorrhage and no early ischemic changes. "
            "Brain Magnetic Resonance Imaging (MRI) is performed immediately. Which specialized MRI sequence is the most sensitive and earliest "
            "modality to detect hyperacute cerebral ischemia (within minutes of onset) by detecting restricted Brownian motion of intracellular water molecules?"
        ),
        "options": [
            ("Diffusion-Weighted Imaging (DWI) paired with Apparent Diffusion Coefficient (ADC) map", True, None),
            ("Fluid-Attenuated Inversion Recovery (FLAIR)", False, "FLAIR suppresses CSF signal but typically takes 3 to 6 hours to show hyperintensity in acute stroke."),
            ("Gradient Echo (GRE) / Susceptibility-Weighted Imaging (SWI)", False, "GRE and SWI are ultra-sensitive for blood breakdown products (hemosiderin, microbleeds), not early cytotoxic edema."),
            ("T1-weighted contrast-enhanced sequence", False, "T1 contrast enhancement occurs days to weeks later when the blood-brain barrier breaks down.")
        ],
        "pearl": "MRI Sequences in Acute Stroke: Diffusion-Weighted Imaging (DWI): Positive within 15-30 MINUTES of arterial occlusion! Cellular ATP failure -> Na+/K+ ATPase shutdown -> cytotoxic edema (water moves from extracellular to intracellular space) -> restricted water diffusion -> BRIGHT on DWI and DARK on ADC (Apparent Diffusion Coefficient) map. DWI-FLAIR Mismatch: Bright on DWI + Normal on FLAIR = Stroke onset within <4.5 hours (eligible for IV thrombolysis!).",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 49 (Stroke MRI), p. 1320-1335.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: MRI Sequences (T1, T2, FLAIR, DWI)",
        "stem": (
            "On brain MRI imaging, distinguishing between simple free fluid (Cerebrospinal Fluid) and periventricular pathological lesions "
            "is critical. Which sequence nullifies/suppresses the bright signal of free fluid (CSF) so that high-signal periventricular demyelinating plaques "
            "(Dawson's fingers in Multiple Sclerosis) stand out prominently?"
        ),
        "options": [
            ("Fluid-Attenuated Inversion Recovery (FLAIR)", True, None),
            ("Short Tau Inversion Recovery (STIR)", False, "STIR nullifies FAT signal, used in musculoskeletal and orbital imaging, not CSF suppression."),
            ("T1-weighted Spin Echo", False, "T1 CSF is dark, but white matter lesions are also hypointense, lacking high-contrast conspicuity."),
            ("Proton Density (PD) weighting", False, "Proton density has poor CSF contrast compared to FLAIR.")
        ],
        "pearl": "MRI Signal Characteristics: T1-weighted: Water/CSF is DARK (hypointense), Fat is BRIGHT (hyperintense). Good for anatomy. T2-weighted: Water/CSF is BRIGHT (hyperintense), Fat is intermediate. Good for pathology/edema. FLAIR (Fluid-Attenuated Inversion Recovery): T2-weighted sequence where FREE WATER (CSF) signal is SUPPRESSED (turned black), making periventricular edema and demyelinating plaques (MS) glow bright white!",
        "citation": "Sutton's Textbook of Radiology, 7th Ed, Chapter 40 (Principles of MRI), p. 1140-1152.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Aortic Dissection & Pulmonary Embolism CT",
        "stem": (
            "A 64-year-old male with long-standing poorly controlled hypertension presents to the emergency department with sudden-onset, "
            "excruciating, tearing retrosternal chest pain that radiates directly through to the interscapular region of his back. "
            "His blood pressure is 185/105 mmHg in the right arm and 130/80 mmHg in the left arm (pulse deficit). "
            "Contrast-Enhanced Computed Tomography Aortography (CT Aorta) is performed. What is the pathognomonic diagnostic imaging finding of Acute Aortic Dissection?"
        ),
        "options": [
            ("Intimal flap separating a true lumen from a false lumen", True, None),
            ("Abrupt 'apple-core' circumferential narrowing of the descending thoracic aorta", False, "Apple-core sign is characteristic of annular constricting colonic carcinoma or coarctation of aorta."),
            ("Calcified pleural plaques along the diaphragmatic dome", False, "Calcified pleural plaques are pathognomonic for asbestos exposure."),
            ("Dense opacification of the azygos arch", False, "Azygos arch opacification is normal venous drainage, not a sign of dissection.")
        ],
        "pearl": "Aortic Dissection Imaging: Contrast CT Aortography is the gold standard imaging modality. Pathognomonic sign: INTIMAL FLAP separating True Lumen (smaller, surrounded by calcification, continuous with aortic root) from False Lumen (larger, slower flow, contains 'cobweb sign' or thrombosis). Stanford Classification: Type A: Involves Ascending Aorta (EMERGENCY SURGERY); Type B: Distal to Left Subclavian Artery (Medical management with IV Beta-blockers: Labetalol/Esmolol to target SBP 100-120 mmHg).",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 22 (Vascular Imaging), p. 580-595.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Aortic Dissection & Pulmonary Embolism CT",
        "stem": (
            "A 45-year-old female who recently underwent major orthopedic hip surgery develops sudden-onset tachypnea, pleuritic chest pain, and hemoptysis. "
            "CT Pulmonary Angiography (CTPA) confirms an acute pulmonary embolism. What is the classic direct lumina finding on axial contrast-enhanced CTPA?"
        ),
        "options": [
            ("Partial or complete intraluminal filling defect surrounded by iodinated contrast (Polo Mint sign on cross-section / Railway Track sign on longitudinal view)", True, None),
            ("Aneurysmal dilatation of the bronchial arteries >10 mm", False, "Bronchial artery hypertrophy is seen in chronic hemoptysis / bronchiectasis."),
            ("Diffuse bilateral calcification of the pulmonary valve leaflets", False, "Pulmonary valve calcification is not related to acute thromboembolism."),
            ("Continuous contrast extravasation into the pericardial sac", False, "Pericardial contrast extravasation indicates cardiac rupture or perforation.")
        ],
        "pearl": "CT Pulmonary Angiography (CTPA) in PE: Gold standard imaging test. Direct signs: Intraluminal filling defect within pulmonary arteries. On cross-section: 'Polo Mint sign' (contrast surrounding central thrombus). On longitudinal section: 'Railway Track sign'. Indirect pulmonary signs: Westermark sign (regional oligemia), Hampton hump (wedge-shaped pleural infarction), Fleischner sign (enlarged pulmonary artery).",
        "citation": "Sutton's Textbook of Radiology, 7th Ed, Chapter 7 (Pulmonary Thromboembolism), p. 195-204.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: High-Resolution CT (HRCT) Chest Patterns",
        "stem": (
            "A 66-year-old male presents with progressive dry cough and exertional breathlessness for 1 year. On auscultation, there are prominent dry, "
            "end-inspiratory 'velcro-like' crackles at both lung bases, and digital clubbing is present. "
            "High-Resolution Computed Tomography (HRCT) of the chest reveals a subpleural and basilar-predominant reticular abnormality, with traction bronchiectasis "
            "and multi-layered subpleural cystic airspaces with thick fibrous walls resembling a 'honeycomb'. There are no ground-glass opacities or air-trapping. "
            "What is this classic HRCT pattern indicative of Idiopathic Pulmonary Fibrosis (IPF)?"
        ),
        "options": [
            ("Usual Interstitial Pneumonia (UIP) pattern", True, None),
            ("Non-Specific Interstitial Pneumonia (NSIP) pattern", False, "NSIP characteristically exhibits diffuse bilateral ground-glass opacities with subpleural sparing, lacking extensive honeycombing."),
            ("Crazy Paving pattern", False, "Crazy paving (ground-glass with thickened interlobular septa) is typical of Pulmonary Alveolar Proteinosis (PAP) and COVID-19 pneumonia."),
            ("Tree-in-Bud pattern", False, "Tree-in-bud pattern indicates active endobronchial infectious bronchiolitis (e.g., active Mycobacterium tuberculosis or bacterial infection).")
        ],
        "pearl": "HRCT Chest Patterns: 1. Usual Interstitial Pneumonia (UIP): Basal and subpleural predominance, Reticular thickening, Traction bronchiectasis, and HONEYCOMBING. Definitive diagnosis of IPF (no biopsy required if HRCT criteria met). 2. Crazy Paving: Ground glass + superimposed interlobular septal thickening (Pulmonary Alveolar Proteinosis, Lipoid pneumonia). 3. Tree-in-Bud: Centrilobular branching nodular opacities reflecting impacted terminal bronchioles (Active pulmonary TB).",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 9 (Diffuse Lung Diseases), p. 240-258.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: High-Resolution CT (HRCT) Chest Patterns",
        "stem": (
            "A 28-year-old female presents with recurrent spontaneous bilateral pneumothoraces and exertional dyspnea. "
            "Physical examination reveals multiple periungual fibromas (Koenen tumors) and facial angiofibromas. "
            "HRCT chest reveals diffuse, thin-walled, round, uniform cystic spaces throughout both lungs surrounded by normal intervening lung parenchyma. "
            "What is this cystic pulmonary disease strongly associated with Tuberous Sclerosis Complex?"
        ),
        "options": [
            ("Lymphangioleiomyomatosis (LAM)", True, None),
            ("Langerhans Cell Histiocytosis (LCH)", False, "Pulmonary LCH occurs in young smokers, spares lung bases, and features bizarre/irregular bizarre-shaped cysts derived from cavitating nodules."),
            ("Pneumocystis jirovecii Pneumonia (PJP)", False, "PJP features bilateral diffuse ground-glass haziness with upper-lobe pneumatoceles in immunocompromised HIV patients."),
            ("Centrilobular Emphysema", False, "Centrilobular emphysema lacks a perceptible wall and has a central dot representing the central bronchovascular bundle in smokers.")
        ],
        "pearl": "Cystic Lung Diseases on HRCT: 1. Lymphangioleiomyomatosis (LAM): Seen in women of childbearing age + Tuberous Sclerosis (TSC1/TSC2 mutation). Uniform, round, thin-walled cysts evenly distributed throughout all lung zones (including bases). 2. Pulmonary Langerhans Cell Histiocytosis (PLCH): Smokers, mid-upper zone predominance, costophrenic angles SPARED, nodules cavitate into bizarre bilobed/clover-leaf cysts.",
        "citation": "Sutton's Textbook of Radiology, 7th Ed, Chapter 8 (HRCT Lung), p. 230-242.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Abdominal Ultrasound & Biliary Imaging",
        "stem": (
            "A 44-year-old obese female presents with severe, colicky right upper quadrant abdominal pain radiating to her right infrascapular area, "
            "accompanied by low-grade fever and nausea after eating a rich, fatty meal. "
            "On abdominal ultrasound, the gallbladder is distended with a thickened anterior wall measuring 5.2 mm (normal <3 mm), "
            "pericholecystic fluid, and an impacted calculus in the gallbladder neck. "
            "When the ultrasound probe is pressed directly over the visualized gallbladder, the patient experiences sharp, agonizing tenderness "
            "with sudden arrest of deep inspiration. What is this pathognomonic ultrasound sign?"
        ),
        "options": [
            ("Sonographic Murphy's Sign", True, None),
            ("Target Sign (Doughnut Sign)", False, "Target/Doughnut sign is characteristic of Intussusception on bowel ultrasound."),
            ("Double Duct Sign", False, "Double duct sign is simultaneous dilatation of common bile duct and pancreatic duct seen on MRCP/CT in pancreatic head carcinoma."),
            ("Double Bubble Sign", False, "Double bubble sign is seen on fetal/neonatal abdominal radiograph in Duodenal Atresia.")
        ],
        "pearl": "Acute Cholecystitis Ultrasound Triad: 1. Gallstones (hyperechoic focus with posterior acoustic shadowing, often impacted in neck/Hartmann pouch) | 2. Gallbladder wall thickening (>3 mm, layered/edematous) | 3. SONOGRAPHIC MURPHY'S SIGN (maximal point tenderness elicited by direct transducer compression over the sonographically identified gallbladder; 95% specificity!). Pericholecystic fluid is a secondary sign.",
        "citation": "Grainger & Allison's Diagnostic Radiology, 7th Ed, Chapter 32 (Gallbladder & Biliary Tree), p. 860-875.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Abdominal Ultrasound & Biliary Imaging",
        "stem": (
            "A 60-year-old male presents with deep, progressive, painless jaundice, generalized pruritus, pale clay-colored stools, and dark tea-colored urine. "
            "Magnetic Resonance Cholangiopancreatography (MRCP) reveals severe, smooth, dilated intrahepatic bile ducts converging at the hepatic hilum, "
            "with an abrupt cutoff at the confluence of the right and left hepatic ducts. The gallbladder is collapsed and the common bile duct (CBD) is normal in caliber. "
            "What is the most likely diagnosis and eponymous name for this tumor?"
        ),
        "options": [
            ("Klatskin Tumor (Hilar Cholangiocarcinoma at the junction of right and left hepatic ducts)", True, None),
            ("Periampullary adenocarcinoma", False, "Periampullary tumors obstruct the distal common bile duct, causing massive dilatation of the gallbladder (Courvoisier law positive) and entire CBD."),
            ("Choledochal cyst Type I", False, "Choledochal cyst Type I presents as fusiform dilatation of the extrahepatic common bile duct in children/young adults."),
            ("Sclerosing cholangitis with bead-like multifocal strictures", False, "Primary sclerosing cholangitis features multifocal 'beads-on-a-string' strictures throughout both intrahepatic and extrahepatic ducts.")
        ],
        "pearl": "Klatskin Tumor (Hilar Cholangiocarcinoma): Arises at the bifurcation/confluence of the right and left hepatic ducts. Classified by Bismuth-Corlette system (Type I to IV). Imaging findings on MRCP/CT: Severe intrahepatic biliary radicle dilatation (IHBRD) with normal/collapsed gallbladder and collapsed distal common bile duct. Courvoisier's Law: Palpably enlarged gallbladder in painless jaundice is UNLIKELY to be gallstones (indicates periampullary/pancreatic head cancer); Klatskin tumor has a collapsed, non-palpable gallbladder!",
        "citation": "Sutton's Textbook of Radiology, 7th Ed, Chapter 30 (Hepatobiliary Imaging), p. 840-854.",
        "difficulty": "moderate"
    }
]
