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

@main.route('/', methods=['POST','GET'])
@login_required
def home():

   #print(request.host)
   if current_user.is_authenticated:
      if not current_user.can(Permission.SUP_ADMINISTER):
         data = {
            # "agences":Agence.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
            # "services":Service.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
            # "guichets":Guichet.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
            # "tickets":Ticket.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
         }

         val = [5000, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000]
         return render_template('index.html',data=data,val=json.dumps(val))
      else:
         data = {
            # "entreprises":Entreprise.query.count(),
            # "agences":Agence.query.count(),
            # "services":Service.query.count(),
            # "guichets":Guichet.query.count(),
            # "tickets":Ticket.query.count(),
         }

         val = [5000, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000]
         return render_template('admin_index.html',data=data,val=json.dumps(val))

   else:
      return redirect(url_for('auth.login'))


### CRUD Off presence ###
@main.route('/presence', methods=['POST','GET'])
def presence():
   filieres = Filiere.query.all()
   annee_academics = AnneeAcademic.query.all()
   form = RechercheForm()
   form.filiere.choices = [(item.id, item.denomination) for item in filieres]
   form.annee.choices = [(item.id, item.denomination) for item in annee_academics]
   presences =[]
   print(form.validate_on_submit())
   if form.validate_on_submit():

      sql = """SELECT etd.nom,etd.prenoms,etd.denomination,etd.niveau,pr_etd.date_badge FROM 
      (SELECT et.*,fi.denomination
      FROM etudiants AS et,filieres AS fi WHERE fi.id={fi} AND fi.id=et.filiere_id) as etd
      LEFT JOIN (SELECT pr.* FROM presences AS pr
      WHERE 
      pr.filiere_id={fi} AND 
      pr.niveau='{ni}' AND 
      pr.date_badge='{d_b}' ) AS pr_etd 
      ON pr_etd.etudiant_id=etd.id
      WHERE 
      etd.niveau='{ni}' 
      
      """.format(ni="{}".format(form.niveau.data),d_b="{} 00:00:00".format(form.date.data),aa=form.annee.data,fi=form.filiere.data)
      print(sql)
      presences = db.engine.execute(sql)

   return render_template('presence.html',presences=[item for item in presences],form=form)

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
   uploaded_file = request.files['file']
   form = EtudiantForm(request.form)
   if uploaded_file.filename != '':
      fieldnames = ['Matricule','Nom','Prenoms','Date de naissance','Filiere','Antenne','Niveau','ID Carte']
      csv.delimiter = ';'
      stream = io.StringIO(uploaded_file.stream.read().decode("UTF8"), newline=None)
      reader = csv.DictReader(stream)
      
      for row in reader:
         print(row)
         filiere = Filiere.query.filter_by(denomination=row['Filiere']).first()
         etudiant = Etudiant(matricule=row['Matricule'],nom=row['Nom'],prenoms=row['Prenoms'],filiere_id=filiere.id,niveau=row['Niveau'],date_naissance=row['Date de naissance'],card_id=row['ID Carte'],antenne=row['antenne'])
         db.session.add(etudiant)
         db.session.commit()

   etudiants = Etudiant.query.all()
   return render_template('etudiant.html',etudiants=[etudiant for etudiant in etudiants.to_json()],form=form)


@main.route('/read_etudiant/<fid>', methods=['POST','GET'])
def read_etudiant(fid):
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/update_etudiant', methods=['POST','GET'])
def update_etudiant():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/delete_etudiant', methods=['POST','GET'])
def delete_etudiant():
   return render_template('admin_index.html',data=data,val=json.dumps(val))
### CRUD Off etudiant ###


### CRUD Off filiere ###
@main.route('/filiereMatiere', methods=['POST','GET'])
def filiereMatiere():
   filieres = Filiere.query.all()
   matieres = Matiere.query.all()

   return render_template('filiereMatiere.html',filieres=filieres,matieres=matieres)

@main.route('/create_filiere', methods=['POST','GET'])
def create_filiere():
   uploaded_file = request.files['file']
   if uploaded_file.filename != '':
      fieldnames = ['Denomination']
      csv.delimiter = ','
      stream = io.StringIO(uploaded_file.stream.read().decode("UTF8"), newline=None)
      reader = csv.DictReader(stream)
      
      for row in reader:
         filiere = Filiere(denomination=row['Denomination'])
         db.session.add(filiere)
      
      db.session.commit()

   filieres = Filiere.query.all()
   matieres = Matiere.query.all()

   return render_template('filiereMatiere.html',filieres=filieres,matieres=matieres)

