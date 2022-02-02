from datetime import datetime
from flask import render_template,session, redirect, url_for,flash,make_response,request, g, jsonify
from . import main
from ..utilities import *
from .forms import *
from flask_login import login_user,login_required,logout_user,current_user
from ..models.models import *
from ..notifications import *
import datetime
import json
from ..decorators import *
import csv
import io
from sqlalchemy.exc import IntegrityError

@main.route('/', methods=['POST','GET'])
@login_required
def home():

   #print(request.host)
   if current_user.is_authenticated:
      return redirect(url_for('main.presence'))

   else:
      return redirect(url_for('auth.login'))


### CRUD Off presence ###
@main.route('/presence', methods=['POST','GET'])
def presence():
   filieres = Filiere.query.all()
   annee_academics = AnneeAcademic.query.all()
   form = RechercheForm()
   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   print(form.antenne.choices)

   if current_user.is_antenne_administrator():
      form.antenne.choices = [current_user.antenne]
      print(form.antenne.choices)
   else:
      form.antenne.choices = ['ABIDJAN','ABENGOUROU','ABOISSO','BOUAKE','DALOA','KORHOGO']

   presences =[]
   print(form.validate_on_submit())

   fm = None
   if form.validate_on_submit():

      

      sql = """SELECT etd.nom,etd.prenoms,etd.antenne,etd.denomination,etd.niveau,etd.groupe,pr_etd.date_badge FROM 
      (SELECT et.*,fi.denomination
      FROM etudiants AS et,filieres AS fi WHERE fi.id={fi} AND fi.id=et.filiere_id AND et.groupe='{gp}') as etd
      LEFT JOIN (SELECT pr.* FROM presences AS pr
      WHERE 
      pr.filiere_id={fi} AND 
      pr.niveau='{ni}' AND 
      pr.date_badge >='{d_b} 00:00:00' and pr.date_badge<='{d_b} 23:59:00'  ) AS pr_etd 
      ON pr_etd.etudiant_id=etd.id
      WHERE 
      etd.niveau='{ni}' 
      AND
      etd.antenne='{ant}'
      
      """.format(ni="{}".format(form.niveau.data),d_b="{}".format(form.date.data),fi=form.filiere.data,gp=form.groupe.data,ant=form.antenne.data)
      print(sql)
      presences = db.engine.execute(sql)
      fi = Filiere.query.get(form.filiere.data)
      fm = form
      fm.filiere.data = fi.denomination

   return render_template('presence.html',presences=[item for item in presences],form=form, fm=fm)

@main.route('/create_presence', methods=['POST','GET'])
def create_presence():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/read_presence/<fid>', methods=['POST','GET'])
def read_presence(fid):
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/update_presence', methods=['POST','GET'])
def update_presence():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/delete_presence', methods=['POST','GET'])
def delete_presence():
   return render_template('admin_index.html',data=data,val=json.dumps(val))
### CRUD Off presence ###

### CRUD Off etudiant ###
@main.route('/etudiant', methods=['POST','GET'])
def etudiant():
   etudiants = db.engine.execute("select etudiants.*,filieres.denomination AS filiere  FROM etudiants,filieres WHERE filieres.id=etudiants.filiere_id")
   
   # etudiants = Etudiant.query.all()
   filieres = Filiere.query.all()

   form = EtudiantForm(request.form)
   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   # etudiants = [item for item in etudiants]
   # print(etudiants)
   return render_template('etudiant.html',etudiants=etudiants,form=form)


