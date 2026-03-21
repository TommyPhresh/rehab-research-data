from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache

login_manager = LoginManager()
mail = Mail()
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
login_manager.login_view = 'main.login'