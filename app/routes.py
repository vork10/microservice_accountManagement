from flask import render_template, request, redirect, url_for
from app import app
import firebase_admin
from firebase_admin import auth, credentials


cred = credentials.Certificate("erdyssa-default-rtdb-export.json")
firebase_app = firebase_admin.initialize_app(cred)

@app.route('/')
def login_page():
    return render_template('loginpage.html')

@app.route('/login', methods=['POST'])
def login():
    # Handle user login logic here
    email = request.form['email']
    password = request.form['password']
    # Authenticate user and redirect accordingly
    return redirect(url_for('dashboard'))

@app.route('/reset_password')
def reset_password():
    # Render the password reset page
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
            user = auth.create_user(
                email=email,
                password=password
            )
            # Optionally, store additional user data in Firestore
            # firestore.collection('users').document(user.uid).set({ 'email': email })
            
            return redirect(url_for('login_page'))
        except firebase_admin.auth.AuthError as e:
            return "Error: " + str(e)
    else:
        return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # Render the dashboard page
    return render_template('dashboard.html')
