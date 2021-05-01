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

class FiliereForm(FlaskForm):
    id = StringField('id')
    denomination = StringField('Denomination',[DataRequired(message="Saisissez la Denomination SVP.")])
    submit = SubmitField('Enregistrer') 

class MatiereForm(FlaskForm):
    id = StringField('id')
    denomination = StringField('Denomination',[DataRequired(message="Saisissez la Denomination SVP.")])
    submit = SubmitField('Enregistrer') 


class EquipementForm(FlaskForm):
    id = StringField('Id')
    denomination = StringField('Dénomination',[DataRequired(message="Saisissez une dénomination SVP.")])
    position = StringField('Position',[DataRequired(message="Saisissez une position SVP.")])
    emei = StringField('Emei',[DataRequired(message="Saisissez un emei SVP.")])
    status = StringField('Status',[DataRequired(message="Saisissez un Status SVP.")])
    submit = SubmitField('Enregistrer')   
    

class EtudiantForm(FlaskForm):
    id = StringField('Id')
    matricule = StringField('Matricule',[DataRequired(message="Saisissez une matricule SVP.")])
    nom = StringField('Nom',[DataRequired(message="Saisissez une nom SVP.")])
    prenoms = StringField('Prenoms',[DataRequired(message="Saisissez un Prenoms SVP.")])
    date_naissance = DateField('Date de naissance',[DataRequired(message="Saisissez une Date de naissance SVP.")])
    filiere = SelectField("Filiere",choices=[])
    niveau = SelectField("Niveau",choices=['LICENCE 1','LICENCE 2','LICENCE 3'],coerce=str)
    antenne = SelectField("Antenne",choices=['ABIDJAN','BOUAKE','ABOISSO','KORHOGO',"ABENGOUROU"],coerce=str)
    groupe = SelectField("Groupe",choices=['Groupe 1','Groupe 2','Groupe 3','Groupe 4',"Groupe 5"],coerce=str)
    id_carte = StringField('Id Carte')
    submit = SubmitField('Enregistrer')   
    
    

class RechercheForm(FlaskForm):
    date = DateField('Titre')
    filiere = SelectField('Filiere',choices=[])
    niveau = SelectField("Niveau",choices=['LICENCE 1','LICENCE 2','LICENCE 3'],coerce=str)
    # annee = SelectField('Annee',choices=[])
    
    submit = SubmitField('Chercher')  

