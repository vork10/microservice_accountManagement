from flask import Flask, render_template, request, redirect, url_for

from app import app

print("Loading routes.py")

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

@app.route('/register')
def register():
    # Render the registration page
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # Render the dashboard page
    return "Dashboard Page"

if __name__ == '__main__':
    app.run(debug=True)
