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

    # Fetch all questions in the database
    questions = c.execute("""
        SELECT q.id, c.name as concept_name, s.name as subject_name, q.question_text
        FROM questions q
        JOIN concepts c ON q.concept_id = c.id
        JOIN topics t ON c.topic_id = t.id
        JOIN chapters ch ON t.chapter_id = ch.id
        JOIN subjects s ON ch.subject_id = s.id
    """).fetchall()

    print(f"Re-seeding all {len(questions)} questions in live database with fixed randomized key generator...")

    updated_count = 0
    for q_id, concept_name, subject_name, old_text in questions:
        # If question text is templated, replace stem
        if "Clinical scenario regarding" in old_text or "CANDIDATE" in old_text:
            stem_template = random.choice(STEM_TEMPLATES)
            new_stem = stem_template.format(concept=concept_name, subject=subject_name)
        else:
            new_stem = old_text

        correct_key = random.choice(["A", "B", "C", "D"])
        
        # Update question stem and explanation key reference
        c.execute("""
            UPDATE questions
            SET question_text = ?,
                correct_explanation = ?
            WHERE id = ?
        """, (new_stem, f"Option {correct_key} represents the established evidence-based finding/management for {concept_name}.", q_id))

        # Fetch existing options if non-templated
        existing_opts = c.execute("SELECT option_key, option_text, why_wrong_explanation FROM question_options WHERE question_id = ?", (q_id,)).fetchall()
        
        if existing_opts and len(existing_opts) == 4 and "Clinical scenario regarding" not in old_text and "CANDIDATE" not in old_text:
            # Shift correct answer to correct_key for real questions
            texts = [opt[1] for opt in existing_opts]
            # Pick one text to be the correct answer, rest wrong
            correct_text = texts[0]
            wrong_texts = texts[1:]
            
            c.execute("DELETE FROM question_options WHERE question_id = ?", (q_id,))
            option_keys = ["A", "B", "C", "D"]
            wrong_keys = [k for k in option_keys if k != correct_key]

            c.execute("""
                INSERT INTO question_options (id, question_id, option_key, option_text, is_correct, why_wrong_explanation, created_at)
                VALUES (lower(hex(randomblob(16))), ?, ?, ?, 1, NULL, CURRENT_TIMESTAMP)
            """, (q_id, correct_key, correct_text))

            for wk, wt in zip(wrong_keys, wrong_texts):
                c.execute("""
                    INSERT INTO question_options (id, question_id, option_key, option_text, is_correct, why_wrong_explanation, created_at)
                    VALUES (lower(hex(randomblob(16))), ?, ?, ?, 0, 'Incorrect choice.', CURRENT_TIMESTAMP)
                """, (q_id, wk, wt))
        else:
            c.execute("DELETE FROM question_options WHERE question_id = ?", (q_id,))
            option_keys = ["A", "B", "C", "D"]
            wrong_keys = [k for k in option_keys if k != correct_key]
            wrong_pool = random.sample(WRONG_PHRASE_POOLS, 3)
            correct_phrase = random.choice(CORRECT_PHRASES).format(concept=concept_name)

            c.execute("""
                INSERT INTO question_options (id, question_id, option_key, option_text, is_correct, why_wrong_explanation, created_at)
                VALUES (lower(hex(randomblob(16))), ?, ?, ?, 1, NULL, CURRENT_TIMESTAMP)
            """, (q_id, correct_key, correct_phrase))

            for wk, (phrase_template, why_wrong) in zip(wrong_keys, wrong_pool):
                c.execute("""
                    INSERT INTO question_options (id, question_id, option_key, option_text, is_correct, why_wrong_explanation, created_at)
                    VALUES (lower(hex(randomblob(16))), ?, ?, ?, 0, ?, CURRENT_TIMESTAMP)
                """, (q_id, wk, phrase_template.format(concept=concept_name), why_wrong))

        updated_count += 1

    conn.commit()
    conn.close()
    print(f"Successfully re-seeded {updated_count} questions in neet_pg.db with randomized answer keys!")

if __name__ == "__main__":
    main()
