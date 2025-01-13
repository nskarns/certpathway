"""CertPathway initializer."""
from flask import Flask
# app is a single object used by all the code modules in this package
app = Flask(__name__)
# Read settings from config module (CertPathway/config.py)
app.config.from_object('CertPathway.config')
# import CertPathway.misc  
import CertPathway.model
import CertPathway.views
import CertPathway.misc
import CertPathway.api