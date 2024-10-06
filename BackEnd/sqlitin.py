import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('Student_db.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Step 1: Create a new table with id as the primary key
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS students_new (
#     id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     profession TEXT,
#     age INTEGER,
#     DateOfBirth TEXT
# );
# ''')

# Step 2: Copy data from the old table to the new table

# Step 3: Drop the old table
# cursor.execute('DROP TABLE IF EXISTS students;')

# Step 4: Rename the new table to the original table name
# cursor.execute('ALTER TABLE students_new RENAME TO students;')
cursor.execute("Update students set (;")  # Replace 'students' with your table name
table_info = cursor.fetchall()

# Extract the column names from the table info
column_names = [info[1] for info in table_info]

print(column_names)
# output_all = cursor.fetchall()
# print(output_all)

# Insert some values into the 'students' table
# cursor.execute('''
# INSERT INTO students (name, email, profession, age, DateOfBirth)
# VALUES ('Shlok Mishra', 'shlok@example.com', 'Student', 20, '2004-01-01');
# ''')
#
# cursor.execute('''
# INSERT INTO students (name, email, profession, age, DateOfBirth)
# VALUES ('Daksh Mohan', 'daksh@example.com', 'Student', 21, '2003-02-02');
# ''')
# cursor.execute('''
# DELETE FROM students
# WHERE rowid NOT IN (
#     SELECT MIN(rowid)
#     FROM students
#     GROUP BY name, email, profession, age, DateOfBirth
# );
# ''')

cursor.execute('SELECT * FROM students;')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Commit the changes
conn.commit()

# Close the connection
conn.close()


# Create a table named 'students'


# C
