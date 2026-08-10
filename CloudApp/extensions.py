from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()

migrate = Migrate()

login_manager.login_view = "auth.login"

login_manager.login_message = "Bitte melde dich an, um auf diese Seite zuzugreifen."

login_manager.login_message_category = "error"

limiter = Limiter(
    key_func=get_remote_address,  

    storage_uri="memory://",      
    
    default_limits=["200 per day", "50 per hour"] 
)