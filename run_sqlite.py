import sqlite3

conn = sqlite3.connect('analytics.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM analytics")
rows = cursor.fetchall()
print(rows)  # Make sure there is actual data
conn.close()
