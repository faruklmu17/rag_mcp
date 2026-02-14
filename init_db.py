import sqlite3
import os

os.makedirs('db', exist_ok=True)
db_path = 'db/agile_board.db'

# Delete old DB if exists
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE engineers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT CHECK(role IN ('Developer', 'QA')) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE work_items (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT CHECK(type IN ('Story', 'Defect')) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY,
    engineer_id INTEGER,
    work_item_id INTEGER,
    status TEXT CHECK(status IN ('Developing', 'Under Review', 'Testing', 'Done', 'Ready for QA')) NOT NULL,
    FOREIGN KEY (engineer_id) REFERENCES engineers(id),
    FOREIGN KEY (work_item_id) REFERENCES work_items(id)
)
''')


# Seed engineers
engineers = [
    (1, 'Alice Smith', 'Developer'),
    (2, 'Bob Johnson', 'QA'),
    (3, 'Charlie Liu', 'Developer'),
    (4, 'Diana Patel', 'QA'),
]

# Seed work items (stories + defects)
work_items = [
    (1, 'Implement login form', 'Story'),
    (2, 'Fix logout bug', 'Defect'),
    (3, 'Add forgot password flow', 'Story'),
    (4, 'Incorrect error message on reset', 'Defect')
]

# Seed assignments
assignments = [
    (1, 1, 1, 'Developing'),
    (2, 2, 1, 'Testing'),
    (3, 3, 2, 'Under Review'),
    (4, 4, 2, 'Done'),
    (5, 1, 3, 'Under Review'),
    (6, 2, 3, 'Testing'),
    (7, 3, 4, 'Developing'),
    (8, 4, 4, 'Testing'),
    (9, 1, 4, 'Ready for QA')  # 🚨 NEW breaking row
]

cursor.executemany('INSERT INTO engineers VALUES (?, ?, ?)', engineers)
cursor.executemany('INSERT INTO work_items VALUES (?, ?, ?)', work_items)
cursor.executemany('INSERT INTO assignments VALUES (?, ?, ?, ?)', assignments)

conn.commit()
conn.close()

print("✅ Agile Board DB created with engineers, stories, defects, and status.")
