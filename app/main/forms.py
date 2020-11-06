from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,DateField,SelectField,BooleanField,FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL
from ..models.models import *



class SecuriteForm(FlaskForm):
    password = PasswordField('Mot de passe ')
    confirmPassword = PasswordField('Confirmation mot de passe')
    submit = SubmitField('Enregistrer') 




class ProfileForm(FlaskForm):
    name = StringField('Nom et prénoms')
    mail = StringField('Email')
    submit = SubmitField('Enregistrer')  


class EtablissementForm(FlaskForm):
    name = StringField('Dénomination',[DataRequired(message="Saisissez une dénomination SVP.")])
    localisation = StringField('Localisation')
    numero = StringField('Numero',[DataRequired(message="Saisissez un numéro SVP.")])
    state = SelectField('Etat',choices=[("desactiver","Desactiver"),("active","Activer")])
    submit = SubmitField('Enregistrer')   


class CollaborateurForm(FlaskForm):
    name = StringField('Dénomination')
    mail = StringField('Numero')
    agence = SelectField("Agence",choices=[],coerce=int)
    service = SelectField("Service",choices=[],coerce=int)
    guichet = SelectField("Guichet",choices=[],coerce=int)
    submit = SubmitField('Enregistrer')         


class AgenceForm(FlaskForm):
    denomination = StringField('Dénominationl')
    numero = StringField('Numero')
    localisation = StringField('Localisation')
    submit = SubmitField('Enregistrer')         

class ServiceForm(FlaskForm):
    denomination = StringField('Dénominationl')
    code = StringField('Code')
    submit = SubmitField('Enregistrer')   

class GuichetForm(FlaskForm):
    code = StringField('Code')
    submit = SubmitField('Enregistrer')       

class PubliciteForm(FlaskForm):
    titre = StringField('Titre')
    etat = SelectField('Etat',choices=[("publier","Publier"),("non_publier","Non Publier")])
    url = StringField('Url')
    media_type = SelectField('Type Media',choices=[("Image","Image")],)
    submit = SubmitField('Enregistrer')  

class DisponibiliteForm(FlaskForm):
    # ,[DataRequired(message="Saisissez une date SVP.")
    date = StringField('Date')
    heure_debut = StringField('Heure debut')
    heure_fin = StringField('Heure fin', [DataRequired(message="Saisissez une heure de fin SVP.")])

    submit = SubmitField('Enregistrer')  