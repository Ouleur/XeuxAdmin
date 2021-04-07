from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,DateField,SelectField,BooleanField,FloatField,TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL
from ..models.models import *



class SecuriteForm(FlaskForm):
    password = PasswordField('Mot de passe ')
    confirmPassword = PasswordField('Confirmation mot de passe')
    submit = SubmitField('Enregistrer') 




class ProfileForm(FlaskForm):
    name = StringField('Nom et prénoms',[DataRequired(message="Saisissez votre Nom et prénoms SVP.")])
    mail = StringField('Email',[DataRequired(message="Saisissez une adresse mail SVP.")])
    submit = SubmitField('Enregistrer')  


class EquipementForm(FlaskForm):
    denomination = StringField('Dénomination',[DataRequired(message="Saisissez une dénomination SVP.")])
    position = StringField('Position',[DataRequired(message="Saisissez une position SVP.")])
    emei = StringField('Emei',[DataRequired(message="Saisissez un emei SVP.")])
    status = StringField('Status',[DataRequired(message="Saisissez un Status SVP.")])
    submit = SubmitField('Enregistrer')   
    

class EtudiantForm(FlaskForm):
    matricule = StringField('Matricule',[DataRequired(message="Saisissez une matricule SVP.")])
    nom = StringField('Nom',[DataRequired(message="Saisissez une nom SVP.")])
    prenoms = StringField('Prenoms',[DataRequired(message="Saisissez un Prenoms SVP.")])
    filiere = SelectField("Filiere",choices=[],coerce=str)
    niveau = SelectField("Niveau",choices=['LICENCE 1','LICENCE 2','LICENCE 3'],coerce=str)
    id_carte = StringField('Id Carte',[DataRequired(message="Saisissez un Id Carte SVP.")])
    submit = SubmitField('Enregistrer')   
    
    

class RechercheForm(FlaskForm):
    date = DateField('Titre')
    filiere = SelectField('Filiere',choices=[])
    niveau = SelectField("Niveau",choices=['LICENCE 1','LICENCE 2','LICENCE 3'],coerce=str)
    annee = SelectField('Annee',choices=[])
    
    submit = SubmitField('Chercher')  

