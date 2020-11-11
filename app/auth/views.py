from flask import render_template, session, redirect, url_for, flash,request,Markup
from flask_login import login_user,login_required,logout_user,current_user
from . import auth
from ..models import *
from .forms import *
from .. import db
from datetime import datetime
from ..email import *
from sqlalchemy.exc import SQLAlchemyError 
#pour la connexion
@auth.route('/login', methods=['POST','GET'])
def login():
    print("d")
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # on recupere le user
        if user is not None and user.verify_password(form.password.data): # on verifie si le mot de passe est juste
            login_user(user, form.remember_me.data) #On signifie qu'il exit
            return redirect(request.args.get('next') or url_for("main.home")) # on redirige vers l'interface
        flash('Email ou mot de passe incorrecte') # message flash lors d'une erreur
    return render_template('auth/login.html',form=form,key=session.get('mail'))


#pour se deconnecter
@auth.route("/logout", methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté !")
    return redirect(url_for('main.home'))

#Poour s'enregistrer
@auth.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.replace(" ","")).count():
            flash('Cette adresse mail existe déja !') 
        else:
            user = User(email=form.email.data,password=form.password.data,name="{} {}".format(form.last_name.data,form.first_name.data))

            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token().decode("utf-8")
            user.hash_token=token
            db.session.add(user)
            db.session.commit()
            

            entreprise = Entreprise(denomination=form.entreprise.data.upper(),
                            numero=form.numero_tel.data,
                            localisation=form.adresse.data,
                            create_by=user.id)

            db.session.add(entreprise)
            db.session.commit()

            user.entreprise_id = entreprise.id
            db.session.add(user)
            db.session.commit()

            send_email(user.email, 'Confirmez votre compte Podipo','confirm', user=user, token=token)
            login_user(user, form.remember_me.data) #On signifie que l'utilisateur est connecté

            return redirect(url_for("auth.unconfirmed")) # on redirige vers l'interface unconfirmed
    return render_template('auth/register.html', form=form)


#pour confirmer son enregistrement
@auth.route('/auth/confirm/<token>', methods=['POST','GET']) 
# @login_required
def confirm(token):

    user = User.query.filter_by(hash_token=token)
    if user.count()>1:
        user = user.first()
        user.confirm = True

    if current_user.confirmed:
        return redirect(url_for('main.home')) 

    if current_user.confirm(token):
        flash('Merci, cous avez confirmez votre compte!') 
    else:
        flash('Le lien de confirmation est invalide ou expiré.') 

    return redirect(url_for('main.home'))

#pour changer de mot de pass
@auth.route('/forgot_password', methods=['POST','GET'])
def forgot_password():
    form = PasswordInitForm()

    if form.validate_on_submit():
        # Envoie de mail de reinitialisation
        user = User.query.filter_by(email=form.email.data)
        if user.count():
            user=user.first()
            token = user.generate_reset_password_token().decode("utf-8")
            user.hash_token = token
            db.session.add(user)
            db.session.commit()
            send_email(user.email, 'Creez un nouveau mot de passe','rescue_password', user=user, token=token)

    return render_template('auth/forgot-password.html',form=form)

#pour creer un nouveau de mot de pass
@auth.route('/init_password/<token>', methods=['POST','GET'])
def init_password(token):
    user = User.query.filter_by(hash_token=token).first()

    form = NewPasswordForm()

    if form.validate_on_submit():
        if form.password.data == form.confirmPassword.data:
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            login_user(user, False) #On signifie que l'utilisateur est connecté
            return redirect(request.args.get('next') or url_for("main.home")) # on redirige vers l'interface

    if user.pwdConfirmToken(token):
        return render_template('auth/init_password.html',form=form)
    else:
        message = Markup('Cette demande n\'est plus valide !')
        flash(message)
        return render_template('auth/unconfirmed.html')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and "main" in request.endpoint:
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed', methods=['POST','GET'])
def unconfirmed():
    print(current_user)
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    
    message = Markup('Bienvenue <b>{}</b>, un email de confirmation vous a été envoyé par email.!'.format(current_user.name))
    flash(message)

    return render_template('auth/unconfirmed.html')

@auth.route('/confirm', methods=['POST','GET']) 
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=current_user, token=token)
    flash('Un nouveau mail de confirmation vous a été envoyé par mail.') 
    return redirect(url_for('main.index'))