@main.route('/create_etudiant', methods=['POST','GET'])
def create_etudiant():
   form = EtudiantForm(request.form)
   
   if len(request.files):
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
         fieldnames = ['Matricule','Nom','Prenoms','Date de naissance','Filiere','Antenne','Niveau','ID Carte']
         csv.delimiter = ';'
         stream = io.StringIO(uploaded_file.stream.read().decode("ISO-8859-1"), newline=None)
         reader = csv.DictReader(stream)
         erreur = "Des erreurs sont survenues !\n"
         msg = ""
         for row in reader:
            print(row)
            try:
               filiere = Filiere.query.filter_by(denomination=row['Filiere']).first()
               etudiant = Etudiant(matricule=row['Matricule'],nom=row['Nom'],prenoms=row['Prenoms'],filiere_id=filiere.id,niveau=row['Niveau'],date_naissance=row['Date de naissance'],card_id=row['ID Carte'],antenne=row['Antenne'],groupe=row['Groupe'])
               db.session.add(etudiant)
               db.session.commit()
            except IntegrityError as error:
               db.session.rollback()
               msg="{},{},{},{},{},{},{},{}\n".format(row['Matricule'],row['Nom'],row['Prenoms'],row['Filiere'],row['Niveau'],row['Date de naissance'],row['ID Carte'],row['Antenne'],row['Groupe'])
         
         if msg!="":   
            flash("{} <br>{}".format(erreur,msg))

   else:
      print(form.data,form.id.data,form.validate_on_submit())
      if form.submit.data:
         print(form.data)

         if form.id.data:
            print(form.data)

            filiere = Filiere.query.filter_by(id=form.filiere.data).first()
            etudiant = Etudiant.query.filter_by(id=form.id.data).first()
            etudiant.matricule = form.matricule.data
            etudiant.nom = form.nom.data
            etudiant.prenoms = form.prenoms.data
            etudiant.filiere_id = filiere.id
            etudiant.niveau = form.niveau.data
            etudiant.card_id = form.id_carte.data
            etudiant.antenne = form.antenne.data
            etudiant.groupe = form.groupe.data

            db.session.add(etudiant)
            db.session.commit()
         else:
            filiere = Filiere.query.filter_by(id=form.filiere.data).first()
            etudiant = Etudiant(matricule=form.matricule.data,nom=form.nom.data,prenoms=form.prenoms.data,filiere_id=filiere.id,niveau=form.niveau.data,date_naissance=form.date_naissance.data,card_id=form.id_carte.data,antenne=form.antenne.data,groupe=form.groupe.data)
            db.session.add(etudiant)
            db.session.commit()

   etudiants = db.engine.execute("select etudiants.*,filieres.id,filieres.denomination AS filiere  FROM etudiants,filieres WHERE filieres.id=etudiants.filiere_id")
   
   # etudiants = Etudiant.query.all()
   filieres = Filiere.query.all()

   form = EtudiantForm(request.form)
   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   
   return render_template('etudiant.html',etudiants=etudiants,form=form)


@main.route('/read_etudiant/<eid>', methods=['POST','GET'])
def read_etudiant(eid):
   etudiant = Etudiant.query.filter_by(id=eid).first()

   return jsonify(etudiant.to_json())

@main.route('/update_etudiant', methods=['POST','GET'])
def update_etudiant():
   if len(request.files):

      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
         fieldnames = ['Matricule','Niveau']
         csv.delimiter = ';'
         stream = io.StringIO(uploaded_file.stream.read().decode("ISO-8859-1"), newline=None)
         reader = csv.DictReader(stream)
         erreur = "Des erreurs sont survenues !\n"
         msg=""
         for row in reader:
            print(row)
            try:
               etudiant = Etudiant.query.filter_by(matricule=row['Matricule'].strip()).first()
               if etudiant:
                  etudiant.matricule=row['Matricule']
                  etudiant.niveau=row['Niveau']
                  etudiant.antenne=row['Antenne']
                  etudiant.groupe=row['Groupe']
                  db.session.add(etudiant)
                  db.session.commit()
               else:
                  msg+="{},{}\n".format(row['Matricule'],row['Niveau'])

            except IntegrityError as error:
               db.session.rollback()
               msg+="{},{}\n".format(row['Matricule'],row['Niveau'])
         if msg!="":   
            flash("{} {}".format(erreur,msg))

   etudiants = db.engine.execute("select etudiants.*,filieres.denomination AS filiere  FROM etudiants,filieres WHERE filieres.id=etudiants.filiere_id")
   
   # etudiants = Etudiant.query.all()
   filieres = Filiere.query.all()

   form = EtudiantForm(request.form)
   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   
   return render_template('etudiant.html',etudiants=etudiants,form=form)

