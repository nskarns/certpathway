import flask 
from flask import abort, request, session, url_for, redirect
import secrets
from urllib.parse import urlencode
import CertPathway
from flask_login import LoginManager, current_user, login_required, logout_user


# TODO: Go though this code and modify it. This is exmaple code from https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023

@CertPathway.app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('show_home'))
    provider_data = CertPathway.app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)


@CertPathway.app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("show_home"))