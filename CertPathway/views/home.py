import flask
from flask import Flask, render_template, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, current_user, login_required, logout_user
import os
import CertPathway 

@CertPathway.app.route("/")
def show_home():

    context = {
        "current_user" : current_user
    }

    return render_template("home.html", **context)




@CertPathway.app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(CertPathway.app.root_path, 'static/images'),
                               'favicon.ico')