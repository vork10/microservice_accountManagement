import os
from flask import Flask
import webbrowser

# Create Flask application instance
app = Flask(__name__)

# Specify template and static file paths
app.template_folder = 'templates'
app.static_folder = 'static'

# Open browser
webbrowser.open_new('http://127.0.0.1:5000')

# Import routes from the app package
from app import routes
