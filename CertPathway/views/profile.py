import flask
from flask import Flask, render_template, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, current_user, login_required, logout_user
import os
import CertPathway 
from CertPathway.views.utils import cert

@CertPathway.app.route("/profile/")
def show_profile():
    if current_user.is_anonymous:
        redirect(url_for("show_home"))

    certs = []

    context = {
        "current_user" : current_user,
        "certificates" : certs
    }

    return render_template("profile.html", **context)