import sqlite3

conn = sqlite3.connect('admissions.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    student_class TEXT,
    district TEXT,
    status TEXT DEFAULT 'Pending'
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")