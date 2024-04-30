from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import User,Etudiant,Presence,EtudiantControle,PresenceStage
from flask import g, jsonify
from sqlalchemy.exc import IntegrityError
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import subprocess
import csv
import io
import os
from ...utilities import *
import requests


auth = HTTPBasicAuth()


#Create presence
@api.route('/insertFiles',methods=['POST','GET'])
def add_card_presence():
    arr = os.listdir(current_app.config['UPLOADS_DIR'])
    print(arr)
    for fi in arr:
        with open(current_app.config['UPLOADS_DIR']+fi, newline='') as csvfile:
            csv.delimiter = ';'
            # stream = io.StringIO(csvfile.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                etudiant = Etudiant.query.filter((Etudiant.matricule=="{}".format(row['Matricule']) )| (Etudiant.card_id=="{}".format(row['ID_card']))).first()
                if etudiant:
                    presence = Presence(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,niveau=etudiant.niveau,date_badge=row["Date"])
                    try:
                        db.session.add(presence)
                        db.session.commit()
                    except IntegrityError as error:
                        db.session.rollback()
                        # pass
        # os.remove(current_app.config['UPLOADS_DIR']+fi)
    #recherche du matricule 
    ###### OU ######
    # if etudiant:
    #     #Etudiant trouver 
    #     #Creation de la presence
    #     presence = Presence(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,device_id="1",niveau=etudiant.niveau,annee_academic_id="1")
    #     #revoie des informations de l'Etudian
    #     db.session.add(presence)
    #     db.session.commit()

    #     return jsonify({"Message":"Vous êtes présent !!"})
    return jsonify({"Message":"Une erreur s'est produite!!"})

#Create presence
@api.route('/add_presence',methods=['POST','GET'])
def add_mtle_presence():

    #recherche du matricule 
    ###### OU ######
    #recherche de la Card ID
    data = request.get_json() or {}
    print(data)
    
    if data['Matricule']:
        etudiant = Etudiant.query.filter(Etudiant.matricule==data['Matricule']).first()
    else:
        etudiant = Etudiant.query.filter(Etudiant.card_id==data['ID_card']).first()
                 
    if etudiant:
        presence = Presence(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,niveau=etudiant.niveau,date_badge=data["Date"],date=data["Date"].split(" ")[0])
    
        url = 'https://www.app-infas.net/scolarite/api/presence'
        myobj = {'matricule': etudiant.matricule}

        x = requests.post(url, json = myobj)

        print(x.text)
        db.session.add(presence)
        db.session.commit()

        return jsonify({"Message":"Vous êtes présent !!","statut":"Succes"})
    return jsonify({"Message":"Cette carte n'est pas valide","statut":"Echoue"})
    

#Create presence
@api.route('/upload_file',methods=['POST','GET'])
def add_file_presence():
    uploaded_file = request.files['file']
    image=file_upload('POST',request,'file','one')
    if image:
        with open(current_app.config['UPLOADS_DIR']+image, newline='') as csvfile:
            csv.delimiter = ';'
            # stream = io.StringIO(csvfile.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                if row['Matricule']:
                    etudiant = Etudiant.query.filter(Etudiant.matricule==row['Matricule']).first()
                else:
                    etudiant = Etudiant.query.filter(Etudiant.card_id==row['ID_card']).first()
                    
                if etudiant:
                    presence = Presence(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,niveau=etudiant.niveau,date_badge=row["Date"],date=row["Date"].split(" ")[0])
                    try:
                        db.session.add(presence)
                        db.session.commit()
                    except IntegrityError as error:
                        db.session.rollback()
                            # pass
            # os.remove(current_app.config['UPLOADS_DIR']+fi)
    else:
        url = ""

    return jsonify({"Message":"Vous êtes présent !!"})



#Create presence
@api.route('/upload_controle_file',methods=['POST','GET'])
def upload_controle_file():
    uploaded_file = request.files['file']
    image=file_upload('POST',request,'file','one')
    if image:
        with open(current_app.config['UPLOADS_DIR']+image, newline='') as csvfile:
            csv.delimiter = ';'
            # stream = io.StringIO(csvfile.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                if row['Matricule']:
                    
                    etudiant = EtudiantControle.query.filter_by(matricule=row['Matricule']).first()
   
                    if etudiant:
                        etudiant.etat = True
                        db.session.add(etudiant)
                        db.session.commit()
                        
                        return jsonify({'message' : 'success'})
                    else :
                        return jsonify({'message' : 'Matricule non valide'}), 404
                    
                            # pass
            # os.remove(current_app.config['UPLOADS_DIR']+fi)
    else:
        return jsonify({"Message":"Erreur aucun fichier reçu !!"})


    return jsonify({"Message":"Vous êtes présent !!"})


#Create presence
@api.route('/upload_stage_file',methods=['POST','GET'])
def upload_stage_file():
    uploaded_file = request.files['file']
    image=file_upload('POST',request,'file','one')
    if image:
        with open(current_app.config['UPLOADS_DIR']+image, newline='') as csvfile:
            csv.delimiter = ';'
            # stream = io.StringIO(csvfile.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                if row['Matricule']:
                    etudiant = Etudiant.query.filter(Etudiant.matricule==row['Matricule']).first()
                else:
                    etudiant = Etudiant.query.filter(Etudiant.card_id==row['ID_card']).first()
                    
                if etudiant:
                    presence = PresenceStage(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,niveau=etudiant.niveau,date_badge=row["Date"],date=row["Date"].split(" ")[0])
                    try:
                        db.session.add(presence)
                        db.session.commit()
                    except IntegrityError as error:
                        db.session.rollback()

                    return jsonify({"Message":"Vous êtes présent !!"})
                return jsonify({"Message":"Une erreur s'est produite!!"})
                    
                            # pass
            # os.remove(current_app.config['UPLOADS_DIR']+fi)
    else:
        return jsonify({"Message":"Erreur aucun fichier reçu !!"})


    return jsonify({"Message":"Vous êtes présent !!"})

