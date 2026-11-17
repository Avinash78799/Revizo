"""
Authentic High-Yield NEET-PG Clinical Questions for Dermatology
References: Neena Khanna's Illustrated Synopsis of Dermatology and Sexually Transmitted Diseases (6th Ed), Fitzpatrick's Dermatology in General Medicine (9th Ed)
"""

DERMATOLOGY_QUESTIONS = [
    {
        "concept_name": "Core Principles: Psoriasis Vulgaris & Nail Changes",
        "stem": (
            "A 34-year-old male presents with chronic, itchy, erythematous plaques covered by thick, silvery-white micaceous scales "
            "over both extensor surfaces of his elbows, knees, and lumbosacral region. "
            "When the scales are gently scraped with a glass slide, they peel off in thin layers resembling candle grease. "
            "Upon removing the last adherent translucent membrane (membrane of Duncan-Bulkley), pinpoint punctate bleeding droplets "
            "appear on the exposed erythematous base. What is the name of this pathognomonic physical examination sign?"
        ),
        "options": [
            ("Auspitz Sign", True, None),
            ("Nikolsky Sign", False, "Nikolsky sign is tangential shearing dislodgement of the superficial epidermis seen in Pemphigus vulgaris and SJS/TEN."),
            ("Darier Sign", False, "Darier sign is whealing, erythema, and pruritus upon stroking a mastocytoma / urticaria pigmentosa lesion."),
            ("Asboe-Hansen Sign (Bulla-Spread Sign)", False, "Asboe-Hansen sign is lateral extension of an intact blister when pressure is applied to its center.")
        ],
        "pearl": "Psoriasis Vulgaris Signs: 1. Candle Grease Sign: Grattage test yields silvery scales. 2. Membrane of Duncan-Bulkley: Thin moist pellicle exposed after scaling. 3. AUSPITZ SIGN: Pinpoint bleeding droplets upon removal of the membrane, caused by thinning of suprapapillary epidermal plates over dilated, tortuous dermal capillary loops. 4. Koebner Phenomenon (Isomorphic response): Development of characteristic psoriatic lesions along lines of trauma/scratching.",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 5 (Psoriasis), p. 68-78.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Psoriasis Vulgaris & Nail Changes",
        "stem": (
            "A 40-year-old female with long-standing plaque psoriasis presents for evaluation of fingernail abnormalities. "
            "On inspection, her nails exhibit multiple tiny, irregularly scattered, punctate depressions on the dorsal nail plate, "
            "along with circumscribed, yellowish-brown translucent patches beneath the nail plate resembling drops of oil ('oil-drop sign' / salmon patch), "
            "and distal subungual hyperkeratosis. Which specific part of the nail apparatus is pathologically involved to produce nail pitting?"
        ),
        "options": [
            ("Proximal Nail Matrix", True, None),
            ("Distal Nail Matrix", False, "Distal nail matrix involvement causes leukonychia, not pitting."),
            ("Nail Bed", False, "Nail bed involvement produces the 'oil-drop' salmon patch and subungual hyperkeratosis."),
            ("Hyponychium", False, "Hyponychium causes distal onycholysis, not matrix pitting.")
        ],
        "pearl": "Psoriasis Nail Changes Pathology: Proximal Nail Matrix involvement -> PITTING (multiple, irregular, thimble-like pits due to parakeratotic cell shedding) and Beau's lines. Nail Bed involvement -> 'Oil Drop' / Salmon patch (exudative collection of neutrophils/serum) and Subungual hyperkeratosis. Distal Hyponychium -> Onycholysis (separation of nail plate from bed). Most common nail sign in psoriasis: Pitting (50-80%).",
        "citation": "Fitzpatrick's Dermatology in General Medicine, 9th Ed, Chapter 28, p. 450-462.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Pemphigus Vulgaris vs Bullous Pemphigoid",
        "stem": (
            "A 45-year-old male presents with painful, widespread oral mucosal erosions that have made swallowing difficult for 3 months, "
            "followed by the appearance of thin-walled, flaccid, clear bullae on apparently normal skin over the scalp, chest, and back. "
            "The blisters rupture easily upon light friction, leaving tender, raw, denuded oozing areas that crust but fail to heal. "
            "Firm sliding pressure with a finger on normal-appearing perilesional skin causes tangential shearing detachment of the epidermis (Nikolsky sign POSITIVE). "
            "Tzanck smear from the base of an unroofed bulla demonstrates rounded, detached, hyperchromatic keratinocytes with perinuclear halos. "
            "What autoantibodies and target antigens are responsible for this intraepidermal blistering disorder?"
        ),
        "options": [
            ("IgG autoantibodies directed against Desmoglein 3 (and Desmoglein 1) in desmosomes causing intraepidermal acantholysis", True, None),
            ("IgG autoantibodies directed against BP180 (Type XVII collagen) and BP230 in hemidesmosomes", False, "Anti-BP180/BP230 antibodies cause Bullous Pemphigoid, which features SUBEPIDERMAL tense bullae with negative Nikolsky sign."),
            ("IgA autoantibodies against Epidermal Transglutaminase depositing in dermal papillae", False, "IgA anti-transglutaminase deposits cause Dermatitis Herpetiformis associated with Celiac disease."),
            ("Autoantibodies directed against Type VII collagen in anchoring fibrils", False, "Anti-type VII collagen antibodies cause Epidermolysis Bullosa Acquisita (EBA).")
        ],
        "pearl": "Pemphigus Vulgaris vs Bullous Pemphigoid: Pemphigus Vulgaris: Middle-aged (40-60 yrs), ORAL EROSIONS PRECEDES SKIN (100%), FLACCID thin-walled bullae, intraepidermal suprabasal acantholysis ('tombstone appearance' of basal layer), Nikolsky sign POSITIVE, Asboe-Hansen positive, Tzanck smear: ACANTHOLYTIC TZANCK CELLS. Target: Desmoglein 3 (mucosa) & Desmoglein 1 (skin). Direct Immunofluorescence (DIF): 'Fishnet' / lace-like intercellular IgG deposits. Bullous Pemphigoid: Elderly (>70 yrs), TENSE thick-walled bullae on erythematous urticarial base, subepidermal, oral lesions rare (10-20%), Nikolsky NEGATIVE. Target: BP180/BP230 hemidesmosomes. DIF: Linear basement membrane zone IgG/C3.",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 10 (Vesiculobullous Diseases), p. 142-156.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Pemphigus Vulgaris vs Bullous Pemphigoid",
        "stem": (
            "A 78-year-old male presents with intensely pruritic, urticarial erythematous plaques on his thighs and lower abdomen for 3 weeks, "
            "upon which large, tense, dome-shaped bullae containing serous fluid have developed. "
            "None of the bullae rupture easily under pressure, and the Nikolsky sign is strictly negative. "
            "There are no oral erosions. Skin biopsy reveals a subepidermal blister containing numerous eosinophils. "
            "Direct Immunofluorescence (DIF) microscopy of perilesional skin reveals which characteristic diagnostic pattern?"
        ),
        "options": [
            ("Continuous linear deposition of IgG and C3 along the dermo-epidermal basement membrane zone (BMZ)", True, None),
            ("Intraepidermal intercellular 'fishnet-like' pattern of IgG around keratinocytes", False, "Intercellular fishnet/lace-like pattern is pathognomonic for Pemphigus vulgaris."),
            ("Granular deposition of IgA clumps concentrated exclusively in the tips of dermal papillae", False, "Granular IgA in dermal papillae is diagnostic of Dermatitis Herpetiformis."),
            ("Dense band-like perivascular lymphocytic infiltrate without immunoreactant deposition", False, "Non-specific inflammatory pattern seen in drug eruptions.")
        ],
        "pearl": "Bullous Pemphigoid DIF: Continuous LINEAR band of IgG and Complement C3 deposited along the dermo-epidermal junction / Basement Membrane Zone (BMZ). Target antigens: BP180 (collagen XVII, specifically the NC16A domain) and BP230. First-line treatment: Superpotent topical corticosteroids (Clobetasol propionate cream) or systemic oral Prednisolone.",
        "citation": "Fitzpatrick's Dermatology in General Medicine, 9th Ed, Chapter 54, p. 920-934.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Lichen Planus Pathognomonic Features",
        "stem": (
            "A 36-year-old male presents with intensely pruritic, violaceous, flat-topped, polygonal papules and plaques "
            "symmetrically distributed over the flexor aspects of his wrists and forearms. "
            "On close magnification with dermoscopy, a delicate network of white, lace-like lines and puncta is visible on the surface of the papules. "
            "Inspection of the oral cavity reveals asymptomatic bilateral reticular white streaks on the buccal mucosa. "
            "What is the eponym for these surface white lines, and what histopathological hallmark of the basal layer is seen on skin biopsy?"
        ),
        "options": [
            ("Wickham's Striae; Liquefactive basal cell degeneration with Civatte (colloid) apoptotic bodies and dense band-like lymphocytic infiltrate", True, None),
            ("Herald patch; Microscopic microabscesses of Munro in the stratum corneum", False, "Munro microabscesses and herald patch are seen in Psoriasis and Pityriasis Rosea, respectively."),
            ("Gottron's papules; Dermal mucin deposition", False, "Gottron's papules are pathognomonic for Dermatomyositis on the MCP and IP joints."),
            ("Heliotrope sign; Subcutaneous fat necrosis with calcification", False, "Heliotrope rash is violaceous periorbital edema seen in Dermatomyositis.")
        ],
        "pearl": "Lichen Planus 6 Ps: Pruritic, Polygonal, Planar (flat-topped), Purple/Violaceous, Papules & Plaques on flexor wrists/shins. Surface feature: WICKHAM'S STRIAE (due to focal hypergranulosis). Mucosal involvement: 70% have oral reticular white lacy streaks. Histopathology: 1. Dense band-like / lichenoid dermal lymphocytic infiltrate hugging the junction | 2. Liquefactive degeneration of basal layer | 3. Civatte / Colloid / Cytoid apoptotic keratinocyte bodies | 4. 'Saw-tooth' appearance of rete ridges | 5. Wedge-shaped Hypergranulosis.",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 6 (Lichen Planus), p. 82-90.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Lichen Planus Pathognomonic Features",
        "stem": (
            "In patients with severe hypertrophic Lichen Planus of the pretibial shins or Lichen Planopilaris of the scalp, "
            "which chronic viral infection has a statistically significant epidemiological and pathogenetic association with Lichen Planus, "
            "warranting routine screening?"
        ),
        "options": [
            ("Hepatitis C Virus (HCV)", True, None),
            ("Cytomegalovirus (CMV)", False, "CMV is not etiologically linked to lichen planus."),
            ("Human Papillomavirus Type 16 (HPV-16)", False, "HPV-16 is oncogenic for cervical and anogenital squamous cell cancers."),
            ("Epstein-Barr Virus (EBV)", False, "EBV is associated with Oral Hairy Leukoplakia and Burkitt lymphoma.")
        ],
        "pearl": "Lichen Planus & Hepatitis C: Strong clinical association between oral/cutaneous Lichen Planus and Hepatitis C Virus (HCV) infection, particularly in Mediterranean, Japanese, and Indian populations. All patients with generalized or mucosal lichen planus should be screened with anti-HCV serology. Treatment of choice for localized cutaneous LP: High-potency topical steroids (Clobetasol); Severe generalized LP: Oral Prednisolone or Acitretin.",
        "citation": "Fitzpatrick's Dermatology in General Medicine, 9th Ed, Chapter 32, p. 520-528.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Ridley-Jopling Leprosy Classification & Reactions",
        "stem": (
            "A 32-year-old male from an endemic region presents with 2 well-defined, hypoesthetic, hypopigmented macules with raised, erythematous margins "
            "over his left forearm and right cheek. Light touch and thermal sensation are markedly impaired within the lesions. "
            "The left greater auricular nerve and right ulnar nerve are thickened, firm, and non-tender. "
            "Slit-skin smear is negative for acid-fast leproma bacilli (Bacteriological Index = 0). Lepromin skin test demonstrates strong induration (Fernandez and Mitsuda positive). "
            "According to the Ridley-Jopling scale and WHO operational classification, how is this case classified, and what is the standard WHO Multi-Drug Therapy (MDT) regimen?"
        ),
        "options": [
            ("Tuberculoid Leprosy (TT / Paucibacillary); 6-month regimen of monthly supervised Rifampicin (600 mg) plus daily self-administered Dapsone (100 mg)", True, None),
            ("Lepromatous Leprosy (LL / Multibacillary); 12-month regimen of Rifampicin, Clofazimine, and Dapsone", False, "Lepromatous leprosy (LL) features diffuse infiltrative leonine facies, BI 5-6+, and negative lepromin test."),
            ("Borderline Lepromatous (BL); Monthly Clofazimine alone for 24 months", False, "Clofazimine monotherapy is inadequate and risks drug resistance."),
            ("Indeterminate Leprosy; Single-dose ROM (Rifampicin, Ofloxacin, Minocycline)", False, "Single-dose ROM is no longer recommended by WHO.")
        ],
        "pearl": "Ridley-Jopling Leprosy Spectrum: TT (Tuberculoid) -> BT (Borderline Tuberculoid) -> BB (Mid-borderline) -> BL (Borderline Lepromatous) -> LL (Lepromatous). TT: High cell-mediated immunity (CMI), Mitsuda lepromin POSITIVE, lesions few (1-3), well-defined, complete anesthesia, BI = 0. LL: Absent CMI, Mitsuda NEGATIVE, numerous bilateral symmetrical shiny infiltrative macules/nodules, glove-and-stocking hypoesthesia, leonine facies, BI = 4-6+. WHO Operational Classification: Paucibacillary (PB: 1-5 skin lesions, ≤1 nerve) -> 6 months Rifampicin + Dapsone. Multibacillary (MB: ≥6 lesions, >1 nerve) -> 12 months Rifampicin + Clofazimine + Dapsone.",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 17 (Leprosy), p. 254-278.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Ridley-Jopling Leprosy Classification & Reactions",
        "stem": (
            "A 28-year-old male with Borderline Lepromatous (BL) leprosy on WHO Multibacillary MDT presents with high fever, malaise, "
            "and the sudden eruption of multiple, crops of painful, tender, bright red subcutaneous erythematous nodules (Erythema Nodosum Leprosum / ENL) "
            "over his arms, thighs, and face. He also has bilateral acute ulnar neuritis with severe neuralgic pain. "
            "This is a Type 2 Lepra Reaction. What is the fundamental immunological mechanism and the definitive drug of choice for severe ENL?"
        ),
        "options": [
            ("Type III immune-complex hypersensitivity (Arthus reaction); Thalidomide (or high-dose Oral Prednisolone)", True, None),
            ("Type IV delayed-type hypersensitivity reaction; Acyclovir and Methotrexate", False, "Type IV delayed hypersensitivity is the mechanism of Type 1 (Reversal) reaction occurring in borderline leprosy (BT/BB/BL)."),
            ("Type I IgE-mediated immediate anaphylaxis; Epinephrine and Cetirizine", False, "Type 2 reaction is not an IgE anaphylactic reaction."),
            ("Direct mycobacterial bacteremia; Intravenous Vancomycin", False, "ENL is an immune complex-mediated phenomenon, not acute staphylococcal sepsis.")
        ],
        "pearl": "Lepra Reactions: Type 1 Reaction (Reversal Reaction): Seen in Borderline spectrum (BT, BB, BL). Mechanism: Type IV Delayed Hypersensitivity (increase or decrease in CMI). Features: Existing lesions become erythematous, swollen, and tender; acute neuritis. DOC: Oral Systemic Corticosteroids (Prednisolone). Type 2 Reaction (Erythema Nodosum Leprosum - ENL): Seen in BL and LL. Mechanism: Type III Immune Complex Hypersensitivity (antigen-antibody complexes + complement activation + high TNF-alpha). Features: Crops of painful evanescent erythematous nodules + fever, arthralgia, iridocyclitis, orchitis. DOC: THALIDOMIDE (100-300 mg/day; inhibits TNF-alpha) or Prednisolone (Note: Continue regular MDT throughout both reactions!).",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 17, p. 270-276.",
        "difficulty": "hard"
    },
    {
        "concept_name": "Core Principles: Syphilis Stages & Serology",
        "stem": (
            "A 26-year-old sexually active male presents with a solitary, indurated, painless ulcer on the coronal sulcus of his penis "
            "that appeared 3 weeks after an unprotected sexual encounter. On examination, the ulcer has a clean base with regular, rolled-in margins "
            "and a cartilage-like button induration upon palpation (Hunterian chancre). There is discrete, firm, non-tender, non-suppurative bilateral inguinal lymphadenopathy. "
            "Darkfield microscopy of exudate from the chancre demonstrates slender, motile, corkscrew-shaped spirochetes exhibiting characteristic flexion and rotation. "
            "What is the first-line therapeutic regimen of choice recommended by CDC and WHO guidelines for Primary Syphilis?"
        ),
        "options": [
            ("Benzathine Penicillin G (2.4 million units intramuscularly in a single dose)", True, None),
            ("Oral Doxycycline 100 mg twice daily for 3 days", False, "Doxycycline is an alternative for penicillin-allergic patients and must be given for 14 days, not 3 days."),
            ("Intravenous Ceftriaxone 2 g daily for 21 days", False, "Intravenous ceftriaxone for 14-21 days is reserved for Neurosyphilis, not uncomplicated primary chancre."),
            ("Oral Azithromycin 1 g single dose", False, "Azithromycin is prone to high Treponema pallidum macrolide resistance (A2058G mutation) and is not first-line.")
        ],
        "pearl": "Primary Syphilis: Incubation period: 9-90 days (average 21 days). Lesion: HARD CHANCRE (Hunterian chancre): Solitary, PAINLESS, indurated button-like base, clean floor, no purulent discharge. Painless, non-suppurative 'shotty' lymphadenopathy. Darkfield microscopy is the earliest diagnostic test. TREATMENT OF CHOICE: Benzathine Penicillin G: 2.4 million units IM single dose (1.2 million units in each buttock). For Late Latent or Tertiary Syphilis: Benzathine Penicillin G 2.4 million units IM weekly for 3 consecutive weeks.",
        "citation": "CDC STI Treatment Guidelines (2021) / Neena Khanna Ch 20 (Syphilis), p. 308-320.",
        "difficulty": "easy"
    },
    {
        "concept_name": "Core Principles: Syphilis Stages & Serology",
        "stem": (
            "A patient treated for secondary syphilis is being monitored to determine therapeutic cure versus reinfection. "
            "Which of the following serological assays is a non-treponemal test that detects antibodies against cardiolipin-lecithin antigen, "
            "correlates directly with disease activity, and exhibits a 4-fold decrease in titer following successful therapy?"
        ),
        "options": [
            ("Venereal Disease Research Laboratory (VDRL) and Rapid Plasma Reagin (RPR)", True, None),
            ("Fluorescent Treponemal Antibody Absorption (FTA-ABS)", False, "FTA-ABS is a treponemal-specific test that remains positive for life despite successful treatment and cannot monitor response."),
            ("Treponema Pallidum Particle Agglutination (TPPA)", False, "TPPA is a treponemal-specific test that stays permanently reactive."),
            ("Microhemagglutination assay for Treponema pallidum (MHA-TP)", False, "MHA-TP is a specific treponemal test that remains lifelong positive.")
        ],
        "pearl": "Syphilis Serology: Non-Treponemal Tests (VDRL, RPR): Detect anti-cardiolipin reaginic antibodies. Highly sensitive, inexpensive, TITER correlates with disease activity. A 4-fold titer drop (e.g., from 1:32 to 1:8) confirms cure. False positives seen in: Pregnancy, Leprosy, Malaria, SLE, Rheumatoid arthritis, IV drug abuse. Treponemal-Specific Tests (FTA-ABS, TPHA, TPPA): Detect specific anti-treponemal antibodies. Used for confirmation; REMAIN POSITIVE FOR LIFE (cannot monitor reinfection or cure).",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 20, p. 314-318.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Genital Ulcer Disease Syndromic Management",
        "stem": (
            "A 29-year-old truck driver presents with three excruciatingly painful, non-indurated, ragged, soft ulcers on his glans penis. "
            "The base of the ulcers is covered with necrotic, purulent, yellowish-grey exudate that bleeds easily on touch. "
            "In the left groin, there is a large, fluctuant, exquisitely tender, unilocular suppurative lymph node (bubo) with erythema of the overlying skin. "
            "Gram stain of the purulent exudate demonstrates Gram-negative coccobacilli arranged in parallel chains resembling a 'school of fish' or 'railroad tracks'. "
            "What is the causative organism and the diagnosis?"
        ),
        "options": [
            ("Haemophilus ducreyi; Chancroid (Soft Sore)", True, None),
            ("Treponema pallidum; Primary Syphilis (Hard Chancre)", False, "Syphilis chancre is painless, solitary, indurated, and lymph nodes never suppurate or become fluctuant."),
            ("Chlamydia trachomatis L1-L3; Lymphogranuloma Venereum (LGV)", False, "LGV presents with a transient painless herpetiform vesicle followed weeks later by painful multilocular buboes divided by Poupart's ligament (Groove sign of Greenblatt)."),
            ("Klebsiella granulomatis; Granuloma Inguinale (Donovanosis)", False, "Donovanosis causes painless, beefy-red exuberant pseudo-buboes that bleed easily on contact with safety-pin Donovan bodies on smear.")
        ],
        "pearl": "Genital Ulcers Key Differentials: 1. Chancroid (Haemophilus ducreyi): PAINFUL, soft, multiple ragged ulcers, bleeds easily. Suppurative unilateral fluctuant BUBO (aspirate, never incise!). Gram stain: 'School of fish' / 'Railroad track' arrangement. Treatment: Azithromycin 1 g oral single dose OR Ceftriaxone 250 mg IM single dose. 2. Granuloma Inguinale (Donovanosis / Klebsiella granulomatis): PAINLESS, beefy red granulation tissue, pseudo-buboes, Donovan bodies (safety-pin bipolar staining). 3. Herpes Genitalis (HSV-2): Grouped painful vesicles on erythematous base -> Tzanck smear multinucleated giant cells.",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 21 (STIs), p. 326-338.",
        "difficulty": "moderate"
    },
    {
        "concept_name": "Core Principles: Superficial Fungal Dermatophytoses",
        "stem": (
            "A 21-year-old college student presents with multiple asymptomatic, mildly pruritic, scaly, hypo- and hyperpigmented circular macules "
            "coalescing across his upper chest, back, and shoulders. The lesions become noticeably more prominent after sun exposure in summer. "
            "Gently stretching or scraping the skin produces fine, branny, furfuraceous scales (Coup d'ongle sign / Besnier sign). "
            "Under Wood's lamp examination, the lesions emit a characteristic pale golden-yellow fluorescence. "
            "Potassium Hydroxide (10% KOH) mount of skin scrapings reveals which classic microscopic appearance?"
        ),
        "options": [
            ("Short, thick, stubby, unbranched hyphae mixed with clusters of round budding yeast cells ('Spaghetti and Meatballs' appearance)", True, None),
            ("Long, branching, true septate hyphae with dichotomous 45-degree angles", False, "Septate 45-degree branching hyphae are characteristic of Aspergillus."),
            ("Pseudohyphae with true budding blastospores and positive germ tube test", False, "Pseudohyphae and germ tubes are diagnostic of Candida albicans."),
            ("Broad, aseptate, ribbon-like hyphae with 90-degree right-angle branching", False, "Aseptate 90-degree hyphae are characteristic of Mucor / Rhizopus.")
        ],
        "pearl": "Pityriasis Versicolor (Tinea Versicolor): Causative organism: Malassezia furfur (lipophilic dimorphic fungus, normal skin commensal). Lesions: Hypo- or hyperpigmented macules with fine 'branny' scales (Besnier sign / Coup d'ongle positive). Wood's Lamp: Golden yellow fluorescence. KOH mount: Classic 'SPAGHETTI AND MEATBALLS' appearance (short curved hyphae + clusters of yeast). Treatment: Topical Ketoconazole 2% shampoo or Selenium Sulfide 2.5% lotion; Oral Itraconazole for widespread disease.",
        "citation": "Neena Khanna's Illustrated Synopsis of Dermatology, 6th Ed, Chapter 13 (Fungal Infections), p. 192-202.",
        "difficulty": "easy"
    }
]
