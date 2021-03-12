from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import User,Etudiant,Presence
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import subprocess


auth = HTTPBasicAuth()


#Create presence
@api.route('/add_presence',methods=['POST','GET'])
def add_presence():

    #recherche du matricule 
    ###### OU ######
    #recherche de la Card ID
    etudiant = Etudiant()
    if hasattr(request.json,'matricule'):
        etudiant = Etudiant.query.filter_by(matricule=request.json['matricule']).first()
    elif hasattr(request.json,'card_id'):
        etudiant = Etudiant.query.filter_by(card_id=request.json['card_id']).first()

    
    if etudiant:
        #Etudiant trouver 
        #Creation de la presence
        presence = Presence(etudiant_id="",filiere_id="1",matiere_id="1",device_id="1",niveau="1",annee_academic_id="1")
        #revoie des informations de l'Etudian
        db.session.add(presence)
        db.session.commit()

        return jsonify({"Message":"Vous êtes présent !!"})
    return jsonify({"Message":"Une erreur s'est produite!!"})
    