@main.route('/read_filiere/<fid>', methods=['POST','GET'])
def read_filiere(fid):
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/update_filiere', methods=['POST','GET'])
def update_filiere():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/delete_filiere', methods=['POST','GET'])
def delete_filiere():
   return render_template('admin_index.html',data=data,val=json.dumps(val))
### CRUD Off filiere ###



### CRUD Off matiere ###
@main.route('/matiere', methods=['POST','GET'])
def matiere():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/create_matiere', methods=['POST','GET'])
def create_matiere():
   uploaded_file = request.files['file']
   if uploaded_file.filename != '':
      fieldnames = ['Denomination']
      csv.delimiter = ','
      stream = io.StringIO(uploaded_file.stream.read().decode("UTF8"), newline=None)
      reader = csv.DictReader(stream)
      
      for row in reader:
         matiere = Matiere(denomination=row['Denomination'])
         db.session.add(matiere)
      
      db.session.commit()

   filieres = Filiere.query.all()
   matieres = Matiere.query.all()

   return render_template('filiereMatiere.html',filieres=filieres,matieres=matieres)

@main.route('/read_matiere/<fid>', methods=['POST','GET'])
def read_matiere(fid):
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/update_matiere', methods=['POST','GET'])
def update_matiere():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/delete_matiere', methods=['POST','GET'])
def delete_matiere():
   return render_template('admin_index.html',data=data,val=json.dumps(val))
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
      device = Device(denomination=form.denomination.data.upper(),position=form.position.data.upper(),emei=form.emei.data.upper(),status=form.status.data.upper())
      db.session.add(device)
      db.session.commit()

   devices = Device.query.all()
   
   return render_template('equipements.html',devices=devices,form=form)

@main.route('/read_device/<fid>', methods=['POST','GET'])
def read_device(fid):
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/update_device', methods=['POST','GET'])
def update_device():
   return render_template('admin_index.html',data=data,val=json.dumps(val))

@main.route('/delete_device/<did>', methods=['POST','GET'])
def delete_device(did):
   return render_template('admin_index.html',data=data,val=json.dumps(val))
### CRUD Off device ###






# @main.route('/agences', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def agences():
#    form = AgenceForm(request.form)
#    #print(form.data)
#    entreprise = Entreprise.query.filter_by(createe_by=current_user.id).first()

#    if entreprise.state:
#       # L'on poura ajout des agences lorsaue l'entrepris est Validée par Omarks
#       if form.validate_on_submit():
#          #print(entreprise.state)

#          image=file_upload('POST',request,'file','one')

#          if image:
#             url = url_for('static', filename='uploads/' + image)
#          else:
#             url = ""
#          agence = Agence(
#             entreprise_id=entreprise.id,
#             denomination=form.denomination.data.upper(),
#             numero=form.numero.data,
#             localisation=form.localisation.data,
#             code=get_random_alphanumeric_string(5,4),
#             ouverture=form.ouverture.data,
#             fermerture=form.fermerture.data,
#             createe_by=current_user.id,
#             logo=url,
#          )
#          db.session.add(agence)
#          db.session.commit()
#    # #print(get_random_alphanumeric_string(3,3))
#    agences = Agence.query.filter_by(createe_by=current_user.id)

#    return render_template('agences.html',form=form,agences=agences)


# @main.route('/agences/<int:aid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def update_agences(aid):
#    agence = Agence.query.filter_by(id=aid).first()
#    form = AgenceForm(request.form)
#    #print(form.data)
   
#    if form.validate_on_submit():
      
#       #print(request.files)
#       image=file_upload('POST',request,'file','one')
   
#       if image:
#          url = url_for('static', filename='uploads/' + image)
#       else:
#          url = ""
      

#       agence.denomination=form.denomination.data.upper()
#       agence.numero=form.numero.data
#       agence.localisation=form.localisation.data
#       agence.ouverture=form.ouverture.data
#       agence.fermerture=form.fermerture.data
#       agence.user_id=current_user.id
#       agence.logo=url

#       db.session.add(agence)
#       db.session.commit()
#    # #print(get_random_alphanumeric_string(3,3))
#    agences = Agence.query.filter_by(createe_by=current_user.id)

