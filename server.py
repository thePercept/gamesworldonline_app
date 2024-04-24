from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pymysql

 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypassword'
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

            # Inserting Games List

            cursor.execute('SELECT * FROM games')
            games = cursor.fetchall()
            cart = session.get('cart', [])              

            site_data ={
                'userdata':{
                    'username':account['username'],
                    'email':account['email'],
                },
                'gamedata':games,
                'cart':cart
            }
            return redirect(url_for('list_games'))    
            

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



@app.route('/users')
def list_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
    users = cursor.fetchall()
    return render_template('users.html', users=users)


@app.route('/games')
def list_games():
    email=None
    print("Session is ",session)
    if 'email' in session:
        email = session['email']
    print(email)


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
    account = cursor.fetchone()    

    cursor.execute('SELECT * FROM games')
    games = cursor.fetchall()
    cart = session.get('cart', [])     

         

    site_data ={
        'userdata':{
            'username':account['username'],
            'email':account['email'],
        },
        'gamedata':games,
        'cart':cart
    }
    return render_template('games.html',site_data=site_data)



def get_game_info(game_id):
    try:
        # Connect to the database
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Execute query to fetch game price
            cursor.execute('SELECT id,base_price,game_name FROM games WHERE id = %s', (game_id,))
            game = cursor.fetchone()

            print("Getting game",game)

            if game:
                return game # Return the price if game found
            else:
                return None  # Return None if game not found

    except pymysql.Error as err:
        print("Error accessing database:", err)
        return None

    finally:
        if 'connection' in locals():
            connection.close()

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    print(request.json)
    game_id = request.json.get('gameId') 
    game_info = get_game_info(game_id)
    print("GAME ID RECIEVED",game_id)
    print("CART VALUE ",session)
    print("CART VALUE ",game_info)
    if 'cart' not in session:
        print("Cart DATA Not Present ")
        session['cart'] = []  # Initialize cart if not exists in session
        session['cart'].append({'id': game_info['id'], 'name':game_info['game_name'], 'price':game_info['base_price'] })  # Add the gameId to the cart
    else:
        print("Cart DATA  Present ",session['cart'])
        print("Adding More in Session",game_id)
        temp = session['cart']
        temp.append({'id': game_info['id'], 'name':game_info['game_name'], 'price':game_info['base_price'] })
        session['cart']= temp  # Add the gameId to the cart
    return jsonify({'message': 'Game added to cart successfully'}), 200 


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    game_id = request.json.get('gameId')
    print("Here ??",game_id)

    cart = session['cart']
    for item in cart:
        print(item['id'] == game_id)
        if item['id'] == game_id:
            cart.remove(item)
            session['cart'] = cart
            return jsonify({'message': 'Game removed from cart successfully'}), 200            
        else:
            return jsonify({'error': 'Game ID not found in cart'}), 404  









if __name__ == "__main__":
    app.run(host="localhost")