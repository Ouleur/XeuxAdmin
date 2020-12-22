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
    GUICHET = 0x01
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
            'Guichet': (Permission.GUICHET, True),
            'Entreprise Admin' : (Permission.GUICHET |
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

    entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprises.id"))


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
        entreprise = Entreprise.query.filter_by(id=self.entreprise_id).first()
        
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
            'entreprise':"" if not entreprise else entreprise.denomination,
        }
        return json_user

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

class Entreprise(baseModel,db.Model):
    __tablename__ = "entreprises"
    denomination = db.Column(db.String(255))
    localisation = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    numero = db.Column(db.String(64))
    state = db.Column(db.Boolean, default=False)
    #create_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # agences = db.relationship('Agence', backref='entreprises')
    # services = db.relationship('Service', backref='entreprises')
    # tickets = db.relationship('Ticket', backref='entreprises')


    def to_json(self):
        vehicule_json = {
            "id":self.id,
            "denomination":self.denomination,
            "localisation":self.localisation,
            "numero":self.numero,
            "state":self.state,
            "logo":self.logo,
        } 

        return vehicule_json

    def __repr__(self):
        return "<Entreprise %r>" % self.denomination
    
class Agence(baseModel,db.Model):
    """Agence()"""
    __tablename__ = "agences"
    denomination = db.Column(db.String(255))
    numero = db.Column(db.String(255))
    localisation = db.Column(db.String(255))
    code = db.Column(db.String(10))
    logo = db.Column(db.String(255))
    ouverture = db.Column(db.Time())
    fermerture = db.Column(db.Time())

    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # users = db.relationship('User', backref='agences')
    services = db.relationship('Service', backref='agences')
    tickets = db.relationship('Ticket', backref='agences')


    def to_json(self):
        json_agence = {
            'id': self.id,
            'denomination': self.denomination,
            'numero': self.numero,
            'localisation': self.localisation,
            'logo': self.logo
        }
        return json_agence

    def __repr__(self):
        return "<Agence %r>" % self.denomination

class Publicite(baseModel,db.Model):
    __tablename__ = "publicites"
    titre = db.Column(db.String(64))
    etat = db.Column(db.String(50))
    url = db.Column(db.String(255))
    media_type = db.Column(db.String(255))

    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    agence_id = db.Column(db.Integer, db.ForeignKey('agences.id'))
    

    def to_json(self):
        json_expert = {
            'id': self.id,
            'titre': self.titre,
            'etat': self.etat,
            'media_type': self.media_type,
            'url': self.url,
            'entreprise_id': self.entreprise_id,
            'agence_id': self.agence_id,
        }
        return json_expert

    def __repr__(self):
        return "<Publicite %r>" % self.titre


class Service(baseModel,db.Model):
    __tablename__ = "services"
    denomination = db.Column(db.String(64))
    code = db.Column(db.String(200))

    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    agences_id = db.Column(db.Integer, db.ForeignKey('agences.id'))
    tickets = db.relationship('Ticket', backref='services')
    guichets = db.relationship('Guichet', backref='services')
    logo = db.Column(db.String(255))

    # users = db.relationship('User', backref='users')

    def to_json(self):
        json_expert = {
            'id': self.id,
            'denomination': self.denomination,
            'code': self.code,
            "logo":self.logo
        }
        return json_expert

    def __repr__(self):
        return "<Service %r>" % self.denomination

class Guichet(baseModel,db.Model):
    __tablename__ = "guichets"

    code = db.Column(db.String(200))

    create_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    agences_id = db.Column(db.Integer, db.ForeignKey('agences.id'))
    services_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    tickets = db.relationship('Ticket', backref='guichets')

    # users = db.relationship('User', backref='users')

    def to_json(self):
        json_expert = {
            'id': self.id,
            'code': self.code,
        }
        return json_expert

    def __repr__(self):
        return "<Guichet %r>" % self.code


class Ticket(baseModel,db.Model):
    __tablename__ = "tickets"
    servstr = db.Column(db.String(64))
    numero = db.Column(db.String(64))
    etat = db.Column(db.String(50))
    date_appel = db.Column(db.DateTime())
    client_hash = db.Column(db.String(255))


    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    agence_id = db.Column(db.Integer, db.ForeignKey('agences.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    guichet_id = db.Column(db.Integer, db.ForeignKey('guichets.id'))


    def to_json(self):
        guichet = Guichet.query.filter_by(id=self.guichet_id).first()
        json_expert = {
            'id': self.id,
            'servstr': self.servstr,
            'numero': self.numero,
            'etat': self.etat,
            'client_hash': self.client_hash,
            'entreprise_id': self.entreprise_id,
            'agence_id': self.agence_id,
            'service': self.service_id,
            'date_create': self.date_create.strftime("%Y-%m-%d"),
            'guichet': "" if not guichet else guichet.to_json(),
        }
        return json_expert

    def __repr__(self):
        return "<Ticket %r>" % self.numero


#Offres
class Offre(baseModel,db.Model):
    __tablename__ = "offres"
    titre = db.Column(db.String(64))
    description = db.Column(db.String(64))
    prix = db.Column(db.String(50))
    temps = db.Column(db.Integer())


    def to_json(self):
        guichet = Guichet.query.filter_by(id=self.guichet_id).first()
        json_expert = {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'prix': self.prix,
            'temps': self.temps,
        }
        return json_expert

    def __repr__(self):
        return "<Offre %r>" % self.titre


#Payements
class Payement(baseModel,db.Model):
    __tablename__ = "payements"
    entreprise = db.Column(db.String(64))
    temps = db.Column(db.String(64))
    prix = db.Column(db.String(64))
    etat = db.Column(db.String(50))
    offre = db.Column(db.String(50))
    numero_client = db.Column(db.String(50))
    numero_omarks = db.Column(db.String(50))
    date_debut = db.Column(db.DateTime(), default=datetime.utcnow)
    date_fin = db.Column(db.DateTime())

    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises.id'))
    
    def to_json(self):
        guichet = Guichet.query.filter_by(id=self.guichet_id).first()
        json_expert = {
            'id': self.id,
            'entreprise': self.entreprise,
            'temps': self.temps,
            'prix': self.prix,
            'etat': self.etat,
            'numero_client': self.numero_client,
            'numero_omarks': self.numero_omarks,
            "entreprise_id": self.entreprise_id,
            "offre": self.offre,
        }
        return json_expert

    def __repr__(self):
        return "<Payement %r>" % self.offre


login_manager.anonymous_user = AnonymousUser
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#Contact
class Contact(baseModel,db.Model):
    __tablename__ = "contact"
    nom = db.Column(db.String(64))
    mail = db.Column(db.String(64))
    message = db.Column(db.Text())

    def to_json(self):
        json_expert = {
            'id': self.id,
            'nom': self.nom,
            'mail': self.mail,
            'message': self.message,
        }
        return json_expert

    def __repr__(self):
        return "<Contact %r>" % self.nom
