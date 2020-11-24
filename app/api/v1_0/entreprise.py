
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import *
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth

from flask_login import login_user,login_required,logout_user,current_user


#Create entreprise
@api.route('/entreprises',methods=['POST'])
def add_entreprise():
    print('Alo')
    entreprise = Entreprise(denomination=request.json['denomination'],
                        numero=request.json['numero'],
                        localisation=request.json['localisation'],
                        user_id=current_user.id)
    db.session.add(entreprise)
    db.session.commit()

    return jsonify({ 'entreprise': entreprise.to_json() })


#Read entreprise
@api.route('/entreprises',methods=['GET'])
def get_entreprises():
    entreprises = Entreprise.query
    return jsonify({ 'entreprises': [ entreprise.to_json() for entreprise in entreprises ] })


#Read one entreprise
@api.route('/entreprises/<int:eid>',methods=['GET'])
def get_entreprise(eid):
    entreprise = Entreprise.query.filter_by(id=tid).first()
    return jsonify({ 'entreprise':  entreprise })


#Update entreprise
@api.route('/entreprises/<int:eid>',methods=['PATCH','UPDATE'])
def update_entreprise(eid):
    entreprise = Entreprise.query.filter_by(id=tid).first()

    entreprise(denomination=request.json['denomination'],
                        numero=request.json['numero'],
                        localisation=request.json['localisation'],
                        code=request.json['code'],
                        entreprise_id=request.json['entreprise'],
                        user_id=current_user.id)
    db.session.add(entreprise)
    db.session.commit()

    return jsonify({ 'entreprise': entreprise.to_json() })


#Delete entreprise
@api.route('/entreprises/<int:eid>',methods=['DELETE'])
def del_entreprises(eid):
    entreprise = Entreprise.query.filter_by(id=tid)
    db.session.delete(entreprise)
    return jsonify({'operations': 'DELETE', 'stat': "Succesfull"})