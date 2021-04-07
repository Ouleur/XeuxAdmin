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
    arr = os.listdir('app/static/uploads')
    print(arr)
    for fi in arr:
        with open('app/static/uploads/'+fi, newline='') as csvfile:
            csv.delimiter = ';'
            # stream = io.StringIO(csvfile.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                etudiant = Etudiant.query.filter((Etudiant.matricule==row['Matricule'] )| (Etudiant.card_id==row['ID card'])).first()
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
        # os.remove('app/static/uploads/'+fi)

    #recherche du matricule 
    ###### OU ######
    #recherche de la Card ID

    
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
        url = url_for('static', filename='uploads/' + image)
    else:
        url = ""
    # if uploaded_file.filename != '':
    # #   fieldnames = ['Matricule','Nom','Prenoms','Date de naissance','Filiere','Antenne','Niveau','ID Carte']
    # #   csv.delimiter = ';'
    #   print(request.files['file'])

    #   stream = io.StringIO(uploaded_file.stream.read().decode("UTF8"), newline=None)
    #   reader = csv.DictReader(stream)
    #   print(len(reader))
    #   for row in reader:
    #      print("row")
        #  filiere = Filiere.query.filter_by(denomination=row['Filiere']).first()
        #  etudiant = Etudiant(matricule=row['Matricule'],nom=row['Nom'],prenoms=row['Prenoms'],filiere_id=filiere.id,niveau=row['Niveau'],date_naissance=row['Date de naissance'],card_id=row['ID Carte'],antenne=row['antenne'])
        #  db.session.add(etudiant)
        #  db.session.commit()
    return jsonify({"Message":"Vous êtes présent !!"})