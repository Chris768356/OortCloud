import os 
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_UPLOAD_FOLDER = os.environ.get("BASE_UPLOAD_PATH")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
USER_QUOTA = 50 * 1000 * 1000