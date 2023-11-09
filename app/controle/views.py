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
   antennes = ['ABIDJAN','BOUAKE','ABOISSO','KORHOGO',"ABENGOUROU","DALOA"]
   # groupes = ['Groupe A','Groupe B','Groupe C','Groupe D',"Groupe E","Groupe F","Groupe G","Groupe H","Groupe I","Groupe J","Groupe K"]
   niveau = ['Licence 1','Licence 2','Licence 3']
   etudiants = []
   etudiants_present= []
   info=[]
   if request.method == 'POST':
      filiere = Filiere.query.get(request.form['filiere'])
      print(request.form)
      info = [request.form['antenne'],filiere.denomination,request.form['niveau']]
      etudiants = EtudiantControle.query.filter_by(filiere_id=request.form['filiere']).filter_by(antenne=request.form['antenne']).filter_by(niveau=request.form['niveau']).all()
      etudiants_present = EtudiantControle.query.filter_by(filiere_id=request.form['filiere']).filter_by(antenne=request.form['antenne'],etat=True).filter_by(niveau=request.form['niveau']).all()
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
      
   return render_template('etudiant_controle.html',filieres=form_filieres, antennes=antennes,niveau=niveau, info=info, presents=etudiants_present,etudiants=[item.to_json() for item in etudiants])

@controle.route('/controle/<matricule>', methods=['POST','GET'])
def etudiant_resultat_controle(matricule):
   uploads_dir = current_app.config['UPLOADS_DIR']
   filieres = Filiere.query.all()
   form_filieres = [(item.id, item.denomination) for item in filieres]
   antennes = ['ABIDJAN','BOUAKE','ABOISSO','KORHOGO',"ABENGOUROU","DALOA"]
   groupes = ['Groupe A','Groupe B','Groupe C','Groupe D',"Groupe E","Groupe F","Groupe G","Groupe H","Groupe I","Groupe J","Groupe K"]
   niveau = ['Licence 1','Licence 2','Licence 3']
   etudiant = EtudiantControle.query.filter_by(matricule=matricule).first()


   if request.method == 'POST':
      et = EtudiantControle.query.filter_by(matricule=matricule).first()
      print(et.id)
      if request.files['image']:
            data = request.files['image']
            filename = secure_filename(data.filename)
            if not exists(os.path.join(uploads_dir, filename)):
               data.save(os.path.join(uploads_dir, filename))
            et.photo = filename

      
      et.nom = request.form['nom']
      et.card_id = request.form['card_id']
      et.prenoms = request.form['prenoms']
      et.niveau = request.form['niveau']
      et.antenne = request.form['antenne']
      et.filiere_id = request.form['filiere']
      et.groupe = request.form['groupe']
      et.date_naissance = request.form['date_naissance_edit']
      db.session.add(et)
      db.session.commit()
      
      return redirect(url_for('controle.etudiant_controle', matricule=matricule))
   
   return render_template('etudiant_result_controle.html', etudiant=etudiant.to_json(),filieres=form_filieres, niveau=niveau, groupes=groupes,antennes=antennes)


@controle.route('/controle/etat/<matricule>', methods=['POST','GET'])
def setEtat(matricule):
   
   etudiant = EtudiantControle.query.filter_by(matricule=matricule).first()
   
   if etudiant:
      etudiant.etat = True
      db.session.add(etudiant)
      db.session.commit()
      
      return jsonify({'message' : 'success'})
   else :
      return jsonify({'message' : 'Matricule non valide'}), 404
   
   


@controle.route('/control/generate/qrcode', methods=['POST'])
def qrcode_generate():
  
   etudiant = EtudiantControle.query.filter_by(matricule=request.args.get('matricule')).first()

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
      etudiant = EtudiantControle(matricule=form.matricule.data,nom=form.nom.data,prenoms=form.prenoms.data,filiere_id=form.filiere.data,niveau=form.niveau.data,date_naissance=datetime.strftime(form.date_naissance.data, '%d/%m/%Y'),card_id=form.id_carte.data,antenne=form.antenne.data,groupe=form.groupe.data, photo=filename, qrcode=qrcode)
      db.session.add(etudiant)
      db.session.commit()

      return redirect(url_for('controle.etudiant_controle'))

      
   return render_template('controle_new.html',form=form)


@controle.route('/controle/rapport', methods=['POST','GET'])
def rapport():
   
   form = RechercheForm()
  
   print(form.antenne.choices)

   form.antenne.choices = ['ABIDJAN','ABENGOUROU','ABOISSO','BOUAKE','DALOA','KORHOGO']
 
   print(form.validate_on_submit())
   presences  = []
   if request.method== 'POST':
      # if not form.date_debut.data:
      #    flash('Veuillez chosir une date svp')
      #    return redirect(url_for('controle.rapport'))
   
      sql = f"""SELECT 
	public.filieres.denomination, 
	public.etudiants_cotrole.niveau, 
	nb_group.antenne,
	count(public.etudiants_cotrole.id), 
	nb_group.nombre
FROM 
	public.filieres,
	public.etudiants_cotrole,
	(SELECT count(public.etudiants_cotrole.id) as nombre,public.etudiants_cotrole.filiere_id, 
		public.etudiants_cotrole.niveau, 
		public.etudiants_cotrole.antenne  
	from 
	 	public.etudiants_cotrole, 
	 	public.filieres 
	where 
	 	public.etudiants_cotrole.filiere_id =public.filieres.id 
	 and 
	 	public.etudiants_cotrole.antenne  = '{form.antenne.data}'
	and
	 	public.etudiants_cotrole.etat='true'
	 group by 
	 	public.etudiants_cotrole.filiere_id, 
	 	public.etudiants_cotrole.niveau, 
	 	public.etudiants_cotrole.antenne
	) 
as 
	nb_group
where  
	public.filieres.id= public.etudiants_cotrole.filiere_id 

and 
	public.etudiants_cotrole.filiere_id = nb_group.filiere_id 
and 
	public.etudiants_cotrole.niveau = nb_group.niveau
group by  
	public.filieres.denomination, 
	public.etudiants_cotrole.niveau, 
	public.filieres.id, 
	nb_group.nombre, 
	nb_group.antenne 
order by 
	public.filieres.denomination, 
	public.etudiants_cotrole.niveau asc
      
      """
      
      
      print(sql)
      presences = db.engine.execute(sql)
      
      print(presences)

   return render_template('rapport_controle.html',presences=[item for item in presences],form=form)




@controle.route('/etudiant/add', methods=['POST','GET'])
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
      
   qrcode = generate_qr(form['matricule'])
   try:
      etudiant = EtudiantControle(matricule=form['matricule'],nom=form['nom'],prenoms=form['prenoms'],filiere_id=form['filiere'],niveau=form['niveau'],date_naissance=form['date_naissance'],statut=form['statut'],antenne=form['antenne'],photo=form['photo'])
      db.session.add(etudiant)
      db.session.commit()
   except:
      db.session.rollback()
      print("error")

   return jsonify(etudiant.to_json())


   