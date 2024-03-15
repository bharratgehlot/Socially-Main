from flask import Flask, g
import sqlite3

app = Flask(__name__)
DATABASE = 'social_network.db'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Function to create the user table
def create_user_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            gender TEXT
        )
    ''')
    conn.commit()

# Function to insert a new user into the database
def insert_user(name, email, password, gender):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, email, password, gender)
        VALUES (?, ?, ?, ?)
    ''', (name, email, password, gender))
    conn.commit()

# Function to check if email already exists in the database
def email_exists(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    return cursor.fetchone() is not None

# Close the database connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
