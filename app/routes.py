import logging
from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
import json
from app.scripts.communicator import Communicator
import pyrebase
import os

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Firebase Configuration
config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'databaseURL': os.getenv('FIREBASE_DB_URL'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_BUCKET_NAME'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

communicator = Communicator()

app.secret_key = os.getenv('SECRET_KEY')
unityrequest = False

@app.route('/')
def login_page():
    global unityrequest
    source = request.args.get('source')
    if source == 'unity':
        unityrequest = True
    logger.debug("Redirecting to login page from /")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global unityrequest
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        logger.debug(f"Attempting login with email: {email}")

        if not email and not password:
            logger.warning("Missing both email and password")
            return render_template('loginpage.html', error_message="Please enter your email and password")
        elif not email:
            logger.warning("Missing email")
            return render_template('loginpage.html', error_message="Please enter your email")
        elif not password:
            logger.warning("Missing password")
            return render_template('loginpage.html', email=email, error_message="Please enter your password")

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = auth.get_account_info(user['idToken'])['users'][0]['localId']
            session['user'] = email
            session['user_id'] = user_id
            logger.info(f"Successfully logged in: {email}")
            logger.debug(f"User ID for {email}: {user_id}")
            print(f"User ID for {email}: {user_id}", flush=True)
            if unityrequest:
                unityrequest = False
                return redirect(url_for('unity_data'))
            else:
                logger.debug("nigger")
                return redirect(url_for('dashboard'))
        except Exception as e:
            logger.error(f"Login failed for {email}: {e}", exc_info=True)
            return render_template('loginpage.html', email=email, error_message="Wrong email or password")
    else:
        return render_template('loginpage.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        logger.debug(f"Password reset request for email: {email}")

        try:
            auth.send_password_reset_email(email)
            logger.info(f"Password reset email sent to {email}")
            return render_template('loginpage.html', email=email, success_message="Email has been sent")
        except Exception as e:
            logger.error(f"Error sending password reset email to {email}: {e}", exc_info=True)
            return render_template('resetpassword.html', email=email, error_message="Something went wrong")
    return render_template('resetpassword.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        logger.debug(f"Registration attempt with email: {email}")

        if password != confirm_password:
            logger.warning(f"Passwords do not match for {email}")
            return render_template('register.html', email=email, error_message="Passwords not matching")

        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = auth.get_account_info(user['idToken'])['users'][0]['localId']
            logger.info(f"Account created successfully for {email}")
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            session['user_id'] = user_id
            logger.debug(f"User ID for {email}: {user_id}")
            print(f"User ID for {email}: {user_id}", flush=True)
            return render_template('loginpage.html')
        except Exception as e:
            logger.error(f"Error creating account for {email}: {e}", exc_info=True)
            return render_template('register.html', email=email, error_message="Email already exists")
    else:
        return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    logger.info(f"User {session.get('user', 'unknown')} logged out")
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print("Entering the dashboard route", flush=True)
    app.logger.info("Entering the dashboard route")
    user = session.get('user')
    user_id = session.get('user_id')

    if not user or not user_id:
        logger.warning('No user session found. Redirecting to login.')
        print("No user session found. Redirecting to login.", flush=True)
        return redirect(url_for('login'))
    
    logger.debug(f"Authenticated user ID: {user_id}")
    print(f"Authenticated user ID: {user_id}", flush=True)
    characterapidata = Communicator.get_data(communicator, f"http://13.60.46.33/api/data/{user_id}")

    stringified_json_objects = json.loads(characterapidata)
    characters = [json.loads(obj) for obj in stringified_json_objects]
    logger.debug(f"Characters data for user ID {user_id}: {characters}")
    print(f"Characters data for user ID {user_id}: {characters}", flush=True)

    logger.info(f"Rendering dashboard for user {user} with characters data")
    print(f"Rendering dashboard for user {user} with characters data", flush=True)
    return render_template('dashboard.html', user=user, characters=characters)

@app.route('/unity_data', methods=['GET'])
def unity_data():
    try:
        user_id = session.get('user_id')
        if not user_id:
            raise Exception('User ID not found in session')
        logger.debug(f"Unity data request for user ID: {user_id}")
        print(f"Unity data request for user ID: {user_id}", flush=True)
        return jsonify({'user_id': user_id})
    except Exception as e:
        logger.error(f"Error processing unity data request: {e}", exc_info=True)
        print(f"Error processing unity data request: {e}", flush=True)
        return jsonify({'error': 'Error processing request: ' + str(e)}), 500
