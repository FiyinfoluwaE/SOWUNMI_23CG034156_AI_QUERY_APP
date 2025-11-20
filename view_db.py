import sqlite3

# Connect to the database
connection = sqlite3.connect('queries.db')
cursor = connection.cursor()

try:
    # Select all rows from the interaction_logs table
    cursor.execute("SELECT * FROM interaction_logs")
    rows = cursor.fetchall()

    print(f"Total Records Found: {len(rows)}\n")
    print("-" * 50)
    
    for row in rows:
        # row[0] is ID, row[1] is Question, row[2] is Answer
        print(f"ID: {row[0]}") 
        print(f"User Asked: {row[1]}")
        print(f"AI Replied: {row[2][:100]}...") # Shows first 100 chars of answer
        print("-" * 50)

except sqlite3.OperationalError:
    print("Table not found! Did you run the app and ask a question yet?")

connection.close()