
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import User
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import subprocess


auth = HTTPBasicAuth()


#Create user
@api.route('/user',methods=['POST','GET'])
def add_user():
    print(request)
    print(User.query.filter_by(email=request.json["email"]))
    if not User.query.filter_by(email=request.json["email"]).first():
        user = User(email=request.json["email"],password=request.json['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'token':  user.generate_auth_token(expiration=3600).decode("utf-8") , 'expiration': 3600})
    
    return jsonify({'error':"Users already exist"}),403

#Read user
@api.route('/users/',methods=['GET'])
def get_users():
    if g.current_user.is_anonymous or not g.token_used:
        return unauthorized('Invalid credentials')
    users = User.query.all()
    return jsonify({ 'users': [user.to_json() for user in users] })


@api.route('/git_update',methods=['GET'])
def git_update():
    home_dir = subprocess.run(["git","pull","--no-edit"],stdout=subprocess.PIPE, text=True)
    return jsonify({ 'users': home_dir.stdout })
    