@main.route('/delete_etudiant/<eid>', methods=['POST','GET'])
def delete_etudiant(eid):
   etudiant = Etudiant.query.filter_by(id=eid).first()
   db.session.delete(etudiant)
   return jsonify({'result':"etudiant supprimé !"})
### CRUD Off etudiant ###


### CRUD Off filiere ###
@main.route('/filiereMatiere', methods=['POST','GET'])
def filiereMatiere():
   filieres = Filiere.query.all()
   matieres = Matiere.query.all()
   fil_form = FiliereForm(request.form)
   mat_form = MatiereForm(request.form)

   return render_template('filiereMatiere.html',filieres=filieres,matieres=matieres,fil_form=fil_form,mat_form=mat_form)

@main.route('/create_filiere', methods=['POST','GET'])
def create_filiere():
   fil_form = FiliereForm(request.form)
   mat_form = MatiereForm(request.form)
   msg=""
   if len(request.files):
      uploaded_file = request.files['file']
      print("f")
      if uploaded_file.filename != '':
         fieldnames = ['Denomination']
         csv.delimiter = ','
         stream = io.StringIO(uploaded_file.stream.read().decode("ISO-8859-1"), newline=None)
         reader = csv.DictReader(stream)
         erreur = "Des erreurs sont survenues !\n"
         
         for row in reader:
            try:
               filiere = Filiere(denomination=row['Denomination'])
               db.session.add(filiere)
               db.session.commit()
            except IntegrityError as error:
               msg="{}\n".format(row['Denomination'])
         if msg!="":
            flash("{} {}".format(erreur,msg))
         
         
   else: 
      if fil_form.id.data:
         filiere = Filiere.query.filter_by(id=fil_form.id.data).first()
         filiere.denomination = fil_form.denomination.data
         db.session.add(filiere)
         db.session.commit()
      elif fil_form.denomination.data:
         filiere = Filiere(denomination=fil_form.denomination.data) 
         db.session.add(filiere)
         db.session.commit()


   filieres = Filiere.query.all()
   matieres = Matiere.query.all()

   return render_template('filiereMatiere.html',filieres=filieres,matieres=matieres,fil_form=fil_form,mat_form=mat_form)

@main.route('/read_filiere/<fid>', methods=['POST','GET'])
def read_filiere(fid):
   filiere = Filiere.query.filter_by(id=fid).first()
   return jsonify(filiere.to_json())

@main.route('/update_filiere', methods=['POST','GET'])
def update_filiere():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/delete_filiere/<fid>', methods=['POST','GET'])
def delete_filiere(fid):
   filiere = Filiere.query.filter_by(id=fid).first()
   db.session.delete(filiere)
   return jsonify({'result':"filiere supprimé !"})

### CRUD Off filiere ###



### CRUD Off matiere ###
@main.route('/matiere', methods=['POST','GET'])
def matiere():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/create_matiere', methods=['POST','GET'])
def create_matiere():
   fil_form = FiliereForm(request.form)
   mat_form = MatiereForm(request.form)

  # print(request.files)
   if len(request.files):
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
         fieldnames = ['Denomination']
         csv.delimiter = ','
         stream = io.StringIO(uploaded_file.stream.read().decode("ISO-8859-1"), newline=None)
         reader = csv.DictReader(stream)
         erreur = "Des erreurs sont survenues !\n"
         
         for row in reader:
            try:
               matiere = Matiere(denomination=row['Denomination'])
               db.session.add(matiere)
               db.session.commit()
            except IntegrityError as error:
               erreur.append(row)
               msg="{}\n".format(row['Denomination'])
         flash("{} {}".format(erreur,msg))
         
         
   else: 
      if mat_form.id.data:
         matiere = Matiere.query.filter_by(id=mat_form.id.data).first()
         matiere.denomination = mat_form.denomination.data
         db.session.add(matiere)
         db.session.commit()
      elif mat_form.denomination.data:
         matiere = Matiere(denomination=mat_form.denomination.data)
         db.session.add(matiere)
         db.session.commit()


   filieres = Filiere.query.all()
   matieres = Matiere.query.all()

   return render_template('filiereMatiere.html',filieres=filieres,matieres=matieres,fil_form=fil_form,mat_form=mat_form)

