import sqlite3

# Connect to a SQLite database (it will create the file if it doesn't exist)
print("Debug: Before connecting to the database")
conn = sqlite3.connect('aichatbot.db')
print("Debug: After connecting to the database")

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute SQL commands
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        first_name TEXT,
        last_name TEXT
    )
''')

def register_user(email, password, first_name, last_name):
    conn = sqlite3.connect('aichatbot.db')
    cursor = conn.cursor()

    # Insert user data into the users table
    cursor.execute('''
        INSERT INTO users (email, password, first_name, last_name)
        VALUES (?, ?, ?, ?)
    ''', (email, password, first_name, last_name))

def login_user(email, password):
    conn = sqlite3.connect('aichatbot.db')
    cursor = conn.cursor()

    # Retrieve user data by email
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user_data = cursor.fetchone()

    if user_data and user_data[2] == password:
        # Login successful
        return user_data  # Return user data as a tuple (id, email, password, first_name, last_name)

    conn.close()
    return None  # Login failed

# Commit the changes and close the connection
conn.commit()
conn.close()
