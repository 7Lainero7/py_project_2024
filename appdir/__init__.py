import dotenv
import os

from flask import Flask
from flask_cors import CORS

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("secret")
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

pass_db = os.getenv("pass_db")


from appdir import routes_api