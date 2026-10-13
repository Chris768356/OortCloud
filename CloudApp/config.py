import os 
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_UPLOAD_FOLDER = os.environ.get("BASE_UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "zip"}
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
USER_QUOTA = 50 * 1000 * 1000