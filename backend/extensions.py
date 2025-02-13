from authlib.integrations.flask_client import OAuth
import os
from flask_mail import Mail

oauth = OAuth()
mail = Mail()

def init_mail(app):
    mail.init_app(app)

def init_oauth(app):
    # Google OAuth setup
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_params=None,
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'email profile'},
        # server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )
    return google