#    #print(agence,aid)
#    if agence:
#       return render_template('agences.html',form=form,agences=agences, agence_item=agence)
#    else:
#       return render_template('agences.html',form=form,agences=agences)

# @main.route('/del_agences/<int:aid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def del_agences(aid):
#    agence = Agence.query.filter_by(id=aid).first()
   
#    db.session.delete(agence)
#    # #print(get_random_alphanumeric_string(3,3))
#    agences = Agence.query.filter_by(createe_by=current_user.id)

#    return render_template('agences.html',form=form,agences=agences)


# @main.route('/guichet/<codeA>/<codeS>/<codeG>', methods=['POST','GET'])
# def guichet(codeA,codeS,codeG):
#    app = current_app._get_current_object()

#    cur_date = datetime.now()
#    agence = Agence.query.filter_by(code=codeA).first()
#    service = Service.query.filter_by(code=codeS).first()
#    guichet = Guichet.query.filter_by(code=codeG).first()
#    cur = "{} {}".format(cur_date.strftime("%Y-%m-%d"),"00:00:00")
#    #print(cur)
#    tickets = Ticket.query.filter(Ticket.date_createe>=cur ,Ticket.date_createe<=cur_date,Ticket.service_id==guichet.services_id)
#    # tickets = Ticket.query.filter(Ticket.date_createe>=cur ,Ticket.date_createe<=cur_date)
#    return render_template('guichet.html',tickets=tickets,guichet=guichet,service=service,agence=agence,mercure_url=app.config['MERCURE_URL'],web_url=app.config['WEB_URL'])

# @main.route('/next_ticket/<gid>', methods=['POST','GET'])
# def next_ticket(gid):
#    cur_date = datetime.now()
#    guichet = Guichet.query.filter_by(id=gid).first()
#    cur = "{} {}".format(cur_date.strftime("%Y-%m-%d"),"00:00:00")

#    ticket = Ticket.query.filter(Ticket.date_createe>=cur ,Ticket.date_createe<=cur_date,Ticket.etat=='nouveau',Ticket.service_id==guichet.services_id).first()
#    if ticket:
#       return jsonify({"ticket":[ticket.to_json()]})
#    return jsonify({"ticket":[]})
   

# @main.route('/call_ticket/<tid>/<gid>', methods=['POST','GET'])
# def call_ticket(tid,gid):
#    tickets = Ticket.query.filter_by(id=tid,etat='nouveau').first()
#    if tickets:
#       tickets.etat='appeler'
#       tickets.guichet_id=gid
#       db.session.add(tickets)
#       db.session.commit()

#       ticket_ecran_notification({"data":tickets.to_json(),"type":"call"},tickets.id)
#       return jsonify({"ticket":[tickets.to_json()]})

#    return jsonify({"ticket":[]})
   

# @main.route('/recall_ticket/<tid>/<gid>', methods=['POST','GET'])
# def recall_ticket(tid,gid): 
#    tickets = Ticket.query.filter_by(id=tid).first()
#    if tickets:
#       tickets.etat='appeler'
#       tickets.guichet_id=gid
#       db.session.add(tickets)
#       db.session.commit()
#       ticket_ecran_notification({"data":tickets.to_json(),"type":"recall"},tickets.id)
#       return jsonify({"ticket":[tickets.to_json()]})

#    return jsonify({"ticket":[]})


# @main.route('/transfert_ticket/<sid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def transfert_ticket(sid):
#    cur_date = datetime.now()
#    tickets = Ticket.query.filter_by(Ticket.date_createe>cur_date)
#    return render_template('guichet.html',tickets=tickets)


# @main.route('/services/<int:aid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def services(aid):
#    agence = Agence.query.filter_by(id=aid).first()
#    form = ServiceForm(request.form)
#    #print(form.data)

#    if form.validate_on_submit():
#       image=file_upload('POST',request,'file','one')
   
#       if image:
#          url = url_for('static', filename='uploads/' + image)
#       else:
#          url = ""

#       service = Service(entreprise_id=agence.entreprise_id,denomination=form.denomination.data.upper(),code=get_random_alphanumeric_string(5,4),agences_id=aid,createe_by=current_user.id,logo=url)
#       db.session.add(service)
#       db.session.commit()
   
#    services = Service.query.filter_by(agences_id=aid)

#    return render_template('services.html',form=form,services=services,agence=agence)

