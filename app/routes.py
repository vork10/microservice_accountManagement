from flask import render_template, request, redirect, url_for
from app import app
import firebase_admin.auth

@app.route('/login', methods=['POST'])
def login():
    # Handle user login logic here
    email = request.form['email']
    password = request.form['password']

    # Add Firebase authentication logic here
    try:
        user = firebase_admin.auth.get_user_by_email(email)
        # If user exists and password matches, redirect to dashboard
        # Note: Implement appropriate Firebase Authentication method here
        if custom_authenticate_user(email, password):
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password"  # Handle invalid credentials
    except firebase_admin.auth.UserNotFoundError:
        return "User not found"  # Handle user not found
    except firebase_admin.auth.InvalidIdTokenError:
        return "Invalid ID token"  # Handle invalid ID token
    except Exception as e:
        return "Error: " + str(e)  # Handle other exceptions

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return "Passwords do not match"
        
        try:
            user = firebase_admin.auth.create_user(
                email=email,
                password=password
            )
            # Optionally, store additional user data in Firestore
            # db_ref.collection('users').document(user.uid).set({ 'email': email })
            
            return redirect(url_for('login_page'))
        except Exception as e:
            return "Error: " + str(e)
    else:
        return render_template('register.html')

# Helper function for custom authentication logic
def custom_authenticate_user(email, password):
    # Implement your custom authentication logic here
    # For demonstration, just returning True if email and password match
    # In a real-world scenario, you would typically hash the password and check against the stored hash
    return True


@app.route('/dashboard')
def dashboard():
    # Render the dashboard page
    return render_template('dashboard.html')

@app.route('/')
def login_page():
    return render_template('loginpage.html')

@app.route('/reset_password')
def reset_password():
    # Render the password reset page
    return render_template('resetpassword.html')