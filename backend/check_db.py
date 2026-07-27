import sqlite3

conn = sqlite3.connect('reviewguard.db')

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables:', tables)

for t in tables:
    cols = conn.execute(f"PRAGMA table_info({t[0]})").fetchall()
    print(f"\n{t[0]} columns:", [c[1] for c in cols])

    rows = conn.execute(f"SELECT * FROM {t[0]} LIMIT 3").fetchall()
    for r in rows:
        print(" row:", r[:3])

conn.close()
