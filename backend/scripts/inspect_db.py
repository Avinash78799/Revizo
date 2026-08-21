import sqlite3

conn = sqlite3.connect('neet_pg.db')
cursor = conn.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables in neet_pg.db:")
for t in tables:
    name = t[0]
    count = cursor.execute(f'SELECT count(*) FROM "{name}"').fetchone()[0]
    print(f"  {name}: {count}")

# Check questions status distribution
if ('questions',) in tables:
    print("\nQuestions status distribution:")
    status_counts = cursor.execute("SELECT status, count(*) FROM questions GROUP BY status").fetchall()
    for s, c in status_counts:
        print(f"  status='{s}': {c}")
        
    print("\nQuestions trust_class distribution:")
    trust_counts = cursor.execute("SELECT trust_class, count(*) FROM questions GROUP BY trust_class").fetchall()
    for tr, c in trust_counts:
        print(f"  trust_class='{tr}': {c}")
