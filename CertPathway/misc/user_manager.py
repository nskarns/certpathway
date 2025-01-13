import CertPathway
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from oauthlib.oauth2 import WebApplicationClient
import requests

login_manager = LoginManager()
login_manager.init_app(CertPathway.app)



class User(UserMixin):
    def __init__(self, email, firstname, lastname, imagelink):
        self.id = email
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.imagelink = imagelink 

    @staticmethod
    def get(email):
        db = CertPathway.model.get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        if not user:
            return None

        user = User(
            email=user['email'], firstname=user['firstname'], lastname=user['lastname'], imagelink = user['imagelink']
        )
        return user

    @staticmethod
    def create(email, firstname, lastname, imagelink):
        db = CertPathway.model.get_db()
        db.execute(
            "INSERT INTO users (email, firstname, lastname, imagelink) "
            "VALUES (?, ?, ?, ?)",
            (email, firstname, lastname, imagelink)
        )
        db.commit()



@login_manager.user_loader
def load_user(email):
    return User.get(email)