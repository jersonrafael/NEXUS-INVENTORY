from flask import Flask
from flask_cors import CORS

import os
from dotenv import load_dotenv

load_dotenv()

# START APP
app = Flask(__name__)
app.secret_key = os.getenv("secret_key")
UPLOAD_FOLDER = os.getenv("folder_route")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from routes import route



