import sqlite3

conn = sqlite3.connect("neet_pg.db")
c = conn.cursor()

print("=" * 70)
print("  REVIZO FULL HEALTH CHECK")
print("=" * 70)

# 1. Total questions
total = c.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
print(f"\n1. TOTAL QUESTIONS: {total}")

# 2. Option key distribution
print("\n2. CORRECT ANSWER KEY DISTRIBUTION:")
dist = c.execute("""
    SELECT option_key, COUNT(*)
    FROM question_options
    WHERE is_correct = 1
    GROUP BY option_key
    ORDER BY option_key
""").fetchall()
for key, cnt in dist:
    pct = cnt / total * 100
    print(f"   Option {key}: {cnt} ({pct:.1f}%)")

# 3. Option integrity
print("\n3. OPTION INTEGRITY CHECK:")
bad_correct = c.execute("""
    SELECT q.id, COUNT(CASE WHEN qo.is_correct=1 THEN 1 END) as correct_count
    FROM questions q
    JOIN question_options qo ON qo.question_id = q.id
    GROUP BY q.id
    HAVING correct_count != 1
""").fetchall()
print(f"   Questions with != 1 correct option: {len(bad_correct)}")

bad_count = c.execute("""
    SELECT q.id, COUNT(qo.id) as opt_count
    FROM questions q
    JOIN question_options qo ON qo.question_id = q.id
    GROUP BY q.id
    HAVING opt_count != 4
""").fetchall()
print(f"   Questions with != 4 options: {len(bad_count)}")

# 4. Template/placeholder markers
print("\n4. PLACEHOLDER / TEMPLATE MARKERS:")
candidate_marker = c.execute("SELECT COUNT(*) FROM questions WHERE question_text LIKE '%CANDIDATE%'").fetchone()[0]
hash_marker = c.execute("SELECT COUNT(*) FROM questions WHERE question_text LIKE '%#%'").fetchone()[0]
clinical_scenario = c.execute("SELECT COUNT(*) FROM questions WHERE question_text LIKE '%Clinical scenario regarding%'").fetchone()[0]
print(f"   Contains CANDIDATE: {candidate_marker}")
print(f"   Contains #: {hash_marker}")
print(f'   Contains "Clinical scenario regarding": {clinical_scenario}')

# 5. Subject distribution
print("\n5. QUESTIONS PER SUBJECT:")
subjects = c.execute("""
    SELECT s.name, COUNT(q.id) as qcount
    FROM questions q
    JOIN concepts c ON q.concept_id = c.id
    JOIN topics t ON c.topic_id = t.id
    JOIN chapters ch ON t.chapter_id = ch.id
    JOIN subjects s ON ch.subject_id = s.id
    GROUP BY s.name
    ORDER BY qcount DESC
""").fetchall()
for name, cnt in subjects:
    print(f"   {name}: {cnt}")
print(f"   --- Total subjects: {len(subjects)} ---")

# 6. TEMP_ keys left behind
temp_keys = c.execute("SELECT COUNT(*) FROM question_options WHERE option_key LIKE 'TEMP_%'").fetchone()[0]
print(f"\n6. TEMP_ KEYS LEFT BEHIND: {temp_keys}")

# 7. Duplicate option keys per question
dup_keys = c.execute("""
    SELECT question_id, option_key, COUNT(*)
    FROM question_options
    GROUP BY question_id, option_key
    HAVING COUNT(*) > 1
""").fetchall()
print(f"   Duplicate option keys in same question: {len(dup_keys)}")

# 8. Sample 3 real questions with options
print("\n7. SAMPLE REAL QUESTIONS WITH OPTIONS (verify correctness mapping):")
samples = c.execute("""
    SELECT q.id, q.question_text
    FROM questions q
    WHERE q.question_text NOT LIKE '%standard evidence-based approach%'
      AND q.question_text NOT LIKE '%clinical vignette consistent with%'
      AND q.question_text NOT LIKE '%being evaluated for features%'
      AND q.question_text NOT LIKE '%diagnostic findings characteristic%'
    LIMIT 3
""").fetchall()
for qid, qtext in samples:
    print(f"\n   Q: {qtext[:150]}...")
    opts = c.execute(
        "SELECT option_key, option_text, is_correct FROM question_options WHERE question_id = ? ORDER BY option_key",
        (qid,),
    ).fetchall()
    for ok, ot, ic in opts:
        flag = " <<< CORRECT" if ic else ""
        print(f"      {ok}. {ot[:90]}{flag}")

conn.close()
print("\n" + "=" * 70)
print("  HEALTH CHECK COMPLETE")
print("=" * 70)
