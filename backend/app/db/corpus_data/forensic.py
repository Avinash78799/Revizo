"""
Authentic High-Yield NEET-PG Clinical Questions for Forensic Medicine & Toxicology
References: Reddy's The Essentials of Forensic Medicine and Toxicology (34th Ed), Parikh's Textbook of Medical Jurisprudence (8th Ed)
"""

FORENSIC_QUESTIONS = [
    {
        "concept_name": "Core Principles: Rigor Mortis & Algor Mortis",
        "stem": (
            "During a medicolegal postmortem examination of an adult male found deceased inside an air-conditioned apartment, "
            "the forensic pathologist observes that rigor mortis is fully established in the involuntary muscles of the heart, "
            "the muscles of the eyelids, jaw, face, neck, and upper extremities, but the lower limbs and small muscles of the feet "
            "remain completely flaccid. According to Nysten's Rule of rigor mortis progression, "
            "what is the sequence of appearance of postmortem rigidity in the human body?"
        ),
        "options": [
            ("Heart and involuntary muscles first, followed by eyelids, lower jaw, neck, thorax, upper extremities, abdomen, lower extremities, and finally fingers/toes", True, None),
            ("Lower extremities first, progressing upward to the thorax and facial muscles", False, "Rigor mortis does not start in the lower extremities; it follows Nysten's craniocaudal progression."),
            ("Simultaneous instantaneous appearance throughout all skeletal muscle groups at the moment of death", False, "Instantaneous rigidity at the moment of death without flaccidity is Cadaveric Spasm, not normal rigor mortis."),
            ("Distal extremities first, progressing centripetally to the core trunk", False, "Rigor mortis follows a descending craniocaudal anatomical order, not centripetal.")
        ],
        "pearl": "Rigor Mortis Progression & Timeline: Mechanism: Cessation of respiration -> ATP depletion -> myosin heads cannot detach from actin filaments -> sustained actin-myosin complex rigor. NYSTEN'S RULE (Craniocaudal progression): Heart (1 hr) -> Eyelids (2-3 hrs) -> Jaw & Face -> Neck & Trunk -> Upper Extremities -> Lower Extremities (12 hrs). RULE OF 12s (Temperate/Tropical climate): Starts in 1-2 hours | Fully established in all muscles by 12 hours | Persists for 12 hours (12-24 hrs) | Disappears in the SAME craniocaudal order over the next 12 hours (24-36 hrs) as autolysis and putrefaction begin.",
        "citation": "Reddy's The Essentials of Forensic Medicine and Toxicology, 34th Ed, Chapter 7 (Thanatology), p. 142-156.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Rigor Mortis & Algor Mortis",
        "stem": (
            "A soldier is found dead on a battlefield immediately following a grenade explosion. "
            "His right hand remains locked in an intensely rigid grip clutching the handle of his service rifle. "
            "There was no period of primary postmortem flaccidity preceding this rigidity. "
            "What is this condition, and what is its primary medicolegal significance?"
        ),
        "options": [
            ("Cadaveric Spasm (Instantaneous Rigor); Proves that the weapon was held in the victim's hand at the exact moment of death, ruling out postmortem placement of the weapon", True, None),
            ("Normal rigor mortis; Indicates that death occurred at least 12 hours prior to discovery", False, "Normal rigor mortis is always preceded by a stage of primary muscle flaccidity."),
            ("Heat stiffening (Pugilistic attitude)", False, "Heat stiffening is caused by thermal coagulation of muscle proteins in burns, producing a 'pugilistic' boxer-like posture."),
            ("Freezing rigidity", False, "Cold stiffening is due to freezing of intracellular water into ice crystals at sub-zero temperatures.")
        ],
        "pearl": "Cadaveric Spasm (Cataleptic Rigidity): Extremely rare form of instantaneous rigidity occurring AT THE EXACT MOMENT OF DEATH without any preceding stage of primary flaccidity. Involves a single muscle group (typically the hand/fingers). Occurs in states of severe emotional stress, physical exhaustion, or sudden violent death (battlefield, drowning victim grasping grass/sand, suicide clutching revolver). MEDICOLEGAL IMPORTANCE: Incontrovertible proof of suicide or activity at the moment of death; CANNOT BE SIMULATED OR PRODUCED AFTER DEATH!",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 7, p. 150-154.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Postmortem Hypostasis & Decomposition",
        "stem": (
            "In an autopsy of a suspected homicide victim discovered inside a closed garage with a running car engine, "
            "the forensic pathologist observes bright, vivid CHERRY-PINK postmortem hypostasis (livor mortis) "
            "distributed over the dependent, uncompressed areas of the back and buttocks. "
            "What is the underlying cause of death responsible for this distinctive livor coloration?"
        ),
        "options": [
            ("Carbon Monoxide (CO) poisoning causing formation of Carboxyhemoglobin", True, None),
            ("Cyanide poisoning causing high levels of oxyhemoglobin in venous blood (brick-red)", False, "Cyanide poisoning produces bright BRICK-RED / CHERRY-RED hypostasis due to inhibition of cytochrome oxidase preventing cellular oxygen utilization."),
            ("Methemoglobinemia from aniline dye poisoning (chocolate-brown)", False, "Methemoglobinemia causes dark chocolate-brown or dusky slate-grey hypostasis."),
            ("Phosphorus poisoning (dark brown)", False, "Phosphorus causes dark brown hypostasis and jaundice.")
        ],
        "pearl": "Color of Postmortem Hypostasis (Livor Mortis): Normal / Asphyxia: Bluish-purple / Violet (due to reduced deoxygenated hemoglobin). 1. Carbon Monoxide (CO): CHERRY-PINK (Carboxyhemoglobin). 2. Cyanide: BRICK-RED / Cherry-red (Oxyhemoglobin excess; histotoxic hypoxia). 3. Nitrites / Aniline / Dapsone: CHOCOLATE-BROWN (Methemoglobinemia). 4. Potassium Chlorate: Dark chocolate-brown. 5. Refrigeration / Hypothermia: BRIGHT PINK / Light red. 6. Hydrogen Sulfide: Greenish-brown (Sulfhemoglobin).",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 7, p. 136-142.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Postmortem Hypostasis & Decomposition",
        "stem": (
            "During summer in North India (ambient temperature 38°C), a dead body undergoes putrefaction. "
            "What is the EARLIEST external sign of decomposition visible on the cutaneous surface of the human body, "
            "and in which anatomical region does it characteristically appear?"
        ),
        "options": [
            ("Greenish discoloration of the skin over the Right Iliac Fossa (due to hydrogen sulfide reacting with hemoglobin to form Sulfhemoglobin in the superficial cecum)", True, None),
            ("Postmortem marbling of superficial veins on the shoulders", False, "Marbling appears later (around 24-36 hours) as bacterial intravascular hemolysis outlines cutaneous veins."),
            ("Skin slippage and bullae formation on the extremities", False, "Skin slippage and bullae appear at 36-48 hours."),
            ("Colliquative liquefaction of the brain", False, "Internal organ liquefaction occurs late in decomposition.")
        ],
        "pearl": "Earliest Sign of Putrefaction: GREENISH DISCOLORATION OF THE RIGHT ILIAC FOSSA (RIF). Appears in 12-18 hours in summer (24-36 hrs in winter). Mechanism: Intestinal bacteria (Clostridium welchii / perfringens) generate Hydrogen Sulfide (H2S) in the feces-rich cecum -> H2S diffuses through the abdominal wall and reacts with hemoglobin in blood vessels to form SULFMETHEMOGLOBIN / SULFMOGLOBIN (green pigment). Casper's Dictum of Putrefaction: 1 week in air = 2 weeks in water = 8 weeks underground in soil (Ratio 1 : 2 : 8).",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 7, p. 156-168.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Firearm Entry vs Exit Wounds",
        "stem": (
            "In a medicolegal autopsy of a firearm fatality victim, examination of an entrance wound on the anterior chest wall "
            "demonstrates a central circular skin defect with inverted margins, an abrasion collar, a grease collar (dirt ring), "
            "and extensive burning, scorching, and singing of hair, along with dense, unburned powder grains embedded into the dermis "
            "that cannot be wiped off (TATTOOING / Stippling) over a radius of 15 cm around the wound. "
            "What range of firing is represented by this entrance wound?"
        ),
        "options": [
            ("Close range firing (within 30 cm / 1 to 2 feet with a handgun)", True, None),
            ("Contact firing (muzzle pressed firmly against the skin)", False, "Contact firing features a muzzle imprint abrasion ring and soot/powder driven entirely INSIDE the wound track, with no external tattooing ring."),
            ("Distant range firing (beyond 1 meter / 3 feet)", False, "Distant range wounds exhibit ONLY the central defect with abrasion and grease collars, with ZERO burning, soot, or tattooing."),
            ("Ricochet pellet injury", False, "Ricochet injuries produce irregular, lacerated entry wounds without concentric tattooing.")
        ],
        "pearl": "Firearm Range Characteristics: 1. Contact Range: Muzzle imprint (abraded ring of muzzle stamp), stellate laceration over flat bone (skull due to expanding subgaleal gases), soot and powder inside wound track. 2. Close Range (within 30-60 cm / 1-2 feet): Burning/Singing of hair + Blackening (soot, can be wiped off) + TATTOOING / STIPPLING (unburned powder grains driven into dermis, CANNOT BE WIPED OFF). 3. Intermediate Range: Blackening disappears first; Tattooing persists up to 60-90 cm. 4. Distant Range (>1 meter): ONLY mechanical bullet defect: Inverted margins + Abrasion Collar + Grease Collar (Dirt Ring). NO soot, NO tattooing! Exit Wound: Everted margins, larger, irregular, NO abrasion collar, NO soot/tattooing.",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 11 (Firearm Injuries), p. 218-236.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Hanging vs Strangulation Differentials",
        "stem": (
            "A 28-year-old female is found dead in her bedroom with a ligature around her neck. "
            "At autopsy, the ligature mark is found to be completely HORIZONTAL, circular, continuous around the entire circumference "
            "of the neck, located BELOW the thyroid cartilage, and deeply grooved with an ecchymotic, congested base. "
            "Dissection of the neck reveals extensive extravasation of blood into the subcutaneous tissues and strap muscles of the neck, "
            "with a fracture of the thyroid cartilage and cricoid cartilage. What is the diagnosis, and what distinguishes this from typical suicidal hanging?"
        ),
        "options": [
            ("Ligature Strangulation (Homicidal); Ligature mark is horizontal, low-lying below thyroid cartilage, continuous, with extensive strap muscle hematomas", True, None),
            ("Typical Suicidal Hanging; Ligature mark is oblique, non-continuous with a suspension knot at the occiput", False, "In hanging, the mark is OBLIQUE, high up above thyroid cartilage, non-continuous at the knot, and neck muscle hemorrhage is minimal."),
            ("Manual Strangulation (Throttling) by bare hands", False, "Throttling features crescentic fingernail scratches and fingertip round contusions on the neck skin, not a continuous mechanical ligature groove."),
            ("Burdell's compression asphyxia", False, "Burdell's or traumatic asphyxia involves chest compression by external heavy weight.")
        ],
        "pearl": "Hanging vs Ligature Strangulation: 1. HANGING: Manner: Almost always SUICIDAL. Ligature Mark: OBLIQUE, non-continuous (interrupted at knot site), HIGH UP in the neck (ABOVE thyroid cartilage, between larynx and chin). Subcutaneous tissues under mark are white, dry, and glistening ('parchment-like') with minimal muscle hemorrhage. Fracture of hyoid: Greater cornu fractured in elderly (abduction fracture). 2. LIGATURE STRANGULATION: Manner: Almost always HOMICIDAL. Ligature Mark: HORIZONTAL, CONTINUOUS, completely encircles neck, LOW DOWN (BELOW thyroid cartilage). Strap muscles severely bruised/lacerated. Thyroid/cricoid cartilage fractures common.",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 13 (Mechanical Asphyxia), p. 272-294.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Heavy Metal Poisoning (Arsenic, Lead, Mercury)",
        "stem": (
            "A 42-year-old male from a rural delta region where groundwater tube wells contain high mineral levels presents with chronic abdominal cramps, "
            "burning paresthesias in a glove-and-stocking distribution, sensory ataxia, and progressive skin pigmentation. "
            "Physical examination reveals diffuse mottled, speckled 'rain-drop' hyperpigmentation over his trunk, punctate hyperkeratotic papules "
            "on the palms and soles (arsenical keratosis), and transverse white bands across all fingernails (Aldrich-Mees lines). "
            "What is the toxic heavy metal responsible, and what is its molecular mechanism of cellular toxicity?"
        ),
        "options": [
            ("Arsenic (Trivalent Arsenite); Inactivation of lipoic acid cofactor and binding to sulfhydryl (-SH) groups of pyruvate dehydrogenase, halting ATP synthesis", True, None),
            ("Lead (Plumbism); Inhibition of ferrochelatase and delta-ALA dehydratase causing basophilic stippling", False, "Lead causes basophilic stippling, Burtonian blue gingival line, and wrist drop (radial palsy), not rain-drop pigmentation or arsenic keratosis."),
            ("Mercury; Irreversible binding to tubulin producing erethism and acrodynia", False, "Mercury causes Minamata disease, erethism, and Pink disease (acrodynia) in children."),
            ("Thallium; Substitution of potassium in ATPase pumps causing total alopecia", False, "Thallium causes rapid, complete painless alopecia (loss of hair) and painful sensory neuropathy.")
        ],
        "pearl": "Heavy Metal Poisoning Classics: 1. ARSENIC: Odor of garlic, Aldrich-Mees white lines on nails, 'Rain-drop' skin pigmentation, Palmar/plantar hyperkeratosis, peripheral neuropathy. Mechanism: Binds -SH groups of lipoic acid, inhibiting Pyruvate Dehydrogenase and uncoupling oxidative phosphorylation. DOC: Dimercaprol (BAL) or DMSA (Succimer). 2. LEAD: Plumbism -> Basophilic stippling on blood smear, Burtonian blue line on gums, Lead lines on metaphysis of long bones, Wrist drop / Foot drop (motor neuropathy), microcytic anemia. DOC: Calcium Disodium EDTA, DMSA, or BAL. 3. THALLIUM: Painful sensory neuropathy + RAPID TOTAL ALOPECIA (spares inner 1/3 of eyebrow). Antidote: Prussian Blue.",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 24 (Metallic Poisons), p. 488-506.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Heavy Metal Poisoning (Arsenic, Lead, Mercury)",
        "stem": (
            "A 38-year-old battery factory worker presents with colicky abdominal pain (lead colic), severe fatigue, and bilateral wrist drop. "
            "Physical examination reveals a bluish-purple line along the gingival margin at the base of the teeth (Burton's line). "
            "Peripheral blood smear demonstrates coarse basophilic stippling (punctate basophilia) in erythrocytes. "
            "Inhibition of which two enzymes in the heme biosynthetic pathway by Lead is directly responsible "
            "for the accumulation of delta-aminolevulinic acid (ALA) and free erythrocyte protoporphyrin (FEP)?"
        ),
        "options": [
            ("Delta-Aminolevulinic Acid Dehydratase (ALAD) and Ferrochelatase", True, None),
            ("Porphobilinogen Deaminase and Uroporphyrinogen Decarboxylase", False, "PBG deaminase is deficient in Acute Intermittent Porphyria; UROD is deficient in Porphyria Cutanea Tarda."),
            ("ALA Synthase and Coproporphyrinogen Oxidase", False, "ALA synthase is the rate-limiting enzyme in heme synthesis, not inhibited by lead."),
            ("Heme Oxygenase and Biliverdin Reductase", False, "These enzymes degrade heme into biliverdin and bilirubin.")
        ],
        "pearl": "Lead Poisoning (Plumbism) Enzymes: Lead binds sulfhydryl groups on two critical heme enzymes: 1. DELTA-AMINOLEVULINIC ACID DEHYDRATASE (ALAD): Leads to accumulation of neurotoxic delta-ALA in blood and urine (responsible for lead colic and encephalopathy) | 2. FERROCHELATASE: Blocks insertion of Fe2+ into Protoporphyrin IX -> accumulation of Free Erythrocyte Protoporphyrin (FEP / Zinc Protoporphyrin). Basophilic stippling is caused by lead-induced inhibition of pyrimidine 5'-nucleotidase, causing precipitated ribosomal RNA to aggregate in RBCs.",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 24, p. 500-508.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Medical Negligence & Consent Law",
        "stem": (
            "A patient files a medical negligence suit against an orthopedic surgeon following a hip replacement complication. "
            "The court applies the landmark legal precedent established in the English case of Bolam v. Friern Hospital Management Committee (1957). "
            "According to the Bolam Test (endorsed by the Supreme Court of India in Jacob Mathew v. State of Punjab, 2005), "
            "what is the fundamental standard of care against which a doctor's professional actions are judged?"
        ),
        "options": [
            ("Whether the doctor acted in accordance with a practice accepted as proper by a responsible body of medical men skilled in that particular art, even if other doctors hold a contrary opinion", True, None),
            ("Whether the treatment resulted in a 100% cure of the underlying disease", False, "Medicine is not an exact science; lack of cure is not proof of negligence."),
            ("Whether the patient experienced any post-operative pain or temporary disability", False, "Complications and pain do not constitute negligence if standard of care was met."),
            ("Whether the doctor possessed the highest possible postgraduate academic qualification in the country", False, "The standard is ordinary competent skill, not extraordinary or highest brilliance.")
        ],
        "pearl": "Bolam Test & Jacob Mathew Verdict (Medical Negligence in India): Bolam Principle: A doctor is NOT negligent if he acted in accordance with a practice accepted as proper by a RESPONSIBLE BODY of medical opinion skilled in that field, even if contrary views exist. Supreme Court in Jacob Mathew v. State of Punjab (2005): 1. A doctor cannot be held criminally liable (IPC 304A) unless there is GROSS NEGLIGENCE or recklessness | 2. A private complaint of criminal negligence cannot be entertained by police without an independent expert medical opinion from a government doctor.",
        "citation": "Parikh's Textbook of Medical Jurisprudence, 8th Ed, Chapter 3 (Medical Ethics & Negligence), p. 52-64.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Medical Negligence & Consent Law",
        "stem": (
            "Under Indian Law and the Indian Contract Act, what is the statutory minimum age at which a mentally sound person "
            "can legally give valid, independent consent to undergo a medical examination or minor medical procedure "
            "under Section 89 and Section 90 of the Indian Penal Code (IPC)?"
        ),
        "options": [
            ("12 years of age (for medical examination / minor treatment; 18 years for surgery / major procedures under Indian Contract Act)", True, None),
            ("7 years of age", False, "A child under 7 years has absolute criminal immunity (doli incapax, Section 82 IPC), but cannot give consent."),
            ("21 years of age", False, "Age of majority is 18 years in India."),
            ("14 years of age", False, "14 years is not a statutory consent age under IPC 89/90.")
        ],
        "pearl": "Age of Consent in Medical Practice (India): Section 89 & 90 IPC: A child aged 12 YEARS OR OLDER can give valid legal consent for medical examination and minor medical treatments (Section 90 implies consent of child <12 years is invalid). Indian Contract Act: Age of majority is 18 YEARS (required for major surgical procedures, elective operations, and financial contracts). Emergency Exception (Section 92 IPC): Doctrine of Emergency allows doctors to perform emergency life-saving procedures without consent if the patient is unconscious and no guardian is immediately available.",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 2 (Legal Procedures & Consent), p. 28-36.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Suspended Animation & Brain Death Criteria",
        "stem": (
            "Under the Transplantation of Human Organs and Tissues Act (THOTA 1994, India), brain stem death must be certified "
            "by a panel of four authorized medical practitioners, including a registered neurosurgeon or neurologist. "
            "Which of the following clinical cranial nerve reflex tests is NOT an essential component of brain stem death evaluation?"
        ),
        "options": [
            ("Deep tendon knee-jerk patellar reflex", True, None),
            ("Pupillary light reflex (bilateral fixed, non-reactive pupils)", False, "Pupillary reflex tests CN II and III midbrain integrity; must be absent."),
            ("Corneal reflex (bilateral absent corneal blink reflex)", False, "Corneal reflex tests CN V and VII pontine integrity; must be absent."),
            ("Oculocephalic reflex (Doll's eye movement) and Oculovestibular test (cold caloric test)", False, "Tests CN VIII, III, VI pontine/midbrain pathways; must be absent.")
        ],
        "pearl": "Brain Stem Death Certification (THOTA India): Spinal reflexes (KNEE JERK, plantar reflex, withdrawal movements) may be PRESERVED because they are mediated by the spinal cord and DO NOT rule out brain stem death! Mandatory Brain Stem Reflexes Tested (Must ALL be Absent): 1. Pupillary light reflex (CN II, III - Midbrain) | 2. Corneal reflex (CN V, VII - Pons) | 3. Oculocephalic (Doll's eye) & Oculovestibular (Cold caloric 50 mL ice water) (CN VIII, III, VI) | 4. Gag reflex & Cough reflex on suction (CN IX, X - Medulla) | 5. APNEA TEST (CO2 challenge with PaCO2 rising to ≥60 mmHg without spontaneous respiratory effort). All tests repeated after a mandatory 6-HOUR INTERVAL.",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 7 (Brain Death), p. 126-132.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Suspended Animation & Brain Death Criteria",
        "stem": (
            "Suspended animation (apparent death) is a clinical condition where the vital functions of respiration, circulation, "
            "and cerebral activity are depressed to the minimum, undetectable by ordinary clinical bedside examination, "
            "giving the superficial appearance of death. In which of the following scenarios is suspended animation classically encountered?"
        ),
        "options": [
            ("Severe accidental hypothermia, electrocution, drowning, and newborn asphyxia neonatorum", True, None),
            ("Rigor mortis established in all limbs", False, "Established rigor mortis is definitive proof of cellular biological death, never suspended animation."),
            ("Putrefactive green discoloration of the right iliac fossa", False, "Decomposition is irreversible biological death."),
            ("Livor mortis fixed for 24 hours", False, "Fixed hypostasis proves death.")
        ],
        "pearl": "Suspended Animation (Apparent Death): State where metabolic rate drops dramatically; heartbeat and breathing are present but imperceptible with a stethoscope. Causes: 1. Newborns (Asphyxia neonatorum) | 2. Hypothermia ('No one is dead until warm and dead!') | 3. Electrocution / Lightning strike | 4. Near-drowning / Cold water immersion | 5. Voluntarily by Yogis | 6. Overdose of barbiturates, opioids, or sedatives. Active prolonged CPR and rewarming must be performed before declaring death!",
        "citation": "Reddy's Essentials of Forensic Medicine, 34th Ed, Chapter 7, p. 124-128.",
        "difficulty": "easy"
    }
]
