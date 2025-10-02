import sqlite3

conn = sqlite3.connect('dist/xojo.db')
cur = conn.cursor()

print("=== Classes with 'timer' ===")
rows = cur.execute("SELECT name FROM classes WHERE name LIKE '%timer%'").fetchall()
for r in rows:
    print(r[0])

print("\n=== Classes with 'runmode' ===")
rows = cur.execute("SELECT name FROM classes WHERE name LIKE '%runmode%'").fetchall()
for r in rows:
    print(r[0])

print("\n=== Properties with 'runmode' ===")
rows = cur.execute("SELECT classes.name, properties.name FROM properties JOIN classes ON properties.class_id = classes.id WHERE properties.name LIKE '%runmode%' OR properties.description LIKE '%runmode%' LIMIT 10").fetchall()
for r in rows:
    print(f"{r[0]}.{r[1]}")

print("\n=== Full text search for 'runmode' ===")
rows = cur.execute("SELECT name FROM classes WHERE id IN (SELECT class_id FROM class_fts WHERE class_fts MATCH 'runmode') LIMIT 10").fetchall()
for r in rows:
    print(r[0])

conn.close()
