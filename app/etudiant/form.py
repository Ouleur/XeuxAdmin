from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,DateField,SelectField,BooleanField,FloatField,TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL
from ..models.models import *

class EtudiantForm(FlaskForm):
    id = StringField('Id')
    matricule = StringField('Matricule',[DataRequired(message="Saisissez une matricule SVP.")])
    nom = StringField('Nom',[DataRequired(message="Saisissez une nom SVP.")])
    prenoms = StringField('Prenoms',[DataRequired(message="Saisissez un Prenoms SVP.")])
    date_naissance = DateField('Date de naissance',[DataRequired(message="Saisissez une Date de naissance SVP.")])
    filiere = SelectField("Filiere",choices=[])
    niveau = SelectField("Niveau",choices=['Licence 1','Licence 2','Licence 3'],coerce=str)
    antenne = SelectField("Antenne",choices=['ABIDJAN','BOUAKE','ABOISSO','KORHOGO',"ABENGOUROU"],coerce=str)
    groupe = SelectField("Groupe",choices=['Groupe A','Groupe B','Groupe C','Groupe D',"Groupe E","Groupe F","Groupe G","Groupe H","Groupe I","Groupe J","Groupe K"],coerce=str)
    id_carte = StringField('Id Carte')
    submit = SubmitField('Enregistrer')