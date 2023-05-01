from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import Etudiant,Filiere
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
    


@api.route('/etudiant/add', methods=['POST','GET'])
def etudiant_add():
    form =request.get_json() or {}
    print(form)
    form = form["root"]
    try: 
        filiere = Filiere.query.filter_by(denomination=form['filiere']).first()
    except:
        filiere = Filiere.query.filter_by(id=form['filiere_id']).first()

    if filiere:
        form['filiere'] =  filiere.id
    else:
        filiere = Filiere(denomination=form['filiere'])
        db.session.add(filiere)
        db.session.commit()
        form['filiere'] =  filiere.id



   # filename = None
   # if request.files['image']:
   #    data = request.files['image']
   #    filename = secure_filename(data.filename)
   #    if not exists(os.path.join(uploads_dir, filename)):
   #       data.save(os.path.join(uploads_dir, filename))
      
#    try:  
    etudiant = Etudiant(matricule=form['matricule'],nom=form['nom'],prenoms=form['prenoms'],filiere_id=form['filiere'],niveau=form['niveau'],date_naissance=form['date_naissance'],etat=form['etat'],antenne=form['antenne'],photo=form['photo'])
    db.session.add(etudiant)
    db.session.commit()
    return jsonify(etudiant.to_json())