# @main.route('/services/<int:aid>/<int:sid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def update_services(aid,sid):
#    service_item = Service.query.filter_by(id=sid).first()

#    agence = Agence.query.filter_by(id=aid).first()
#    form = ServiceForm(request.form)
#    #print(form.data)

#    if form.validate_on_submit():
#       image=file_upload('POST',request,'file','one')
   
#       if image:
#          url = url_for('static', filename='uploads/' + image)
#       else:
#          url = ""
#       service_item.denomination=form.denomination.data.upper()
#       service_item.code=form.code.data
#       service_item.agences_id=aid
#       service_item.logo=url
      
#       db.session.add(service_item)
#       db.session.commit()
   
#    services = Service.query.filter_by(agences_id=aid)

#    return render_template('services.html',form=form,services=services,agence=agence,service_item=service_item)

# @main.route('/del_ervices/<int:aid>/<int:sid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def del_services(aid,sid):
#    service_item = Service.query.filter_by(id=sid).first()
#    agence = Agence.query.filter_by(id=aid).first()

#    db.session.delete(service_item)
   
#    form = ServiceForm(request.form)

#    services = Service.query.filter_by(agences_id=aid)

#    return render_template('services.html',form=form,services=services,agence=agence)

# @main.route('/liste_guichets/<int:aid>/<int:sid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def guichets(aid,sid):
#    app = current_app._get_current_object()

#    agence = Agence.query.filter_by(id=aid).first()
#    service = Service.query.filter_by(id=sid).first()
#    form = GuichetForm(request.form)
#    #print(form.data)

#    if form.validate_on_submit():
#       guichet = Guichet(code=form.code.data,entreprise_id=agence.entreprise_id,agences_id=aid,services_id=sid,createe_by=current_user.id)
#       db.session.add(guichet)
#       db.session.commit()
   
#    guichets = Guichet.query.filter_by(services_id=sid)

#    return render_template('liste_guichets.html',form=form,guichets=guichets,agence=agence,service=service,url=app.config['WEB_URL'])

# @main.route('/liste_guichets/<int:aid>/<int:sid>/<int:gid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def update_guichets(aid,sid,gid):
#    app = current_app._get_current_object()

#    guichet_item = Guichet.query.filter_by(id=gid).first()

#    agence = Agence.query.filter_by(id=aid).first()
#    service = Service.query.filter_by(id=sid).first()

#    form = GuichetForm(request.form)
#    #print(form.data)

#    if form.validate_on_submit():
#       guichet_item.code=form.code.data
#       guichet_item.entreprise_id=agence.entreprise_id
#       guichet_item.agences_id=aid
#       guichet_item.services_id=sid
      
#       db.session.add(guichet_item)
#       db.session.commit()
   
#    guichets = Guichet.query.filter_by(services_id=sid)

#    return render_template('liste_guichets.html',form=form,guichets=guichets,agence=agence,service=service,guichet_item=guichet_item,url=app.config['WEB_URL'])

# @main.route('/del_guichets/<int:aid>/<int:sid>/<int:gid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def del_guichets(aid,sid,gid):
#    app = current_app._get_current_object()

#    guichet_item = Guichet.query.filter_by(id=gid).first()

#    agence = Agence.query.filter_by(id=aid).first()
#    service = Service.query.filter_by(id=sid).first()

#    form = GuichetForm(request.form)
#    db.session.delete(guichet_item)
   
#    guichets = Guichet.query.filter_by(services_id=sid)

#    return render_template('liste_guichets.html',form=form,guichets=guichets,agence=agence,service=service,url=app.config['WEB_URL'])


# @main.route('/update_collaborateurs/<uid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def update_collaborateurs(uid):
#    user = User.query.filter_by(id = uid).first()
  
#    form = CollaborateurForm(request.form)
#    agences = Agence.query.filter_by(createe_by=current_user.id).order_by(Agence.denomination)
#    services = Service.query.filter_by(id=user.service_id).order_by(Service.denomination)
#    guichets = Guichet.query.filter_by(id=user.guichet_id).order_by(Guichet.code)
#    form.agence.choices = [(agence.id,agence.denomination) for agence in agences]
#    form.agence.default = user.agence_id
#    form.service.choices = [(service.id,service.denomination) for service in services]
#    form.guichet.choices = [(guichet.id,guichet.code) for guichet in guichets]

