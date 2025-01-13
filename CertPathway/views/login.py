import flask
from flask import Flask, render_template
from flask import Flask, redirect, url_for, session
import CertPathway 

@CertPathway.app.route("/login/")
def show_login():
    return render_template("login.html")