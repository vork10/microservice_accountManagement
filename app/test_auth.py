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
