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
@api.route('/add_card_presence/<card>',methods=['POST','GET'])
def add_card_presence(card):

    #recherche du matricule 
    ###### OU ######
    #recherche de la Card ID
    etudiant = Etudiant.query.filter_by(card_id=card).first()

    
    if etudiant:
        #Etudiant trouver 
        #Creation de la presence
        presence = Presence(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,device_id="1",niveau=etudiant.niveau,annee_academic_id="1")
        #revoie des informations de l'Etudian
        db.session.add(presence)
        db.session.commit()

        return jsonify({"Message":"Vous êtes présent !!"})
    return jsonify({"Message":"Une erreur s'est produite!!"})

#Create presence
@api.route('/add_mtle_presence/<mtle>',methods=['POST','GET'])
def add_mtle_presence(mtle):

    #recherche du matricule 
    ###### OU ######
    #recherche de la Card ID
    etudiant = Etudiant.query.filter_by(matricule=request.json['matricule']).first()

    
    if etudiant:
        #Etudiant trouver 
        #Creation de la presence
        presence = Presence(etudiant_id="",filiere_id="1",matiere_id="1",device_id="1",niveau="1",annee_academic_id="1")
        #revoie des informations de l'Etudian
        db.session.add(presence)
        db.session.commit()

        return jsonify({"Message":"Vous êtes présent !!"})
    return jsonify({"Message":"Une erreur s'est produite!!"})
    
