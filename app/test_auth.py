import os
import pytest
import pyrebase
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_and_login(client):
    # Firebase configuration
    config = {
        'apiKey': os.getenv('AIzaSyAXyiq6xiCnaLbOcKCV23zVBO9Jc83zb94'),
        'authDomain': os.getenv('erdyssa.firebaseapp.com'),
        'databaseURL': os.getenv('https://erdyssa-default-rtdb.europe-west1.firebasedatabase.app'),
        'projectId': os.getenv('erdyssa'),
        'storageBucket': os.getenv('erdyssa.appspot.com'),
        'messagingSenderId': os.getenv('390029170184'),
        'appId': os.getenv('390029170184:web:96edfc78b92014837d23bd'),
        'measurementId': os.getenv('G-40WW2CVD40')
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    
    # Test credentials
    test_email = "testuser@example.com"
    test_password = "test_password"
    
    # Register the user
    try:
        user = auth.create_user_with_email_and_password(test_email, test_password)
        assert user is not None
        print("User registration successful.")
    except Exception as e:
        pytest.fail(f"User registration failed: {e}")
    
    # Authenticate the user
    try:
        user = auth.sign_in_with_email_and_password(test_email, test_password)
        assert user is not None
        print("User authentication successful.")
    except Exception as e:
        pytest.fail(f"User authentication failed: {e}")

if __name__ == '__main__':
    pytest.main()