#    if form.validate_on_submit():
#       user.name=form.name.data
#       user.email=form.mail.data
#       user.entreprise_id=current_user.entreprise_id
#       user.agence_id=form.agence.data.id
#       user.service_id=form.service.data.id
#       user.guichet_id=form.guichet.data.id
#       user.password=get_random_alphanumeric_string(5,4)

#       db.session.add(user)
#       db.session.commit()

#    users = User.query.filter_by(entreprise_id=current_user.entreprise_id)
#    users = [user.to_json() for user in users]

#    return render_template('collaborateurs.html',form=form,users=users,user=user)


# @main.route('/del_collaborateurs/<uid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def del_collaborateurs(uid):
#    user = User.query.filter_by(id=uid).first()
#    db.session.delete(user)

#    form = CollaborateurForm(request.form)
#    agences = Agence.query.filter_by(createe_by=current_user.id).order_by(Agence.denomination)
#    services = Service.query.filter_by(id=user.service_id).order_by(Service.denomination)
#    guichets = Guichet.query.filter_by(id=user.guichet_id).order_by(Guichet.code)
#    form.agence.choices = [(agence.id,agence.denomination) for agence in agences]
#    form.agence.default = user.agence_id
#    form.service.choices = [(service.id,service.denomination) for service in services]
#    form.guichet.choices = [(guichet.id,guichet.code) for guichet in guichets]

#    users = User.query.filter_by(entreprise_id=current_user.entreprise_id)
#    users = [user.to_json() for user in users]

#    return render_template('collaborateurs.html',form=form,users=users,user=[])

# @main.route('/collaborateurs', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def collaborateurs():
   
#    form = CollaborateurForm(request.form)
#    agences = Agence.query.filter_by(createe_by=current_user.id).order_by(Agence.denomination)
#    services = Service.query.filter_by(createe_by=current_user.id).order_by(Service.denomination)
#    guichet = Guichet.query.filter_by(createe_by=current_user.id).order_by(Guichet.code)
#    form.agence.choices = [(agence.id,agence.denomination) for agence in agences]

#    #print(form.validate_on_submit())
#    #print(form.data)
#    if form.validate_on_submit():
#       users = User(name=form.name.data,email=form.mail.data,entreprise_id=current_user.entreprise_id,agence_id=form.agence.data.id,service_id=form.service.data.id,guichet_id=form.guichet.data.id,password=get_random_alphanumeric_string(5,4))
#       db.session.add(users)
#       db.session.commit()
      
#    users = User.query.filter_by(entreprise_id=current_user.entreprise_id)
#    users = [user.to_json() for user in users]

 
#    return render_template('collaborateurs.html',form=form,users=users,user=[])



# @main.route('/etablissement', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def etablissement():
#    user = User.query.filter_by(id=current_user.id).first()
#    profil = ProfileForm(request.form)
  
#    securiteForm = SecuriteForm(request.form)
   
#    entreprises = Entreprise.query.order_by(Entreprise.state).all()
#    etablissement = EtablissementForm(request.form)

   
#    if etablissement.validate_on_submit():
#       ets.denomination = etablissement.name.data
#       ets.localisation = etablissement.localisation.data
#       ets.numero = etablissement.numero.data
#       ets.state = etablissement.state.data
#       db.session.add(ets)
#       db.session.commit()

#    #print(entreprises)

#    return render_template('entreprise.html',formE=etablissement,user=user,entreprises=entreprises)

# @main.route('/update_etablissement/<int:eid>', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def update_etablissement(eid):
#    user = User.query.filter_by(id=current_user.id).first()
#    profil = ProfileForm(request.form)
  
#    securiteForm = SecuriteForm(request.form)
   
#    ent_item = Entreprise.query.filter_by(id=eid).first()
#    entreprises = Entreprise.query.order_by(Entreprise.state).all()
#    etablissement = EtablissementForm(request.form)

   
#    if etablissement.validate_on_submit():
#       ent_item.denomination = etablissement.name.data.upper()
#       ent_item.localisation = etablissement.localisation.data
#       ent_item.numero = etablissement.numero.data
#       if etablissement.state.data=='active':
#          ent_item.state = True
#       else:
#          ent_item.state = False


#       db.session.add(ent_item)
#       db.session.commit()

#    #print(entreprises)

