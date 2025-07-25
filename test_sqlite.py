# import sqlite3
# import os

# db_path = os.path.join('C:\\Sridhar\\Python\\AI_Projects\\blog-content-generator', 'blogs.db')
# try:
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS blogs
#                      (id INTEGER PRIMARY KEY, topic TEXT, category TEXT, region TEXT, content TEXT, keywords TEXT)''')
#     cursor.execute('INSERT INTO blogs (topic, category, region, content, keywords) VALUES (?, ?, ?, ?, ?)',
#                    ('Test Blog', 'Technology', 'US', 'This is a test blog.', 'test,keyword'))
#     conn.commit()
#     print(f"Database created and test blog inserted successfully at {db_path}")
#     conn.close()
# except Exception as e:
#     print(f"SQLite error: {str(e)}")

import sqlite3

conn = sqlite3.connect('analytics.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        category TEXT,
        region TEXT,
        keywords TEXT,
        analysis TEXT
    )
''')

cursor.execute('''
    INSERT INTO analytics (topic, category, region, keywords, analysis)
    VALUES (?, ?, ?, ?, ?)
''', ("AI in Healthcare", "Technology", "Europe", "AI, Healthcare, Trends", "AI is transforming healthcare..."))

conn.commit()
conn.close()
print("Sample data inserted.")
