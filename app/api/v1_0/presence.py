from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import User,Etudiant,Presence
from flask import g, jsonify
from sqlalchemy.exc import IntegrityError
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import subprocess
import csv
import io
import os
from ...utilities import *


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
                print(row)
                print(etudiant)
                if etudiant:
                    presence = Presence(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,niveau=etudiant.niveau,date_badge=row["Date"])
                    try:
                        db.session.add(presence)
                        db.session.commit()
                    except IntegrityError as error:
                        print('')
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
                    
                print(etudiant)
                if etudiant:
                    presence = Presence(etudiant_id=etudiant.id,filiere_id=etudiant.filiere_id,niveau=etudiant.niveau,date_badge=row["Date"],date=row["Date"].split(" ")[0])
                    try:
                        db.session.add(presence)
                        db.session.commit()
                    except IntegrityError as error:
                        print('')
                        db.session.rollback()
                            # pass
            # os.remove(current_app.config['UPLOADS_DIR']+fi)
    else:
        url = ""

    return jsonify({"Message":"Vous êtes présent !!"})