#    return render_template('entreprise.html',formE=etablissement,user=user,entreprises=entreprises,ent_item=ent_item)



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


   
   # ent_item = Entreprise.query.filter_by(id=user.entreprise_id).first()

   #print(etablissement.validate_on_submit(),etablissement.data)

   # if etablissement.validate_on_submit():
   #    ent_item.denomination = etablissement.denomination.data.upper()
   #    ent_item.localisation = etablissement.localisation.data
   #    ent_item.numero = etablissement.numero.data

   #    db.session.add(ent_item)
   #    db.session.commit()


   return render_template('profil.html',formP=profil,user=user,securiteForm=securiteForm)

# @main.route('/change_service/<aid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def change_service(aid):
#    services = Service.query.filter_by(id=aid)

#    return jsonify({'services': [service.to_json() for service in services]})


# @main.route('/publicite/<aid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def publicite(aid):
#    pubForm = PubliciteForm(request.form)

#    agence = Agence.query.filter_by(id=aid).first()

#    if pubForm.validate_on_submit():
#       image=file_upload('POST',request,'file','one')
#       if image:
#          publicite = Publicite(titre=pubForm.titre.data,etat=pubForm.etat.data,url=url_for('static', filename='uploads/' + image),media_type=pubForm.media_type.data,entreprise_id=current_user.entreprise_id,agence_id=aid)
#          db.session.add(publicite)
#          db.session.commit()
         
#    publicites = Publicite.query.filter_by(agence_id=aid).all()

#    return render_template('publicite.html',form=pubForm,publicites=publicites,agence=agence)


# @main.route('/update_publicite/<aid>/<pid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def update_publicite(aid,pid):
#    pubForm = PubliciteForm(request.form)

#    agence = Agence.query.filter_by(id=aid).first()
#    publicites = Publicite.query.filter_by(agence_id=aid).all()
#    publicite_item = Publicite.query.filter_by(id=pid).first()

#    if pubForm.validate_on_submit():
#       image=file_upload('POST',request,'file','one')
#       if image:
#          publicite_item.url=url_for('static', filename='uploads/' + image)

#       publicite_item.titre=pubForm.titre.data
#       publicite_item.etat=pubForm.etat.data
#       publicite_item.media_type=pubForm.media_type.data

#    return render_template('publicite.html',form=pubForm,publicites=publicites,publicite_item=publicite_item,agence=agence)


# @main.route('/del_publicite/<aid>/<pid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def del_publicite(aid,pid):
#    agence = Agence.query.filter_by(id=aid).first()
#    publicites = Publicite.query.filter_by(agence_id=aid).all()
#    publicite_item = Publicite.query.filter_by(id=pid)
#    db.session.delete(publicite_item)

#    return render_template('publicite.html',form=pubForm,publicites=publicites,agence=agence)



# @main.route('/get_publicite', methods=['POST','GET'])
# def get_publicite():
#    app = current_app._get_current_object()
#    code = request.json["code"]
#    #print(code)
#    agence = Agence.query.filter_by(code=code).first()
#    publicites = Publicite.query.filter_by(agence_id=agence.id).all()

#    return jsonify({'publicite': ['{}{}'.format(app.config['WEB_URL'].replace('/pozy',''),publicite.url) for publicite in publicites]})


# @main.route('/check_agences', methods=['POST','GET'])
# def check_agences():
#    code = request.json["code"]
#    agence = Agence.query.filter_by(code=code).first()
#    return jsonify({'agence': "Acune valeur" if not agence else agence.to_json()})




# @main.route('/offre', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def offre():
#    offreForm = OffreForm(request.form)

#    if offreForm.validate_on_submit():
#       offre = Offre(titre=offreForm.titre.data,description=offreForm.description.data,prix=offreForm.prix.data,temps=offreForm.temps.data)
#       db.session.add(offre)
#       db.session.commit()
         
#    offres = Offre.query.filter_by().all()

#    return render_template('offre.html',form=offreForm,offres=offres)


# @main.route('/update_offre/<int:oid>', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def update_offre(oid):
#    offreForm = OffreForm(request.form)

#    offre = Offre.query.filter_by(id=oid).first()

#    if offreForm.validate_on_submit():
#       offre.titre=offreForm.titre.data
#       offre.description=offreForm.description.data
#       offre.temps=offreForm.temps.data
#       offre.prix=offreForm.prix.data
   
#    offres = Offre.query.all()


#    return render_template('offre.html',form=offreForm,offres=offres)


