from flask import render_template, session, redirect, url_for, flash,request
from flask_login import login_user,login_required,logout_user,current_user
from . import auth
from ..models import User
from .forms import RegisterForm,LoginForm
from .. import db
from datetime import datetime
from ..email import *


#pour la connexion
@auth.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # on recupere le user
        if user is not None and user.verify_password(form.password.data): # on verifie si le mot de passe est juste
            login_user(user, form.remember_me.data) #On signifie qu'il exit
            return redirect(request.args.get('next') or url_for("main.home")) # on redirige vers l'interface
        flash('Email ou mot de passe incorrecte') # message flash lors d'une erreur
    return render_template('auth/login.html',form=form,key=session.get('mail'))


#pour se deconnecter
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.home'))

#Poour s'enregistrer
@auth.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirmez votre compte Podipo','confirm', user=user, token=token)
        flash('Un email de confirmation vous a été envoyé par email.')
        return redirect(url_for('main.home'))
    return render_template('auth/register.html', form=form)


#pour confirmer son enregistrement
@auth.route('/auth/confirm/<token>') 
# @login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index')) 

    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!') 
    else:
        flash('The confirmation link is invalid or has expired.') 

    return redirect(url_for('main.index'))

#pour changer de mot de pass
@auth.route('/forgot_password')
def forgot_password():
   return render_template('auth/forgot-password.html')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed:
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    print("ddd")
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm') 
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.') 
    return redirect(url_for('main.index'))