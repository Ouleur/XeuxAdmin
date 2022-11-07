"""
Ce module est pour effectuer des actions sur les informations
des étudiants 
Verification
Ajout
Controle des informations

Sans se connecter 
"""
from flask import Blueprint
from ..models.models import Permission

etudiant = Blueprint('etudiant', __name__)

from . import views





