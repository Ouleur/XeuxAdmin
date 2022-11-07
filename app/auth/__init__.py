"""
Ce module est fait pour s'authentifier
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
