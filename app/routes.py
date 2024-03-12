from flask import render_template, request, redirect, url_for, session
from app import app
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

app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def login_page():
    return render_template('loginpage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('register.html')
        except Exception as e:
            return 'no'
    else:
        return render_template('loginpage.html')

@app.route('/reset_password')
def reset_password():
    return render_template('resetpassword.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return "Passwords do not match"
        
        try:
            auth.create_user_with_email_and_password(email, password)
            
            return redirect(url_for('login_page'))
        except Exception as e:
            return e
    else:
        return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # Render the dashboard page
    return render_template('dashboard.html')
