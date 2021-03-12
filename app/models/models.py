from . import db,login_manager
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
import hashlib


class baseModel():
    
    id = db.Column(db.Integer, primary_key=True)
    
    date_create = db.Column(db.DateTime(), default=datetime.utcnow)
    date_modify = db.Column(db.DateTime(), onupdate=datetime.utcnow)
    create_by = db.Column(db.Integer)
    modify_by = db.Column(db.Integer)

class Permission:
    USER = 0x01
    ADMINISTER = 0x02
    SUP_ADMINISTER = 0x04

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USER, True),
            'Ecole Admin' : (Permission.USER |
                           Permission.ADMINISTER , False),
            'Super Administrator' : (Permission.SUP_ADMINISTER, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
        
    def __repr__(self):
        return '<Role %r>' % self.name

class User(baseModel,db.Model,UserMixin):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['PO_ADMIN']:
                self.role = Role.query.filter_by(permissions=0x04).first()
            if self.role is None :
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    avatar_hash = db.Column(db.String(32))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    hash_token = db.Column(db.Text)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    # role = db.Column(db.String(32))

    # entreprises = db.relationship('Entreprise', back_populates="users")
    # agences = db.relationship('Agence')
    # services = db.relationship('Service')

    # entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprises.id"))


    role = db.relationship('Role', backref='users')

    
    def generate_confirmation_token(self, expiration=43200):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    
    def generate_reset_password_token(self, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.email})
    
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def pwdConfirmToken(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.email:
            return False
        return True

    @property
    def password(self):
        raise AttributeError("le mot de passe n'est pas un attribut lisible")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow() 
        db.session.add(self)

    def __repr__(self):
        return "<User %r>" % self.name

    #For API """
    
    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        
        return s.dumps({'id':self.id,"email":self.email,'state':self.confirmed})
    

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            print(data)
        except:
            return None
        print(User.query.get(data['id']))
        return User.query.get(data['id'])
    

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_super_administrator(self):
        return self.can(Permission.SUP_ADMINISTER)
    
    def is_entreprise_administrator(self):
        return self.can(Permission.ADMINISTER)


    #For API """
    def to_json(self):
        
        json_user = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'date_create': self.date_create,
            'date_modify':self.date_modify,
            'create_by': self.create_by,
            'modify_by':self.modify_by,
        }
        return json_user

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

class Etudiant(baseModel,db.Model):
    __tablename__ = "etudiants"
    nom = db.Column(db.String(255))
    prenoms = db.Column(db.String(255))
    matricule = db.Column(db.String(255))
    card_id = db.Column(db.String(255))
    niveau = db.Column(db.String(255))
    date_naissance = db.Column(db.Date())

    filiere_id = db.Column(db.Integer, db.ForeignKey('filieres.id'))
    
    presences = db.relationship('Presence', backref='etudiants')
    # services = db.relationship('Service', backref='entreprises')
    # tickets = db.relationship('Ticket', backref='entreprises')


    def to_json(self):
        filiere = Filiere.query.filter_by(id=self.filiere_id).first()
        etudiant_json = {
            "id":self.id,
            "nom":self.nom,
            "prenoms":self.prenoms,
            "matricule":self.matricule,
            "niveau":self.niveau,
            "card_id":self.card_id,
            "filiere_id":filiere.id,
            "filiere":filiere.denomination,
            "date_naissance":self.date_naissance,
        } 

        return etudiant_json

    def __repr__(self):
        return "<Etudiant %r>" % self.denomination
    
class Filiere(baseModel,db.Model):
    """Filiere()"""
    __tablename__ = "filieres"
    denomination = db.Column(db.String(255))

    # entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    # create_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    etudiants = db.relationship('Etudiant', backref='filieres')
    presences = db.relationship('Presence', backref='filieres')
    # tickets = db.relationship('Ticket', backref='agences')


    def to_json(self):
        json_filiere = {
            'id': self.id,
            'denomination': self.denomination,
        }
        return json_filiere

    def __repr__(self):
        return "<Filiere %r>" % self.denomination

class Presence(baseModel,db.Model):
    __tablename__ = "presences"
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    filiere_id = db.Column(db.Integer, db.ForeignKey('filieres.id'))
    matiere_id = db.Column(db.Integer, db.ForeignKey('matieres.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    niveau = db.Column(db.String(255))
    annee_academic_id = db.Column(db.Integer, db.ForeignKey('anneeAcademics.id'))

    # entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    # agence_id = db.Column(db.Integer, db.ForeignKey('agences.id'))
    

    def to_json(self):

        etudiant = etudiant.query.filter_by(id=etudiant_id).first()
        filiere = filiere.query.filter_by(id=filiere_id).first()
        matiere = matiere.query.filter_by(id=matiere_id).first()
        device = device.query.filter_by(id=device_id).first()
        annee_academic = annee_academic.query.filter_by(id=annee_academic_id).first()

        json_presence= {
            'id': self.id,
            'etudiant_id': self.etudiant_id,
            'etudiant':etudiant,
            'filiere_id': self.filiere_id,
            'filiere': filiere,
            'niveau': self.niveau,
            'device_id': self.device_id,
            'device': device,
            'annee_academic_id': self.annee_academic_id,
            'annee_academic':annee_academic
        }
        return json_presence

    def __repr__(self):
        return "<Presence %r>" % self.titre


class Matiere(baseModel,db.Model):
    __tablename__ = "matieres"
    denomination = db.Column(db.String(64))

    presences = db.relationship('Presence', backref='matieres')

    def to_json(self):
        json_matiere = {
            'id': self.id,
            'denomination': self.denomination,
        }
        return json_matiere

    def __repr__(self):
        return "<Matiere %r>" % self.denomination

class Device(baseModel,db.Model):
    __tablename__ = "devices"

    denomination = db.Column(db.String(200))
    position = db.Column(db.String(200))
    emei = db.Column(db.String(200))
    status = db.Column(db.String(200))

    presences = db.relationship('Presence', backref='devices')

    def to_json(self):
        json_device = {
            'id': self.id,
            'denomination': self.denomination,
            'position': self.position,
            'emei': self.emei,
            'status': self.status,
        }
        return json_device

    def __repr__(self):
        return "<Device %r>" % self.code


class AnneeAcademic(baseModel,db.Model):
    __tablename__ = "anneeAcademics"
    denomination = db.Column(db.String(64))
    presences = db.relationship('Presence', backref='annee_academics')

    def to_json(self):
        json_anneeAcademic = {
            'id': self.id,
            'denomination': self.denomination,
        }
        return json_anneeAcademic

    def __repr__(self):
        return "<AnneeAcademic %r>" % self.denomination

class Progression(baseModel,db.Model):
    __tablename__ = "progressions"
    niveau = db.Column(db.String(64))
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    annee_academic_id = db.Column(db.Integer, db.ForeignKey('anneeAcademics.id'))
    

    def to_json(self):
        json_anneeAcademic = {
            'id': self.id,
            'niveau': self.niveau,
            'etudiant_id': self.etudiant_id,
            'annee_academic_id': self.annee_academic_id,
        }
        return json_anneeAcademic

    def __repr__(self):
        return "<Progression %r>" % self.niveau

login_manager.anonymous_user = AnonymousUser
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


