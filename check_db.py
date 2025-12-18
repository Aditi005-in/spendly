import sqlite3

conn = sqlite3.connect("app/spendly.db")
cursor = conn.cursor()

# tables check
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in DB:")
for t in tables:
    print(t[0])

conn.close()
