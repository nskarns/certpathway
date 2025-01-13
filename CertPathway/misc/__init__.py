"""Miscellaneous routes for handling non-content functions"""
from CertPathway.misc.authorize import oauth2_authorize, logout
from CertPathway.misc.callback import oauth2_callback
from CertPathway.misc.user_manager import User, load_user
from CertPathway.misc.recommender import change_post