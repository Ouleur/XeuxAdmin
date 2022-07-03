from genericpath import exists
from flask import render_template,session, redirect, url_for,flash,make_response,request, g, jsonify
from sqlalchemy import false
from . import etudiant
from ..utilities import *
from .form import *
from ..models.models import *
from ..notifications import *
from datetime import date
import json
from ..decorators import *
from sqlalchemy.exc import IntegrityError




@etudiant.route('/etudiant/infos', methods=['POST','GET'])
def etudiant_infos():
   form = EtudiantForm(request.form)
   
   if request.method == 'POST':
   
      etudiant = EtudiantVerif.query.filter_by(matricule=request.form['matricule']).first()
      if etudiant:
         print()
         if session.get('etudiant'):
            session.pop('etudiant')
         session['etudiant'] = etudiant.to_json()
         return jsonify({'message' : 'succes'}), 200
      else:
         return jsonify({'message' : 'matricule invalide'}), 404 
      
      # return redirect(url_for('etudiant.etudiant_resultat'))
   return render_template('etudiant_infos.html',form=form)

@etudiant.route('/etudiant/result', methods=['POST','GET'])
def etudiant_resultat():
   uploads_dir = current_app.config['UPLOADS_DIR']
   filieres = Filiere.query.all()
   form_filieres = [(item.id, item.denomination) for item in filieres]
   antennes = ['ABIDJAN','BOUAKE','ABOISSO','KORHOGO',"ABENGOUROU","DALOA"]
   groupes = ['Groupe A','Groupe B','Groupe C','Groupe D',"Groupe E","Groupe F","Groupe G","Groupe H","Groupe I","Groupe J","Groupe K"]
   niveau = ['Licence 1','Licence 2','Licence 3']
   etudiant = session['etudiant']
   
   if request.method == 'POST':
      et = EtudiantVerif.query.filter_by(id=etudiant['id']).first()
      print(et.id)
      if request.files['image']:
            data = request.files['image']
            filename = secure_filename(data.filename)
            if not exists(os.path.join(uploads_dir, filename)):
               data.save(os.path.join(uploads_dir, filename))
            et.photo = filename
            
      print(request.form)
      et.date_naissance = request.form['date_naissance_edit']
      et.lieu_naissance = request.form['lieu_naissance']
      db.session.add(et)
      db.session.commit()
      session.pop('etudiant')
      session['etudiant'] = et.to_json()
      print(etudiant)
      return redirect(url_for('etudiant.etudiant_resultat'))
   
   return render_template('etudiant_result.html', etudiant=etudiant, filieres=form_filieres, niveau=niveau, groupes=groupes,antennes=antennes)


@etudiant.route('/etudiant/verif/add', methods=['POST','GET'])
def etudiant_add():
   form =request.get_json() or {}
   print(form)
   form = form["root"]
   filiere = Filiere.query.filter_by(denomination=form['filiere']).first()

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
      
   qrcode = generate_qr(form['matricule'])
   try:
      etudiant = EtudiantVerif(matricule=form['matricule'],nom=form['nom'],prenoms=form['prenoms'],filiere_id=form['filiere'],niveau=form['niveau'],date_naissance=form['date_naissance'],statut=form['statut'],antenne=form['antenne'],photo=form['photo'])
      db.session.add(etudiant)
      db.session.commit()
   except:
      db.session.rollback()
      print("error")

   return jsonify(etudiant.to_json())

@etudiant.route('/generate/qrcode', methods=['POST'])
def qrcode_generate():
   et = session['etudiant']
   etudiant = EtudiantVerif.query.filter_by(id=et.get('id')).first()

   qrcode = generate_qr(etudiant.matricule)
   etudiant.qrcode = qrcode
   db.session.add(etudiant)
   db.session.commit()
   session.pop('etudiant')
   session['etudiant'] = etudiant.to_json()
   return redirect(url_for('etudiant.etudiant_resultat'))


@etudiant.route('/etudiant/new', methods=['POST','GET'])
def etudiant_new():
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
      etudiant = EtudiantVerif(matricule=form.matricule.data,nom=form.nom.data,prenoms=form.prenoms.data,filiere_id=form.filiere.data,niveau=form.niveau.data,date_naissance=datetime.strftime(form.date_naissance.data, '%d/%m/%Y'),card_id=form.id_carte.data,antenne=form.antenne.data,groupe=form.groupe.data, photo=filename, qrcode=qrcode)
      db.session.add(etudiant)
      db.session.commit()

      return redirect(url_for('etudiant.etudiant_infos'))

      
   return render_template('etudiant_new.html',form=form)

