from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AITkWu7p'
app.config['MYSQL_DB'] = 'gameworlds_db'
 
 
mysql = MySQL(app)
 
 
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE email = % s \
            AND password = % s', (email, password ))
        account = cursor.fetchone()
        if account:
            print("Account found ....")
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully ! USERNAME IS : {}'.format(account['username'])
            return render_template('index.html', msg=msg)
        else:
            print("Account not found ....")
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)
 
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))    





@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        if 'password' in request.form and 'email' in request.form:
            password = request.form['password']
            email = request.form['email']
            username = request.form['username']

            # Check if account already exists
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            else:
                # Insert new account into the database
                cursor.execute('INSERT INTO accounts (username ,password, email, usercategory) VALUES (%s, %s, %s, %s)', (username ,password, email, "customer"))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
        else:
            msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)




if __name__ == "__main__":
    app.run(host="localhost")