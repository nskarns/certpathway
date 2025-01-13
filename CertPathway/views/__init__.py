"""CertPathway Views Module, functions imported from .py files"""
from flask import Flask
from CertPathway.views.home import show_home
from CertPathway.views.home import favicon
from CertPathway.views.explore import show_explore
from CertPathway.views.interest_form import show_interest_form
from CertPathway.views.login import show_login
from CertPathway.views.profile import show_profile
from CertPathway.views.utils import cert