from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import Etudiant
from flask import g, jsonify,request
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import subprocess


auth = HTTPBasicAuth()


#Create presence
@api.route('/check_etudiant/<mtle>',methods=['POST','GET'])
def check_etudiant(mtle):

    #recherche du matricule 
    etudiant = Etudiant.query.filter_by(matricule=mtle).first()

    #Etudiant trouver 
    if etudiant:
        #revoie des informations de l'Etudiant
        print(etudiant.to_json())
        return jsonify(etudiant.to_json())
    else:
        return jsonify({ 'message': "Aucun resultat" })



#Create presence
@api.route('/enroll_etudiant/<mtle>/<card_id>',methods=['POST','GET'])
def enroll_etudiant(mtle,card_id):

    #recherche du etudiant 
    etudiant = Etudiant.query.filter_by(matricule=mtle.replace(' ','')).first()
    if etudiant:
        etudiant.card_id = card_id

        #Mise à jour de l'etudiant
        db.session.add(etudiant)
        db.session.commit()
        #Creation de la presence
        return jsonify({ 'statut': "Succes" ,'etudiant':etudiant.to_json()})    
    return jsonify({ 'statut': "Echec" })
    

#Create presence
@api.route('/update_etudiant/<mtle>',methods=['POST','GET'])
def update_etudiant(mtle):

    #recherche du matricule 
    etudiant = Etudiant.query.filter_by(matricule=mtle).first()

    #Etudiant trouver 
    if etudiant:
        #revoie des informations de l'Etudiant
        etudiant.nom = request.json["nom"]
        etudiant.prenoms = request.json["prenoms"]
        etudiant.matricule = request.json["matricule"]
        etudiant.card_id = request.json["card_id"]
        etudiant.niveau = request.json["niveau"]
        etudiant.date_naissance = request.json["date_naissance"]
        etudiant.antenne = request.json["antenne"]
        etudiant.groupe = request.json["groupe"]
        etudiant.filiere_id = request.json["filiere_id"]
        db.session.add(etudiant)
        db.session.commit()
        
        return jsonify(etudiant.to_json())
    else:
        return jsonify({ 'message': "Aucun resultat" })