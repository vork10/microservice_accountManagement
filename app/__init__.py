import os
from flask import Flask

# Create Flask application instance
app = Flask(__name__)

# Specify template and static file paths
app.template_folder = 'templates'
app.static_folder = 'static'

# Import routes from the app package
from app import routes
