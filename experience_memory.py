import sqlite3

conn = sqlite3.connect("experience.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS experience (
    task TEXT,
    steps TEXT,
    result TEXT,
    success INTEGER
)
""")
conn.commit()

def save_experience(task, steps, result, success=True):
    cur.execute(
        "INSERT INTO experience VALUES (?, ?, ?, ?)",
        (task, steps, result, int(success))
    )
    conn.commit()