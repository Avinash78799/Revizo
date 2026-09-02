import sqlite3
import random


def main():
    conn = sqlite3.connect("neet_pg.db")
    c = conn.cursor()

    STEM_TEMPLATES = [
        "A patient presents with clinical and diagnostic findings characteristic of {concept}. Which of the following is the most appropriate finding or intervention?",
        "In a patient being evaluated for features consistent with {concept}, which option best reflects the established next step in management or diagnosis?",
        "Which of the following statements most accurately describes the standard evidence-based approach to {concept} in the context of {subject}?",
        "A clinical vignette consistent with {concept} is presented. Based on current {subject} guidelines, which of the following represents the correct finding or management step?",
    ]
    CORRECT_PHRASES = [
        "Represents the primary, first-line, evidence-based finding or intervention for {concept}",
        "Is the standard-of-care finding/management step most consistent with {concept}",
        "Correctly identifies the established diagnostic or therapeutic approach to {concept}",
    ]
    WRONG_PHRASE_POOLS = [
        ("Reflects a secondary or differential feature that is not the primary finding in {concept}", "Incorrect — describes a differential feature, not the primary finding."),
        ("Describes an intervention that is contraindicated in the clinical context of {concept}", "Incorrect — contraindicated in this clinical setting."),
        ("Describes a finding seen only in atypical or late-stage presentations of {concept}", "Incorrect — associated only with rare or late complications, not the typical presentation."),
        ("Reflects an outdated or superseded approach no longer recommended for {concept}", "Incorrect — superseded by current standard-of-care guidance."),
    ]

    questions = c.execute("""
        SELECT q.id, c.name as concept_name, s.name as subject_name, q.question_text
        FROM questions q
        JOIN concepts c ON q.concept_id = c.id
        JOIN topics t ON c.topic_id = t.id
        JOIN chapters ch ON t.chapter_id = ch.id
        JOIN subjects s ON ch.subject_id = s.id
    """).fetchall()

    print(f"Processing {len(questions)} questions...")

    updated_count = 0
    flagged_for_manual_review = []

    for q_id, concept_name, subject_name, old_text in questions:
        is_templated = "Clinical scenario regarding" in old_text or "CANDIDATE" in old_text

        if is_templated:
            # Synthetic placeholder — safe to fully regenerate.
            stem_template = random.choice(STEM_TEMPLATES)
            new_stem = stem_template.format(concept=concept_name, subject=subject_name)
            correct_key = random.choice(["A", "B", "C", "D"])

            c.execute("UPDATE questions SET question_text = ?, correct_explanation = ? WHERE id = ?",
                      (new_stem, f"Option {correct_key} represents the established evidence-based finding/management for {concept_name}.", q_id))

            c.execute("DELETE FROM question_options WHERE question_id = ?", (q_id,))
            option_keys = ["A", "B", "C", "D"]
            wrong_keys = [k for k in option_keys if k != correct_key]
            wrong_pool = random.sample(WRONG_PHRASE_POOLS, 3)
            correct_phrase = random.choice(CORRECT_PHRASES).format(concept=concept_name)

            c.execute("""INSERT INTO question_options (id, question_id, option_key, option_text, is_correct, why_wrong_explanation, created_at)
                         VALUES (lower(hex(randomblob(16))), ?, ?, ?, 1, NULL, CURRENT_TIMESTAMP)""",
                      (q_id, correct_key, correct_phrase))
            for wk, (phrase_template, why_wrong) in zip(wrong_keys, wrong_pool):
                c.execute("""INSERT INTO question_options (id, question_id, option_key, option_text, is_correct, why_wrong_explanation, created_at)
                             VALUES (lower(hex(randomblob(16))), ?, ?, ?, 0, ?, CURRENT_TIMESTAMP)""",
                          (q_id, wk, phrase_template.format(concept=concept_name), why_wrong))

        else:
            # REAL question — DO NOT touch question_text or guess correctness.
            # Read actual is_correct, reassign only the KEY (A/B/C/D label),
            # never the text-to-correctness mapping.
            existing_opts = c.execute(
                "SELECT id, option_key, option_text, is_correct, why_wrong_explanation FROM question_options WHERE question_id = ?",
                (q_id,)
            ).fetchall()

            if len(existing_opts) != 4:
                flagged_for_manual_review.append((q_id, f"expected 4 options, found {len(existing_opts)}"))
                continue

            correct_rows = [o for o in existing_opts if o[3] == 1]
            if len(correct_rows) != 1:
                # Ambiguous or already-corrupted correctness (0 or 2+ correct flags,
                # e.g. possibly from the earlier buggy script run) — do not guess.
                # Flag for a human to verify against the source/explanation text.
                flagged_for_manual_review.append((q_id, f"found {len(correct_rows)} options flagged correct, expected exactly 1"))
                continue

            option_keys = ["A", "B", "C", "D"]
            random.shuffle(option_keys)
            # Phase 1: Set temporary keys to avoid UNIQUE (question_id, option_key) constraint
            for (opt_id, old_key, opt_text, is_correct, why_wrong), new_key in zip(existing_opts, option_keys):
                c.execute("UPDATE question_options SET option_key = ? WHERE id = ?", (f"TEMP_{new_key}", opt_id))
            # Phase 2: Set final keys
            for (opt_id, old_key, opt_text, is_correct, why_wrong), new_key in zip(existing_opts, option_keys):
                c.execute("UPDATE question_options SET option_key = ? WHERE id = ?", (new_key, opt_id))

        updated_count += 1

    conn.commit()
    conn.close()

    print(f"Updated {updated_count} questions.")
    if flagged_for_manual_review:
        print(f"\n{len(flagged_for_manual_review)} questions could NOT be safely auto-fixed and need manual review:")
        for q_id, reason in flagged_for_manual_review:
            print(f"  - {q_id}: {reason}")
        print("\nThese are likely ones the earlier buggy reseed script already touched.")
        print("Check them against your original source material before trusting their 'correct' answer.")


if __name__ == "__main__":
    main()
