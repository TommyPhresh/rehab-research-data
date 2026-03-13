from flask_login import UserMixin
from extensions import login_manager

users = {"demo": {"password": "demo_project"},
         "pmr": {"password": "pmrresearch"}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

def register_user_loader():
    @login_manager.user_loader
    def load_user(user_id):
        if user_id in users:
            return User(user_id)
