from flask import Flask, render_template, request, redirect, url_for, flash
from database import create_connection, create_user_table, insert_user, email_exists

app = Flask(__name__)
app.secret_key = '12345678'


#DATABASE CONNECTIONS MANAGEMENT

conn = create_connection()
create_user_table(conn)


#APP ROUTES FOR WEBSITES 

@app.route('/')
def home():
  return render_template('home.html')



@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
         

        # Check if email already exists
        if email_exists(conn, email):
            flash('Account already exists. Please login instead.', 'error')
        else:
            # Insert new user into the database
            user_id = insert_user(conn, name, email, password, gender)
            if user_id:
                flash('Successfully registered! You can now login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error registering. Please try again.', 'error')  

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email and password match
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        if user:
            # Redirect to dashboard if login successful
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Display dashboard if user is logged in
    return render_template('dashboard.html')





#START THE FLASK APP 

if __name__ == '__main__':
    app.run(debug=True,threaded=False )