@main.route('/read_matiere/<fid>', methods=['POST','GET'])
def read_matiere(fid):
   matiere = Matiere.query.filter_by(id=fid).first()
   return jsonify(matiere.to_json())

@main.route('/update_matiere/<mid>', methods=['POST','GET'])
def update_matiere(mid):
   form = MatiereForm(request.form)
   data = Matiere.query.filter_by(id=mid).first()

   if form.validate_on_submit():      
      data.denomination = form.denomination.data.upper()
      data.position = form.position.data.upper()

      db.session.add(data)
      db.session.commit()

   matieres = Matiere.query.all()

   return render_template('filiereMatiere.html',data=matieres)

@main.route('/delete_matiere/<mid>', methods=['POST','GET'])
def delete_matiere(mid):
   data = Matiere.query.filter_by(id=mid).first()
   db.session.delete(data)
   return jsonify({ 'result': 'Delete OK' })

### CRUD Off matiere ###

### CRUD Off device ###
@main.route('/device', methods=['POST','GET'])
def device():
   devices = Device.query.all()
   form = EquipementForm(request.form)

   return render_template('equipements.html',devices=devices,form=form)


@main.route('/create_device', methods=['POST','GET'])
def create_device():

   form = EquipementForm(request.form)

   if form.validate_on_submit():
      if form.id.data:
         device = Device.query.filter_by(id=form.id.data).first()
         device.denomination = form.denomination.data.upper()
         device.position = form.position.data.upper()
         device.emei=form.emei.data.upper()
         device.status=form.status.data.upper()
         db.session.add(device)
         db.session.commit()
      else:
         device = Device(denomination=form.denomination.data.upper(),position=form.position.data.upper(),emei=form.emei.data.upper(),status=form.status.data.upper())
         db.session.add(device)
         db.session.commit()

   devices = Device.query.all()
   
   return render_template('equipements.html',devices=devices,form=form)

@main.route('/read_device/<fid>', methods=['POST','GET'])
def read_device(fid):
   data = Device.query.filter_by(id=fid).first()
   return jsonify(data.to_json())

@main.route('/update_device/<did>', methods=['POST','GET'])
def update_device(did):
   data = Device.query.filter_by(id=did).first()
   form = EquipementForm(request.form)

   if form.validate_on_submit():
      data.denomination = form.denomination.data.upper()
      data.position = form.position.data.upper()
      data.emei=form.emei.data.upper()
      data.status=form.status.data.upper()
      
   data = Device.query.all()
   return render_template('equipements.html',data=data)

@main.route('/delete_device/<did>', methods=['POST','GET'])
def delete_device(did):
   device = Device.query.filter_by(id=did).first()
   db.session.delete(device)

   return jsonify({ 'result': 'Delete OK' })


@main.route('/init', methods=['POST','GET'])
def init():
   db.engine.execute("DELETE FROM presences")
   db.engine.execute("DELETE FROM etudiants where niveau='LICENCE 3'")

   return jsonify({ 'result': 'Delete OK' })

### CRUD Off device ###

@main.route('/profil', methods=['POST','GET'])
@login_required
def profil():
   user = User.query.filter_by(id=current_user.id).first()
   profil = ProfileForm(request.form)
   securiteForm = SecuriteForm(request.form)

   #print(profil.validate_on_submit(),profil.data)
   if profil.validate_on_submit():
      user.name=profil.name.data
      user.email=profil.mail.data

      db.session.add(user)
      db.session.commit()

   if securiteForm.validate_on_submit():
      if securiteForm.password.data == securiteForm.confirmPassword.data:
         user.password=securiteForm.password.data

   return render_template('profil.html',formP=profil,user=user,securiteForm=securiteForm)
