from flask  import Flask, render_template, request
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    gender TEXT NOT NULL
                )''')
conn.commit()


# Function to add user to database
def add_user(name, email, password, gender):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (name, email, password, gender) 
                      VALUES (?, ?, ?, ?)''', (name, email, password, gender))
    conn.commit()
    conn.close()



def email_exists(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None
    


# Function to retrieve user by email
def get_user_by_email(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user 





@app.route('/')
def index():
  return render_template ('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']

        if email_exists(email):
            message = "User already registered. Please login instead."
        else:
            add_user(name, email, password, gender)
            message = "Registration successful! You can now login."

    return render_template('index.html',message=message )


if __name__ == '__main__':
    app.run(debug=True)