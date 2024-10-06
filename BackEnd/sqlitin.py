import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('Student_db.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Step 1: Create a new table with id as the primary key
#cursor.execute('''
# CREATE TABLE IF NOT EXISTS students (
#     id INTEGER PRIMARY KEY,
#     name TEXT NOT NULL,
 #    pq1 TEXT,
  #   pq2 TEXT
 #);
 #''')
# Step 2: Copy data from the old table to the new table

# Step 3: Drop the old table
# cursor.execute('DROP TABLE IF EXISTS students;')

# Step 4: Rename the new table to the original table name
# cursor.execute('ALTER TABLE students_new RENAME TO students;')
 # Replace 'students' with your table name

cursor.execute(f"PRAGMA table_info({'students'});")
table_info = cursor.fetchall()
# Extract the column names from the table info
column_names = [info[1] for info in table_info]

print(column_names)
# output_all = cursor.fetchall()
# print(output_all)

# Insert some values into the 'students' table
#cursor.execute('''
# INSERT INTO students (name, pq1, pq2)
# VALUES ('Shlok Mishra', 'What is Pythagoras Theorem', 'Explain Bayes Theorem');
# ''')
#
#cursor.execute('''
# INSERT INTO students (name, pq1, pq2)
# VALUES ('Daksh Mohan', 'What is Flux', 'Newtons Three Laws of Motion');
# ''')
# cursor.execute('''
# DELETE FROM students
# WHERE rowid NOT IN (
#     SELECT MIN(rowid)
#     FROM students
#     GROUP BY name, email, profession, age, DateOfBirth
# );
# ''')



# Commit the changes
conn.commit()

# Close the connection



def pqUpd(a, b,  iden):
    cursor.execute(f'Update students set pq2="{b}" where id={iden}')
    cursor.execute(f'Update students set pq1="{a}" where id={iden}')
    conn.commit()
cursor.execute('SELECT * FROM students;')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()

# Create a table named 'students'


# C
