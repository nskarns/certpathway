"""CertPathway development configuration."""
import pathlib
import os
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Secret key for encrypting cookies

# TODO:
# This is a horrible idea to have this here and it definitely needs to be moved out of this file
SECRET_KEY = b'''\x82\xb9U\x84<\xb38\xe6\xc2\x7f%
                 \xb1\xbd\x835G}\x11F\xfd\x06\xe2\xb9!'''



SESSION_COOKIE_NAME = 'login'
CERTPATH_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATABASE_FILENAME = CERTPATH_ROOT/'var'/'CertPathwayDB.sqlite3'
UPLOAD_FOLDER = CERTPATH_ROOT/'var'/'uploads'

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
CLIENT_ID = os.environ.get('CLIENT_ID'),
CLIENT_SECRET = os.environ.get('CLIENT_SECRET'),
OAUTH2_PROVIDERS = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
            'profile': lambda json: json,
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
    },
}