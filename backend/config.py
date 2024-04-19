from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
#cross origin resource sharing
CORS(app)
