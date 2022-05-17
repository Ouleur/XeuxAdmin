from genericpath import exists
from flask import render_template,session, redirect, url_for,flash,make_response,request, g, jsonify
from sqlalchemy import false
from . import controle
from ..utilities import *
from .form import *
from ..models.models import *
from ..notifications import *
from datetime import date
import json
from ..decorators import *
from sqlalchemy.exc import IntegrityError


@controle.route('/controle', methods=['POST','GET'])
def etudiant_controle():
   datas = {}
   datas['data'] = []
   filieres = Filiere.query.all()
   form_filieres = [(item.id, item.denomination) for item in filieres]
   antennes = ['ABIDJAN','BOUAKE','ABOISSO','KORHOGO',"ABENGOUROU"]
   # groupes = ['Groupe A','Groupe B','Groupe C','Groupe D',"Groupe E","Groupe F","Groupe G","Groupe H","Groupe I","Groupe J","Groupe K"]
   niveau = ['Licence 1','Licence 2','Licence 3']
   etudiants = []
   if request.method == 'POST':
   
      etudiants = Etudiant.query.filter_by(filiere_id=request.form['filiere']).filter_by(antenne=request.form['antenne']).filter_by(niveau=request.form['niveau']).all()
      # etudiants_data = [item.to_json() for item in etudiants]
      # for etudiant in etudiants:
      #    filiere = Filiere.query.filter_by(id=etudiant.filiere_id).first()
      #    datas['data'].append(
      #       [
      #       etudiant.matricule,
      #       etudiant.nom,
      #       etudiant.prenoms,
      #       etudiant.antenne,
      #       filiere.denomination,
      #       etudiant.niveau,
      #       etudiant.groupe,
      #       '<td class="pst">PRESENT(E)</td>' if etudiant.etat else '<td class="abs">ABSENT(E)</td>',
      #       ]
      #    )
      # return jsonify(datas)
   return render_template('etudiant_controle.html',filieres=form_filieres, antennes=antennes,niveau=niveau, etudiants=[item.to_json() for item in etudiants])

@controle.route('/controle/<matricule>', methods=['POST','GET'])
def etudiant_resultat_controle(matricule):
   uploads_dir = current_app.config['UPLOADS_DIR']
   filieres = Filiere.query.all()
   form_filieres = [(item.id, item.denomination) for item in filieres]
   antennes = ['ABIDJAN','BOUAKE','ABOISSO','KORHOGO',"ABENGOUROU"]
   groupes = ['Groupe A','Groupe B','Groupe C','Groupe D',"Groupe E","Groupe F","Groupe G","Groupe H","Groupe I","Groupe J","Groupe K"]
   niveau = ['Licence 1','Licence 2','Licence 3']
   etudiant = Etudiant.query.filter_by(matricule=matricule).first()
   
   if request.method == 'POST':
      et = Etudiant.query.filter_by(matricule=matricule).first()
      print(et.id)
      if request.files['image']:
            data = request.files['image']
            filename = secure_filename(data.filename)
            if not exists(os.path.join(uploads_dir, filename)):
               data.save(os.path.join(uploads_dir, filename))
            et.photo = filename

      et.nom = request.form['nom']
      et.card_id = request.form['card_id']
      et.prenom = request.form['prenoms']
      et.niveau = request.form['niveau']
      et.antenne = request.form['antenne']
      et.filiere_id = request.form['filiere']
      et.groupe = request.form['groupe']
      et.date_naissance = request.form['date_naissance_edit']
      db.session.add(et)
      db.session.commit()
      
      return redirect(url_for('controle.etudiant_resultat_controle', matricule=matricule))
   
   return render_template('etudiant_result_controle.html', etudiant=etudiant.to_json(), filieres=form_filieres, niveau=niveau, groupes=groupes,antennes=antennes)


@controle.route('/controle/etat/<matricule>', methods=['POST','GET'])
def setEtat(matricule):
   
   etudiant = Etudiant.query.filter_by(matricule=matricule).first()
   
   if etudiant:
      etudiant.etat = 1
      db.session.add(etudiant)
      db.session.commit()
      
      return jsonify({'message' : 'success'})
   else :
      return jsonify({'message' : 'Matricule non valide'}), 404
   
   


@controle.route('/control/generate/qrcode', methods=['POST'])
def qrcode_generate():
  
   etudiant = Etudiant.query.filter_by(matricule=request.args.get('matricule')).first()

   qrcode = generate_qr(etudiant.matricule)
   etudiant.qrcode = qrcode
   db.session.add(etudiant)
   db.session.commit()
   
   return redirect(url_for('controle.etudiant_resultat_controle', matricule=request.args.get('matricule')))


@controle.route('/controle/etudiant/new', methods=['POST','GET'])
def controle_new():
   uploads_dir = current_app.config['UPLOADS_DIR']
   filieres = Filiere.query.all()
   form = EtudiantForm(request.form)
   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   if form.is_submitted() :
      filename = None
      if request.files['image']:
         data = request.files['image']
         filename = secure_filename(data.filename)
         if not exists(os.path.join(uploads_dir, filename)):
            data.save(os.path.join(uploads_dir, filename))
      
      qrcode = generate_qr(form.matricule.data)
      etudiant = Etudiant(matricule=form.matricule.data,nom=form.nom.data,prenoms=form.prenoms.data,filiere_id=form.filiere.data,niveau=form.niveau.data,date_naissance=datetime.strftime(form.date_naissance.data, '%d/%m/%Y'),card_id=form.id_carte.data,antenne=form.antenne.data,groupe=form.groupe.data, photo=filename, qrcode=qrcode)
      db.session.add(etudiant)
      db.session.commit()

      return redirect(url_for('controle.etudiant_controle'))

      
   return render_template('controle_new.html',form=form)