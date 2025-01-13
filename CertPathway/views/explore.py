import flask
from flask import Flask, render_template
from flask import Flask, redirect, url_for, session
from CertPathway.views.utils import cert
import CertPathway



@CertPathway.app.route('/explore/')
def show_explore():
    """Display /explore/ route."""
    
    certs = []


    context = { 
        "certificates": certs
    }
    return render_template('explore.html', **context)