from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField,TextAreaField,SubmitField,PasswordField,DateField,SelectField,BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL


class RegisterForm(FlaskForm):
    """ Sign up for a user account."""
    last_name = StringField('Nom',[DataRequired(message="Saisissez votre nom.")])
    first_name = StringField('Prénoms',[DataRequired(message="Saisissez vos prénoms.")])
    email = StringField('Email',[Email(message="Votre adresse mail est invalide."),DataRequired()])
    password = PasswordField('Password', [EqualTo('confirmPassword', message="Les mots de passe doivent corresponde."),DataRequired(message="Saisissez votre mot de passe SVP.")])
    confirmPassword = PasswordField("Ressaisissez le mot de passe", [DataRequired(message="Saisissez votre mot de passe SVP.")])
    entreprise = StringField('Entreprise',[DataRequired(message="Saisissez le nom d'Entreprise.")])
    adresse = StringField('Adresse',[DataRequired(message="Saisissez l'adresse d'Entreprise.")])
    numero_tel = StringField('Contact',[DataRequired(message="Saisissez votre contact.")])

    # recaptcha = RecaptchaField()
    submit = SubmitField('Enregistrer')         

class LoginForm(FlaskForm):
    """ Login on Dashboard """
    email = StringField('Email',[DataRequired(),Email(message="Votre adresse mail est invalide.")])
    password = PasswordField('Password', [DataRequired(message="Saisissez votre mot de passe SVP.")])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')         


class PasswordInitForm(FlaskForm):
    """ Password Initialisation """
    email = StringField('Email',[DataRequired(message="Saisissez votre mail SVP."),Email(message="Votre adresse mail est invalide.")])
    submit = SubmitField('Reinitialisation du mot de passe')         

class NewPasswordForm(FlaskForm):
    """ Password Initialisation """
    password = PasswordField('Password', [EqualTo('confirmPassword', message="Les mots de passe doivent corresponde."),DataRequired(message="Saisissez votre mot de passe SVP.")])
    confirmPassword = PasswordField("Ressaisissez le mot de passe", [DataRequired(message="Saisissez votre mot de passe SVP.")])
    submit = SubmitField('Reinitialisation du mot de passe')         