# @main.route('/del_offre/<int:oid>', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def del_offre(oid):
#    offreForm = OffreForm(request.form)
#    offre = Offre.query.filter_by(id=oid).first()
#    #print(offre)
#    db.session.delete(offre)
#    offres = Offre.query.filter_by(id=oid).all()

#    return render_template('offre.html',form=offreForm,offres=offres)



# @main.route('/payement', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def payement():
#    payementForm = PayementForm(request.form)

#    if payementForm.validate_on_submit():
#       payement = Payement(offre=payementForm.offre.data,etat=payementForm.etat.data,prix=payementForm.prix.data,temps=payementForm.temps.data)
#       db.session.add(payement)
#       db.session.commit()
         
#    payements = Payement.query.filter_by().all()

#    return render_template('payement.html',form=payementForm,payements=payements)


# @main.route('/update_payement/<int:pid>', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def update_payement(pid):
#    payementForm = PayementForm(request.form)

#    payement = Payement.query.filter_by(id=pid).first()

#    if payementForm.validate_on_submit():
#       payement.temps=payementForm.temps.data
#       payement.prix=payementForm.prix.data
#       payement.etat=payementForm.etat.data
#       payement.offre=payementForm.offre.data
#       payement.date_debut=payementForm.date_debut.data
#       payement.date_fin=payementForm.date_fin.data


#    payements = Payement.query.all()


#    return render_template('publicite.html',form=payementForm,payements=payements,payement=payement)


# @main.route('/del_payement/<int:pid>', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def del_payement(pid):
#    payement = Payement.query.filter_by(id=pid).first()
#    db.session.delete(payement)
#    payements = Payement.query.all()

#    return render_template('payement.html',form=payementForm,payements=offres)



# @main.route('/payement/<eid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def mes_payements(eid):
#    payementForm = PayementForm(request.form)

#    offres = Offre.query.all()
         
#    payements = Payement.query.filter_by(entreprise_id=current_user.entreprise_id).all()

#    return render_template('payement.html',form=payementForm,payements=payements,offres=offres)


# @main.route('/achat_offre/<oid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def achat_offre(oid):
#    payementForm = PayementForm(request.form)

#    offres = Offre.query.all()
#    offre = Offre.query.filter_by(id=oid).first()
#    entreprise = Entreprise.query.filter_by(id=current_user.entreprise_id).first()
#    payement = Payement(offre=offre.titre,etat="En cours",prix=offre.prix,temps=offre.temps,entreprise_id=current_user.entreprise_id, entreprise=entreprise.denomination)
#    db.session.add(payement)
#    db.session.commit()
         
#    payements = Payement.query.filter_by(entreprise_id=current_user.entreprise_id).all()

#    return render_template('payement.html',form=payementForm,payements=payements,offres=offres)


# @main.route('/annuler_offre/<pid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def annuler_offre(pid):
#    payement = Payement.query.filter_by(id=pid).first()
#    payement.etat = "Annuler"
#    db.session.add(payement)
#    db.session.commit()

#    return {"response":True}

# @main.route('/valider_offre/<pid>', methods=['POST','GET'])
# @login_required
# @super_admin_required
# def valider_offre(pid):
#    payement = Payement.query.filter_by(id=pid).first()
#    payement.etat = "Payer"
#    db.session.add(payement)
#    db.session.commit()

#    if payement.etat =="Payer":
#       entreprise = Entreprise.filter_by(id=payement.entreprise_id).first()
#       entreprise.etat = True
#       db.session.add(entreprise)
#       db.session.commit()

#    return {"response":True}

# @main.route('/update_payement/<eid>/<int:pid>', methods=['POST','GET'])
# @login_required
# @entreprise_admin_required
# def update_mes_payement(eid,pid):
#    payementForm = PayementForm(request.form)
#    payement = Payement.query.filter_by(id=pid).first()

#    if payementForm.validate_on_submit():
#       payement.temps=payementForm.temps.data
#       payement.prix=payementForm.prix.data
#       payement.etat=payementForm.etat.data
#       payement.offre=payementForm.offre.data
#       payement.date_debut=payementForm.date_debut.data
#       payement.date_fin=payementForm.date_fin.data
   
#    payements = Payement.query.all()

#    return render_template('publicite.html',form=payementForm,payements=payements,payement=payement)


# @main.route('/check_equipment', methods=['POST','GET'])
# def check_equipment():

#    print(request.headers)
#    print(request.headers['User-Agent'])

#    return render_template('hearder.html',headers=request.headers)
