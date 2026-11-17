"""
Authentic High-Yield NEET-PG Clinical Questions for Physiology
References: Guyton and Hall Textbook of Medical Physiology (14th Ed), Ganong's Review of Medical Physiology (26th Ed)
"""

PHYSIOLOGY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Resting Membrane Potential & Action Potential",
        "stem": (
            "During the rapid depolarizing upstroke (Phase 0) of an action potential in a mammalian peripheral nerve axon, "
            "the membrane potential shifts from -70 mV to +35 mV within 1 millisecond. "
            "Which of the following ion channel biophysical events is primarily responsible for this rapid voltage reversal?"
        ),
        "options": [
            ("Massive, regenerative influx of Sodium ions (Na+) through rapidly opening Voltage-Gated Sodium Channels (m-gates opening)", True, None),
            ("Efflux of Potassium ions (K+) through delayed rectifier potassium channels", False, "Potassium efflux mediates REPOLARIZATION, restoring the negative membrane potential."),
            ("Influx of Calcium ions (Ca2+) through L-type channels", False, "Calcium influx through L-type channels is responsible for the plateau phase (Phase 2) of cardiac ventricular action potentials, not nerve action potentials."),
            ("Efflux of Chloride ions (Cl-) through GABA-A channels", False, "Chloride influx causes hyperpolarization and inhibitory post-synaptic potentials (IPSPs).")
        ],
        "pearl": "Nerve Action Potential Phases: 1. Resting Membrane Potential (-70 to -90 mV): Determined primarily by high resting K+ permeability through K+ leak channels (Nernst potential of K+ = -90 mV) maintained by Na+/K+ ATPase pump. 2. Depolarization (Phase 0): Stimulus reaches threshold (-55 mV) -> activation gates (m-gates) of Voltage-Gated Na+ Channels open rapidly -> regenerative Na+ INFLUX towards Na+ equilibrium potential (+60 mV). 3. Repolarization: Inactivation gates (h-gates) of Na+ channels close (absolute refractory period) while Delayed Rectifier K+ channels open -> K+ EFFLUX restores negativity. Tetrodotoxin (TTX) and Saxitoxin block voltage-gated Na+ channels.",
        "citation": "Guyton and Hall Textbook of Medical Physiology, 14th Ed, Chapter 5 (Membrane Potentials), p. 61-74.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Resting Membrane Potential & Action Potential",
        "stem": (
            "In cardiac ventricular muscle myocytes, Phase 2 of the action potential is characterized by a prolonged plateau phase "
            "lasting approximately 200 to 300 milliseconds. What balanced inward and outward ionic currents maintain this electrical plateau, "
            "preventing premature tetanic contraction and ensuring adequate mechanical ventricular ejection?"
        ),
        "options": [
            ("Inward flux of Calcium (Ca2+) through L-type (DHP) channels balanced by outward flux of Potassium (K+) through delayed rectifier channels", True, None),
            ("Inward flux of Sodium (Na+) balanced by outward flux of Chloride (Cl-)", False, "Sodium channels are rapidly inactivated at the end of Phase 0 by h-gates."),
            ("Inward flux of Potassium balanced by outward flux of Calcium", False, "Potassium flux is outward; calcium flux is inward."),
            ("Direct electrogenic activation of the sodium-calcium exchanger (NCX) in reverse mode alone", False, "NCX contributes to calcium extrusion, but L-type calcium channels and delayed rectifier K+ channels govern Phase 2.")
        ],
        "pearl": "Cardiac Ventricular Action Potential Phases: Phase 0: Rapid depolarization (fast Na+ influx via Nav1.5). Phase 1: Early partial repolarization (transient outward K+ current, Ito). Phase 2 (PLATEAU): Prolonged refractory plateau maintained by INWARD L-TYPE Ca2+ CURRENT (ICa-L) BALANCED BY OUTWARD DELAYED RECTIFIER K+ CURRENT (IKr/IKs). Phase 3: Rapid repolarization (Ca2+ channels close, strong outward K+ efflux). Phase 4: Resting membrane potential (-90 mV, inward rectifier K1 channels). Sinoatrial Node (Pacemaker): Phase 4 automaticity driven by FUNNY CHANNELS (If: hyperpolarization-activated cyclic nucleotide-gated HCN channels carrying Na+/K+ current).",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 28 (Electrical Activity of the Heart), p. 505-516.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Oxygen-Hemoglobin Dissociation Curve",
        "stem": (
            "During vigorous aerobic exercise in skeletal muscle, local tissue physiological conditions change dramatically: "
            "temperature increases, local tissue pCO2 rises, lactic acid lowers pH, and erythrocyte 2,3-Bisphosphoglycerate (2,3-BPG) synthesis increases. "
            "How do these physiological changes shift the Oxygen-Hemoglobin Dissociation Curve, and what is the functional effect on oxygen delivery?"
        ),
        "options": [
            ("Shifts the curve to the RIGHT (Bohr Effect), DECREASING hemoglobin affinity for oxygen and promoting O2 unloading to working tissues", True, None),
            ("Shifts the curve to the LEFT, increasing hemoglobin affinity for oxygen and preventing O2 unloading", False, "Left shift increases O2 affinity, holding onto oxygen tightly, which impairs tissue delivery."),
            ("Shifts the curve upward without changing affinity", False, "Shifting upward is an increase in total oxygen capacity (e.g. polycythemia), not a change in p50."),
            ("Completely abolishes the sigmoidal shape into a hyperbolic curve", False, "Hyperbolic curve is characteristic of single-subunit Myoglobin, not tetrameric cooperative Hemoglobin.")
        ],
        "pearl": "Oxygen-Hemoglobin Dissociation Curve Shifts (CADET Mnemonic): SHIFT TO THE RIGHT (Releases O2 to tissues; Increased p50, Lower affinity): C: CO2 increased | A: Acidity / H+ increased (low pH, Bohr effect) | D: 2,3-DPG (2,3-BPG) increased | E: Exercise | T: Temperature increased. (Think: Working muscle needs Oxygen!). SHIFT TO THE LEFT (Holds O2 tightly; Decreased p50, Higher affinity): Low CO2, Alkalosis (high pH), Low 2,3-DPG, Low Temp, Fetal Hemoglobin (HbF binds 2,3-BPG poorly), Carboxyhemoglobin (CO poisoning), Methemoglobin.",
        "citation": "Guyton and Hall Textbook of Medical Physiology, 14th Ed, Chapter 41 (Physical Principles of Gaseous Exchange), p. 515-528.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Oxygen-Hemoglobin Dissociation Curve",
        "stem": (
            "Fetal Hemoglobin (HbF: alpha-2 gamma-2) has a significantly higher affinity for oxygen than Adult Hemoglobin (HbA: alpha-2 beta-2), "
            "causing its oxygen dissociation curve to lie to the LEFT of the adult curve. "
            "What is the precise biochemical mechanism underlying HbF's higher oxygen affinity that enables maternal-to-fetal oxygen transfer across the placenta?"
        ),
        "options": [
            ("The gamma globin chain contains a neutral Serine residue instead of a positively charged Histidine (His143) present in the adult beta chain, dramatically reducing its binding affinity for 2,3-BPG", True, None),
            ("HbF contains four heme pockets instead of two", False, "Both HbA and HbF are tetramers with exactly four heme moieties."),
            ("HbF is completely immune to carbon monoxide binding", False, "HbF binds carbon monoxide with high affinity similar to HbA."),
            ("HbF contains an intrinsic carbonic anhydrase catalytic site", False, "Carbonic anhydrase is an erythrocyte enzyme, not part of globin peptide structure.")
        ],
        "pearl": "Fetal Hemoglobin (HbF) Biochemical Basis: Adult HbA has beta chains with Histidine-143 facing the central cavity, forming salt bridges with negatively charged 2,3-BPG (stabilizing the deoxygenated T-state). In Fetal HbF, the gamma chain has SERINE instead of Histidine-143 -> loses positive charge -> CANNOT BIND 2,3-BPG effectively -> favors relaxed R-state -> HIGHER OXYGEN AFFINITY (Left-shifted curve, p50 = 19 mmHg vs 27 mmHg in adult). Ensures fetus extracts O2 from maternal blood in placenta!",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 35 (Gas Transport), p. 625-634.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Cardiac Cycle & Pressure-Volume Loops",
        "stem": (
            "On a Left Ventricular Pressure-Volume (P-V) loop, what phase of the cardiac cycle begins immediately when the Mitral Valve closes "
            "and ends when the Aortic Valve opens, during which ventricular pressure rises steeply from 10 mmHg to 80 mmHg "
            "with ABSOLUTELY NO CHANGE in ventricular volume?"
        ),
        "options": [
            ("Isovolumetric (Isovolumic) Contraction Phase", True, None),
            ("Rapid Ventricular Ejection Phase", False, "Rapid ejection begins AFTER the aortic valve opens, during which ventricular volume decreases sharply."),
            ("Isovolumetric Relaxation Phase", False, "Isovolumetric relaxation occurs after aortic valve closure and before mitral valve opening."),
            ("Reduced Ventricular Filling Phase", False, "Reduced filling (diastasis) is a late diastolic phase with open mitral valve.")
        ],
        "pearl": "Left Ventricular Pressure-Volume Loop Phases: 1. End-Diastolic Volume (Point A, ~120 mL): MITRAL VALVE CLOSES -> First Heart Sound (S1). 2. ISOVOLUMETRIC CONTRACTION (Line A-B): All 4 cardiac valves closed. Pressure rises rapidly (10 -> 80 mmHg), volume unchanged (120 mL). 3. Point B: AORTIC VALVE OPENS. 4. Rapid & Reduced Ejection (Line B-C): Volume falls to End-Systolic Volume (~50 mL). Stroke Volume = EDV - ESV = 70 mL. 5. Point C: AORTIC VALVE CLOSES -> Second Heart Sound (S2). 6. ISOVOLUMETRIC RELAXATION (Line C-D): Pressure drops (80 -> 10 mmHg), volume unchanged (50 mL). 7. Point D: MITRAL VALVE OPENS -> Rapid filling (S3 if abnormal).",
        "citation": "Guyton and Hall Textbook of Medical Physiology, 14th Ed, Chapter 9 (Heart Muscle), p. 112-124.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Cardiac Output & Frank-Starling Law",
        "stem": (
            "According to the Frank-Starling Law of the Heart, what is the intrinsic physiological mechanism by which an increase in End-Diastolic Volume "
            "(increased venous return / preload) directly produces an increase in Stroke Volume and myocardial contractility?"
        ),
        "options": [
            ("Stretching of cardiac ventricular myocytes optimizes sarcomere length (toward 2.2 um) and increases Troponin C affinity for Calcium ions, enhancing cross-bridge formation", True, None),
            ("Direct activation of beta-1 adrenergic receptors by intramyocardial stretch", False, "Frank-Starling law is an INTRINSIC property of myocardium independent of nerves or hormones; it functions in a denervated transplanted heart!"),
            ("Closure of Ryanodine receptors in the sarcoplasmic reticulum", False, "Ryanodine receptors release calcium to initiate contraction; closure would impair contraction."),
            ("Decrease in afterload during aortic valve opening", False, "Frank-Starling is a preload-dependent mechanism, not an afterload reduction.")
        ],
        "pearl": "Frank-Starling Law of the Heart: 'Within physiological limits, the force of ventricular contraction is directly proportional to the initial resting length of the muscle fibers (preload / End-Diastolic Volume).' Molecular mechanism: 1. Optimal overlapping of actin and myosin filaments (optimal sarcomere length = 2.0-2.2 um) | 2. Length-dependent increase in TROPONIN C AFFINITY FOR CALCIUM. INTRINSIC AUTOREGULATION: Occurs without sympathetic innervation (vital in transplanted hearts!). Balances cardiac output between right and left ventricles.",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 29 (The Heart as a Pump), p. 520-530.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Glomerular Filtration Rate Regulation",
        "stem": (
            "In renal physiology, which substance is considered the gold-standard exogenous filtration marker "
            "for measuring Glomerular Filtration Rate (GFR) because it is freely filtered at the glomerulus, "
            "completely neither reabsorbed, secreted, synthesized, nor metabolized by the renal tubules?"
        ),
        "options": [
            ("Inulin (fructose polysaccharide clearance = GFR)", True, None),
            ("Para-aminohippuric acid (PAH clearance = Renal Plasma Flow)", False, "PAH is freely filtered AND actively secreted by proximal tubules, used to measure Renal Plasma Flow (RPF), not GFR."),
            ("Creatinine", False, "Creatinine is endogenous and practical, but mildly secreted (~10-15%) by proximal tubules, slightly overestimating true GFR."),
            ("Urea", False, "Urea is reabsorbed (~50%) along the nephron, underestimating GFR.")
        ],
        "pearl": "Renal Clearance Principles: Clearance Formula: C = (U_x * V) / P_x. 1. INULIN CLEARANCE = GFR (~125 mL/min in males): Freely filtered, NO tubular reabsorption, NO secretion. Gold standard! 2. PARA-AMINOHIPPURIC ACID (PAH) CLEARANCE = EFFECTIVE RENAL PLASMA FLOW (eRPF ~600 mL/min): Filtered + actively SECRETED (almost 100% extracted in single pass). Renal Blood Flow (RBF) = RPF / (1 - Hematocrit) (~1200 mL/min, 20-25% of cardiac output). 3. FILTRATION FRACTION (FF) = GFR / RPF = 125 / 600 = ~0.20 (20%). 4. If Clearance of Substance X > Inulin -> Net tubular SECRETION. If Clearance < Inulin -> Net tubular REABSORPTION.",
        "citation": "Guyton and Hall Textbook of Medical Physiology, 14th Ed, Chapter 27 (Glomerular Filtration), p. 327-340.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Countercurrent Multiplier Mechanism",
        "stem": (
            "The renal medullary hyperosmolar gradient (increasing from 300 mOsm/L at the corticomedullary junction up to 1200 mOsm/L at the papilla) "
            "is essential for urine concentration. Which segment of the nephron acts as the active 'Countercurrent Multiplier' "
            "by actively reabsorbing Sodium, Potassium, and Chloride via the 1Na+-1K+-2Cl- (NKCC2) cotransporter while remaining completely IMPERMEABLE to water?"
        ),
        "options": [
            ("Thick Ascending Limb of the Loop of Henle", True, None),
            ("Thin Descending Limb of the Loop of Henle", False, "Thin descending limb is highly permeable to WATER (via AQP1) but impermeable to solutes."),
            ("Proximal Convoluted Tubule", False, "PCT reabsorbs isosmotically (300 mOsm/L) and does not generate the medullary hypertonic gradient."),
            ("Cortical Collecting Duct", False, "Cortical collecting duct reabsorbs water under ADH control, acting as an equilibrator rather than the multiplier.")
        ],
        "pearl": "Countercurrent System in Kidney: 1. COUNTERCURRENT MULTIPLIER = LOOP OF HENLE. Descending Thin Limb: Permeable to WATER (AQP1), impermeable to solutes -> tubular fluid becomes hypertonic (1200 mOsm/L). Thick Ascending Limb: Active NKCC2 cotransporter reabsorbs Na+, K+, 2Cl- into medullary interstitium; IMPERMEABLE TO WATER -> tubular fluid becomes hypotonic (100 mOsm/L, 'diluting segment') while interstitium becomes hyperosmolar. Inhibited by Loop Diuretics (Furosemide). 2. COUNTERCURRENT EXCHANGER = VASA RECTA (passive, hairpin loop architecture prevents washout of medullary solutes while supplying oxygen). UREA RECYCLING accounts for ~50% of inner medullary hyperosmolarity.",
        "citation": "Guyton and Hall Textbook of Medical Physiology, 14th Ed, Chapter 28 (Urine Concentration), p. 343-356.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Acid-Base Balance Regulation",
        "stem": (
            "A 24-year-old male with acute diabetic ketoacidosis has an arterial blood gas (ABG) showing: "
            "pH 7.18, Serum Bicarbonate (HCO3-) 12 mEq/L (normal 22-26 mEq/L). "
            "According to Winter's Formula for respiratory compensation in primary Metabolic Acidosis, "
            "what is the expected compensatory arterial partial pressure of carbon dioxide (pCO2)?"
        ),
        "options": [
            ("Expected pCO2 = 26 mmHg (range: 24 to 28 mmHg)", True, None),
            ("Expected pCO2 = 40 mmHg (normal range)", False, "40 mmHg would indicate concomitant respiratory acidosis / respiratory arrest because expected pCO2 should be lower to compensate for metabolic acidosis."),
            ("Expected pCO2 = 18 mmHg", False, "18 mmHg would indicate concomitant primary respiratory alkalosis."),
            ("Expected pCO2 = 50 mmHg", False, "50 mmHg reflects severe hypercapnic hypoventilation.")
        ],
        "pearl": "Winter's Formula for Metabolic Acidosis Compensation: Expected pCO2 = (1.5 x [HCO3-]) + 8 (+/- 2). Calculation: (1.5 x 12) + 8 = 18 + 8 = 26 mmHg (+/- 2, range 24-28 mmHg). Interpretation Rules: If Measured pCO2 = Expected pCO2 -> Simple compensated Metabolic Acidosis. If Measured pCO2 > Expected pCO2 -> Concomitant RESPIRATORY ACIDOSIS (e.g. respiratory fatigue/hypoventilation). If Measured pCO2 < Expected pCO2 -> Concomitant RESPIRATORY ALKALOSIS (e.g. salicylate toxicity).",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 38 (Acid-Base Homeostasis), p. 675-688.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Acid-Base Balance Regulation",
        "stem": (
            "In evaluating a patient with severe metabolic acidosis, the Serum Anion Gap is calculated using the formula: "
            "Anion Gap = [Na+] - ([Cl-] + [HCO3-]). Normal range is 8 to 12 mEq/L. "
            "Which of the following clinical conditions characteristically causes a NORMAL ANION GAP (Hyperchloremic) Metabolic Acidosis?"
        ),
        "options": [
            ("Severe Diarrhea or Renal Tubular Acidosis (RTA)", True, None),
            ("Diabetic Ketoacidosis (DKA)", False, "DKA causes High Anion Gap Metabolic Acidosis (HAGMA) due to unmeasured ketoacids (beta-hydroxybutyrate, acetoacetate)."),
            ("Lactic Acidosis due to septic shock", False, "Lactic acidosis causes HAGMA due to unmeasured lactate anions."),
            ("Salicylate (Aspirin) intoxication", False, "Salicylate poisoning causes mixed HAGMA and respiratory alkalosis.")
        ],
        "pearl": "Anion Gap Metabolic Acidosis Causes: 1. HIGH ANION GAP METABOLIC ACIDOSIS (HAGMA, >12 mEq/L; MUDPILES Mnemonic): M: Methanol | U: Uremia | D: DKA | P: Paraldehyde / Propylene glycol | I: INH / Iron | L: Lactic Acidosis | E: Ethylene Glycol | S: Salicylates. 2. NORMAL ANION GAP / HYPERCHLOREMIC (NAGMA, 8-12 mEq/L; HARDASS Mnemonic): H: Hyperalimentation (TPN) | A: Acetazolamide | R: RENAL TUBULAR ACIDOSIS (RTA Types 1, 2, 4) | D: DIARRHEA (massive loss of HCO3- with compensatory Cl- retention) | A: Addison's disease | S: Spironolactone | S: Saline infusion (massive normal saline).",
        "citation": "Guyton and Hall Textbook of Medical Physiology, 14th Ed, Chapter 31 (Acid-Base Regulation), p. 395-410.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Lung Volumes & Compliance",
        "stem": (
            "During routine pulmonary function testing (Spirometry), a patient breathes quietly and then performs maximal inspiratory "
            "and expiratory maneuvers. Which of the following lung volumes or capacities CANNOT BE MEASURED by simple Spirometry "
            "and requires Helium Dilution, Nitrogen Washout, or Body Plethysmography?"
        ),
        "options": [
            ("Residual Volume (RV), Functional Residual Capacity (FRC), and Total Lung Capacity (TLC)", True, None),
            ("Vital Capacity (VC) and Tidal Volume (TV)", False, "Both Vital Capacity and Tidal Volume are directly measured by simple spirometry."),
            ("Inspiratory Reserve Volume (IRV) and Inspiratory Capacity (IC)", False, "Both IRV and IC are easily measured by spirometry."),
            ("Expiratory Reserve Volume (ERV)", False, "ERV is measured directly as the maximal air expired below normal resting end-expiratory baseline.")
        ],
        "pearl": "Spirometry Limitations Golden Rule: Simple spirometry CANNOT measure any lung volume that contains the RESIDUAL VOLUME (RV, the volume of air remaining in lungs after maximal forced expiration, ~1200 mL). Therefore, the 3 parameters that CANNOT be measured by spirometry are: 1. RESIDUAL VOLUME (RV) | 2. FUNCTIONAL RESIDUAL CAPACITY (FRC = ERV + RV, volume at end of normal tidal expiration, ~2200 mL) | 3. TOTAL LUNG CAPACITY (TLC = VC + RV, ~6000 mL). Measured via: Body Plethysmography, Helium Dilution, or Nitrogen Washout.",
        "citation": "Ganong's Review of Medical Physiology, 26th Ed, Chapter 34 (Pulmonary Function), p. 605-616.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Lung Volumes & Compliance",
        "stem": (
            "At the end of a normal quiet tidal expiration (at Functional Residual Capacity, FRC), "
            "what are the opposing mechanical elastic forces acting on the respiratory system that reach an exact mechanical equilibrium?"
        ),
        "options": [
            ("The inward elastic recoil of the lungs is exactly equal and opposite to the outward spring-like elastic recoil of the thoracic chest wall", True, None),
            ("Atmospheric pressure is greater than alveolar pressure by 10 mmHg", False, "At FRC, alveolar pressure is 0 cm H2O (exactly equal to atmospheric pressure)."),
            ("Intrapleural pressure becomes positive (+5 cm H2O)", False, "At FRC, intrapleural pressure is NEGATIVE (-5 cm H2O) due to the opposing recoils pulling apart."),
            ("Diaphragmatic active tone reaches maximal downward contraction", False, "The diaphragm is completely relaxed at FRC.")
        ],
        "pearl": "Functional Residual Capacity (FRC) Equilibrium: FRC (~2200 mL) is the resting equilibrium volume of the respiratory system. Two opposing elastic recoil forces balance each other: 1. INWARD ELASTIC RECOIL of the lungs (wants to collapse inward due to surface tension and elastin) | 2. OUTWARD ELASTIC RECOIL of the chest wall (springs outward like a compressed cage). At FRC: Net balance -> Alveolar pressure = 0 (atmospheric) -> Airflow is zero. INTRAPLEURAL PRESSURE is NEGATIVE (-5 cm H2O) because the two opposing walls pull in opposite directions! In Pneumothorax: Chest wall springs outward; lung collapses inward.",
        "citation": "Guyton and Hall Textbook of Medical Physiology, 14th Ed, Chapter 38 (Pulmonary Ventilation), p. 482-492.",
        "difficulty": "moderate"
    }
]
