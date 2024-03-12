from flask import Flask
import webbrowser
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

# Create Flask application instance
app = Flask(__name__)

# Specify template and static file paths
app.template_folder = 'templates'
app.static_folder = 'static'

try:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("erdyssa-default-rtdb-export.json")
    firebase_app = initialize_app(cred)
    # Get a reference to the Firestore database
    db_ref = firestore.client()
    print("Firebase initialized successfully")
except Exception as e:
    print("Firebase initialization failed:", e)

# Open browser
webbrowser.open_new('http://127.0.0.1:5000')

# Import routes from the app package
from app import routes
