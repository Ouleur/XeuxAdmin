
from genericpath import exists
from flask import render_template,session, redirect, url_for,flash,make_response,request, g, jsonify
from sqlalchemy import false
from . import main
from ..utilities import *
from .forms import *
from flask_login import login_user,login_required,logout_user,current_user
from ..models.models import *
from ..notifications import *
from datetime import date
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
   month = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre","Octobre", "Novembre", "Decembre"]
   form = RechercheForm()
   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   print(form.antenne.choices)

   if current_user.antenne:
      form.antenne.choices = [current_user.antenne]
      print(form.antenne.choices)
   else:
      form.antenne.choices = ['ABIDJAN','ABENGOUROU','ABOISSO','BOUAKE','DALOA','KORHOGO']


   presences =[]
   print(form.validate_on_submit())

   fm = None
   if request.method == 'POST':
      
      presences = {}
      presences['columns'] = [
            { 'title': "Nom" },
            { 'title': "Prenoms" },
            { 'title': "Antenne" },
            { 'title': "Filière" },
            { 'title': "Niveau" },
            { 'title': "Groupe" }
      ]
      
      pres = []
      presences['data'] = []
      data = request.form
      if not data['date_debut']:
         return jsonify({'message' : "Veuillez choisir une date svp"}), 404
      date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d')
      print(date_debut.month)
      presences['columns'].append({'title' : f'{date_debut.day}-{month[int(date_debut.month)-1]}'})
      # y,m,d = str(data['date_debut']).split('-')
      if data['date_fin']:

         date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d')
         count =  date_fin - date_debut

         if count.days < 0:
            return jsonify({'message' : "La date de fin doit être supperieur à la date de debut"}), 404

         if count.days > 10:
            return jsonify({'message' : "Veuillez choisir un interval de moins de 10 jours"}), 404
         for item in range(int(count.days)):
            date_sql = date_debut + timedelta(days= int(item)+1)
               
            presences['columns'].append({'title' : f'{date_sql.day}-{month[int(date_sql.month) -1]}'})
            sql_two = """SELECT etd.nom,etd.prenoms,etd.antenne,etd.denomination,etd.niveau,etd.groupe,pr_etd.date_badge FROM 
                     (SELECT et.*,fi.denomination
                     FROM etudiants AS et,filieres AS fi WHERE fi.id={fi} AND fi.id=et.filiere_id AND et.groupe='{gp}') as etd
                     LEFT JOIN (SELECT pr.* FROM presences AS pr
                     WHERE 
                     pr.filiere_id={fi} AND 
                     pr.niveau='{ni}' AND 
                     pr.date_badge >='{d_b}' and pr.date_badge<='{d_b_fin}'   ) AS pr_etd 
                     ON pr_etd.etudiant_id=etd.id
                     WHERE 
                     etd.niveau='{ni}' 
                     AND
                     etd.antenne='{ant}'
                     ORDER BY etd.nom
                     """.format(ni="{}".format(data['niveau']),d_b=f'{date_sql}',d_b_fin=f'{datetime.strftime(date_sql, "%Y-%m-%d 23:59:00")}',fi=data['filiere'],gp=data['groupe'],ant=data['antenne'])
         
            pres.append(db.engine.execute(sql_two)) 

      

    
      
        

      



      
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
         ORDER BY etd.nom
       """.format(ni="{}".format(data['niveau']),d_b="{}".format(data['date_debut']),fi=data['filiere'],gp=data['groupe'],ant=data['antenne'])

      
      
      presences_one = db.engine.execute(sql)

      # presences.extend(presences_one)

      # presences.append(presences2)
      # presences.append(presences3)
      # fi = Filiere.query.get(form.filiere.data)
      # fm = form
      # fm.filiere.data = fi.denomination
      
   
      
  
      for presence in presences_one:
         
         presences['data'].append([
                              presence[0],
                              presence[1],
                              presence[2],
                              presence[3],
                              presence[4],
                              presence[5],
                              '<td class="pst">PRESENT(E)</td>' if presence[6] else '<td class="abs">ABSENT(E)</td>',
                              ])
      i= 0
      for item in pres:
         i=0
         for el in item:
            presences['data'][i].append("<td class='pst'>PRESENT(E)</td>" if el[6] else '<td class="abs">ABSENT(E)</td>')
            i = i+1

      return json.dumps(presences)


      

   return render_template('presence.html',presences=[item for item in presences],form=form, fm=fm)



### CRUD Off presence ###
@main.route('/presence_unique', methods=['POST','GET'])
def presence_unique():
   filieres = Filiere.query.all()
   annee_academics = AnneeAcademic.query.all()
   month = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Novembre", "Decembre"]
   form = RechercheMatriculeForm()
   


   presences =[]
   print(form.validate_on_submit())

   fm = None
   if request.method == 'POST':
      
      presences = {}
      presences['columns'] = [
            { 'title': "Nom" },
            { 'title': "Prenoms" },
            { 'title': "Antenne" },
            { 'title': "Filière" },
            { 'title': "Niveau" },
            { 'title': "Groupe" }
      ]
      pres = []
      presences['data'] = []
      da = request.form
      
      etudiant  = Etudiant.query.filter_by(matricule=da["matricule"]).first()
      print(etudiant.to_json())
      data = {}
      data['date_fin'] = da["date_fin"]
      data['niveau'] = etudiant.niveau
      data['date_debut']= da["date_debut"]
      data['matricule']= da["matricule"]
      data['filiere']= etudiant.filiere_id
      data['groupe']= etudiant.groupe
      data['antenne']= etudiant.antenne
      if not data['date_debut']:
         return jsonify({'message' : "Veuillez choisir une date svp"}), 404
      date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d')
      presences['columns'].append({'title' : f'{date_debut.day}-{month[int(date_debut.month) -1]}'})
      

      # y,m,d = str(data['date_debut']).split('-')
      if data['date_fin']:

         date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d')
         count =  date_fin - date_debut

         if count.days < 0:
            return jsonify({'message' : "La date de fin doit être supperieur à la date de debut"}), 404

         if count.days > 10:
            return jsonify({'message' : "Veuillez choisir un interval de moins de 10 jours"}), 404
         for item in range(int(count.days)):
            date_sql = date_debut + timedelta(days= int(item)+1)
               
            presences['columns'].append({'title' : f'{date_sql.day}-{month[int(date_sql.month) -1]}'})
            sql_two = """SELECT etd.nom,etd.prenoms,etd.antenne,etd.denomination,etd.niveau,etd.groupe,pr_etd.date_badge FROM 
                     (SELECT et.*,fi.denomination
                     FROM etudiants AS et,filieres AS fi WHERE fi.id={fi} AND fi.id=et.filiere_id AND et.groupe='{gp}' AND et.matricule='{mtl}') as etd
                     LEFT JOIN (SELECT pr.* FROM presences AS pr
                     WHERE 
                     pr.filiere_id={fi} AND 
                     pr.niveau='{ni}' AND 
                     pr.date_badge >='{d_b}' and pr.date_badge<='{d_b_fin}'   ) AS pr_etd 
                     ON pr_etd.etudiant_id=etd.id
                     WHERE 
                     etd.niveau='{ni}' 
                     AND
                     etd.antenne='{ant}'
                     ORDER BY etd.nom
                     """.format(ni="{}".format(data['niveau']),mtl="{}".format(data['matricule']),d_b=f'{date_sql}',d_b_fin=f'{datetime.strftime(date_sql, "%Y-%m-%d 23:59:00")}',fi=data['filiere'],gp=data['groupe'],ant=data['antenne'])
         
            pres.append(db.engine.execute(sql_two)) 


      
      sql = """SELECT etd.nom,etd.prenoms,etd.antenne,etd.denomination,etd.niveau,etd.groupe,pr_etd.date_badge FROM 
         (SELECT et.*,fi.denomination
         FROM etudiants AS et,filieres AS fi WHERE fi.id={fi} AND fi.id=et.filiere_id AND et.groupe='{gp}' AND et.matricule='{mtl}') as etd
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
         ORDER BY etd.nom
       """.format(ni="{}".format(data['niveau']),mtl="{}".format(data['matricule']),d_b="{}".format(data['date_debut']),fi=data['filiere'],gp=data['groupe'],ant=data['antenne'])

      
      
      presences_one = db.engine.execute(sql)

      # presences.extend(presences_one)

      # presences.append(presences2)
      # presences.append(presences3)
      # fi = Filiere.query.get(form.filiere.data)
      # fm = form
      # fm.filiere.data = fi.denomination
      
   
      
      for presence in presences_one.all():
         
         presences['data'].append([
                              presence[0],
                              presence[1],
                              presence[2],
                              presence[3],
                              presence[4],
                              presence[5],
                              '<td class="pst">PRESENT(E)</td>' if presence[6] else '<td class="abs">ABSENT(E)</td>',
                              ])
      i= 0
      print( presences['data'])
      for item in pres:
         i=0
         print(item)
         for el in item:
            try:
               presences['data'][i].append("<td class='pst'>PRESENT(E)</td>" if el[6] else '<td class="abs">ABSENT(E)</td>')
            except : 
               print("erreur")

            i = i+1

      return jsonify(presences)


      

   return render_template('presence_unique.html',presences=[item for item in presences],form=form, fm=fm)




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


@main.route('/rapport', methods=['POST','GET'])
def rapport():
   
   form = RechercheForm()
   if current_user.antenne:
      form.antenne.choices = [current_user.antenne]
      print(form.antenne.choices)
      antenne = current_user.antenne

   else:
      form.antenne.choices = ['ABIDJAN','ABENGOUROU','ABOISSO','BOUAKE','DALOA','KORHOGO']
      antenne = 'ABIDJAN'
   
   now = date.today()
   sql = f"""SELECT  public.filieres.denomination, public.presences.niveau,public.etudiants.groupe, public.presences.date, count(public.presences.id), nb_group.nombre, nb_group.antenne
	FROM public.presences,public.filieres,public.etudiants,   (SELECT count(public.etudiants.id) as nombre, public.etudiants.groupe,public.etudiants.filiere_id, public.etudiants.niveau, public.etudiants.antenne  from public.etudiants, public.filieres where public.etudiants.filiere_id =public.filieres.id and public.etudiants.antenne  = '{antenne}' group by public.etudiants.groupe , public.etudiants.filiere_id, public.etudiants.niveau, public.etudiants.antenne) as nb_group
	
	where public.presences.date ='{now}' and public.etudiants.antenne=nb_group.antenne and public.filieres.id= public.presences.filiere_id and public.etudiants.id=public.presences.etudiant_id and public.etudiants.groupe = nb_group.groupe and public.etudiants.filiere_id = nb_group.filiere_id and public.etudiants.niveau = nb_group.niveau
	
	group by  public.filieres.denomination, public.presences.niveau, public.etudiants.groupe, public.presences.groupe, public.presences.date, public.filieres.id, nb_group.nombre, nb_group.antenne
	
	order by public.filieres.denomination, public.presences.niveau,  public.etudiants.groupe asc;
      """

   presences = db.engine.execute(sql)
  
   print(form.antenne.choices)

   if current_user.antenne:
      form.antenne.choices = [current_user.antenne]
      print(form.antenne.choices)
   else:
      form.antenne.choices = ['ABIDJAN','ABENGOUROU','ABOISSO','BOUAKE','DALOA','KORHOGO']

 
   print(form.validate_on_submit())

   if request.method== 'POST':
      if not form.date_debut.data:
         flash('Veuillez chosir une date svp')
         return redirect(url_for('main.rapport'))
   
      sql = f"""SELECT public.filieres.denomination, public.presences.niveau,public.etudiants.groupe, public.presences.date, count(public.presences.id), nb_group.nombre, nb_group.antenne
	FROM public.presences,public.filieres,public.etudiants,   (SELECT count(public.etudiants.id) as nombre, public.etudiants.groupe,public.etudiants.filiere_id, public.etudiants.niveau, public.etudiants.antenne  from public.etudiants, public.filieres where public.etudiants.filiere_id =public.filieres.id and public.etudiants.antenne  = '{form.antenne.data}' group by public.etudiants.groupe , public.etudiants.filiere_id, public.etudiants.niveau, public.etudiants.antenne) as nb_group
	
	where public.presences.date ='{form.date_debut.data}' and public.etudiants.antenne=nb_group.antenne and public.filieres.id= public.presences.filiere_id and public.etudiants.id=public.presences.etudiant_id and public.etudiants.groupe = nb_group.groupe and public.etudiants.filiere_id = nb_group.filiere_id and public.etudiants.niveau = nb_group.niveau
	
	group by  public.filieres.denomination, public.presences.niveau, public.etudiants.groupe, public.presences.groupe, public.presences.date, public.filieres.id, nb_group.nombre, nb_group.antenne
	
	order by public.filieres.denomination, public.presences.niveau,  public.etudiants.groupe asc;
      
      """
      
      
      print(sql)
      presences = db.engine.execute(sql)
      
      print(presences)

   return render_template('rapport.html',presences=[item for item in presences],form=form)



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



@main.route('/etudiant/api')
def etudiant_api():
   data = {}
   data['data'] = []
   etudiants = db.engine.execute("select etudiants.*,filieres.denomination AS filiere  FROM etudiants,filieres WHERE filieres.id=etudiants.filiere_id")
   
   for etudiant in etudiants:
      data['data'].append([
          etudiant.matricule,
          etudiant.nom,
          etudiant.prenoms,
          etudiant.date_naissance,
          etudiant.antenne,
          etudiant.filiere,
          etudiant.niveau,
          etudiant.groupe,
          etudiant.card_id,
          f'<i class="modif fa fa-pen" onClick="ShowEtudiant({etudiant.id})"></i> | <i class="fa fa-trash" onClick="deleteEtudiant({etudiant.id})"></i></td>'
         ])
   return jsonify(data)
   


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
               print(error)
               db.session.rollback()
               msg+="{},{},{},{},{},{},{},{}\n".format(row['Matricule'],row['Nom'],row['Prenoms'],row['Filiere'],row['Niveau'],row['Date de naissance'],row['ID Carte'],row['Antenne'],row['Groupe'])
         
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
                  etudiant.matricule=row['Matricule'] if row['Matricule'] else etudiant.matricule
                  # etudiant.niveau=row['Niveau'] if row['Niveau'] else etudiant.niveau
                  # etudiant.antenne=row['Antenne'] if row['Antenne'] else etudiant.antenne
                  etudiant.groupe=row['Groupe'] if row['Groupe'] else etudiant.groupe
                  db.session.add(etudiant)
                  db.session.commit()
               else:
                  msg+="{},{},{},{},{},{},{},\n".format(row['Matricule'],row['Nom'],row['Prenoms'],row['Niveau'],row['Antenne'],row['Groupe'], row['Filiere'])
                  # msg += row

            except IntegrityError as error:
               db.session.rollback()
               msg+="{},{},{},{},{},{},{},\n".format(row['Matricule'],row['Nom'],row['Prenoms'],row['Niveau'],row['Antenne'],row['Groupe'], row['Filiere'])
               # msg += row
         if msg!="":   
            flash("{} {}".format(erreur,msg))
            return redirect(url_for('main.etudiant'))

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


@main.route('/etudiant_edit', methods=['POST','GET'])
def etudiant_edit():
   form = EtudiantForm(request.form)
   filieres = Filiere.query.all()

   form.filiere.choices = [(item.id, item.denomination) for item in filieres]

      # return redirect(url_for('etudiant.etudiant_resultat'))
   return render_template('etudiant_edit.html',form=form)

@main.route('/etudiant_edit_json', methods=['POST','GET'])
def etudiant_edit_json():
   
   etudiant = Etudiant.query.filter_by(matricule=request.form['matricule']).first()
   if etudiant:
      print()
      return jsonify({'message' : 'succes','data':etudiant.to_json()}), 200
   else:
      return jsonify({'message' : 'matricule invalide'}), 404 


@main.route('/etudiant_edit_json_update', methods=['POST','GET'])
def etudiant_edit_json_update():
   form = EtudiantForm(request.form)
   filieres = Filiere.query.all()

   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   if form.matricule.data:
      etudiant = Etudiant.query.filter_by(matricule=form.matricule.data).first()
      if etudiant:
         etudiant.nom = form.nom.data
         etudiant.prenoms = form.prenoms.data
         etudiant.id_carte = form.id_carte.data
         etudiant.antenne = form.antenne.data
         etudiant.niveau = form.niveau.data
         etudiant.filiere = form.filiere.data
         etudiant.groupe = form.groupe.data
         db.session.commit()
         
   return render_template('etudiant_edit.html',form=form)
      

      # return redirect(url_for('etudiant.etudiant_resultat'))
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