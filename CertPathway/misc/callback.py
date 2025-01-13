# TODO: Go though this code and modify it. This is exmaple code from https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023
import flask 
from flask import abort, request, session, url_for, redirect, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import json
import CertPathway
from CertPathway.misc.user_manager import User
import requests


@CertPathway.app.route('/callback/<provider>')
def oauth2_callback(provider):
    if flask.session.get("logID"):
        return redirect(url_for('show_home'))

    print("=============================================")
    print("Doing Callback")

    provider_data = CertPathway.app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    print("Fetched Provider Data")

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('show_home'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    print("Verified State")
    
    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    print("Verified Code")
    print("=============================================")


    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)

    email = provider_data['userinfo']['email'](response.json())
    profile = provider_data['userinfo']['profile'](response.json())
    firstname = profile["given_name"]
    lastname = profile["family_name"]
    imagelink = profile["picture"]
    
    print("=============================================")
    print(json.dumps(profile, indent=2))
    print("=============================================")
    # find or create the user in the database
    user = User(email=email, firstname=firstname, lastname=lastname, imagelink=imagelink)

# Doesn't exist? Add it to the database.
    if not User.get(email):
        User.create(email=email, firstname=firstname, lastname=lastname, imagelink=imagelink)

    # log the user in
    login_user(user)
    return redirect(url_for('show_home'))