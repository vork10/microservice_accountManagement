from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
import json
from app.scripts.communicator import Communicator
import pyrebase

config = {
    'apiKey': "AIzaSyAXyiq6xiCnaLbOcKCV23zVBO9Jc83zb94",
    'authDomain': "erdyssa.firebaseapp.com",
    'databaseURL': "https://erdyssa-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "erdyssa",
    'storageBucket': "erdyssa.appspot.com",
    'messagingSenderId': "390029170184",
    'appId': "1:390029170184:web:96edfc78b92014837d23bd",
    'measurementId': "G-40WW2CVD40"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

communicator = Communicator()


app.secret_key = 'secret'
unityrequest = False

@app.route('/')
def login_page():
    global unityrequest
    source = request.args.get('source')
    if source == 'unity':
        unityrequest = True
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global unityrequest
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email and not password:
            return render_template('loginpage.html', error_message="Please enter your email and password")
        elif not email:
            return render_template('loginpage.html', error_message="Please enter your email")
        elif not password:
            return render_template('loginpage.html', email=email, error_message="Please enter your password")
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email 
            if unityrequest == True:
                unityrequest = False
                return redirect(url_for('unity_data'))
            else:
                return redirect(url_for('dashboard'))     
        except:
            return render_template('loginpage.html', email=email, error_message="Wrong email or password")
    else:
        return render_template('loginpage.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        
        try:
            auth.send_password_reset_email(email)
            return render_template('loginpage.html', email=email, success_message="Email has been sent")
        except:
            return render_template('resetpassword.html', email=email, error_message="Something went wrong")
    return render_template('resetpassword.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', email=email, error_message="Passwords not matching")
        
        try:
            user = auth.create_user_with_email_and_password(email, password)
            print('Successfully created an account')
            user = auth.sign_in_with_email_and_password(email, password)
            print('Successfully logged in')
            session['user'] = email
            return render_template('loginpage.html')
        except:
            return render_template('register.html', email=email, error_message="Email already exists")
        
    else:
        return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    user_id = auth.current_user['localId']
    characters = ""
    
    try:
        characterapidata = Communicator.get_data(communicator, f"http://44.220.151.108/api/data/{user_id}")

        stringified_json_objects = json.loads(characterapidata)

        characters = [json.loads(obj) for obj in stringified_json_objects]
    except:
        pass
        
    user = session['user']

    return render_template('dashboard.html', user=user, characters=characters)

@app.route('/unity_data', methods=['GET'])
def unity_data():
    try:
        user_id = auth.current_user['localId']
        return jsonify({'user_id': user_id})
    except Exception as e:
        return jsonify({'error': 'Error processing request: ' + str(e)}), 500