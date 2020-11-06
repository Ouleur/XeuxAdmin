
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import *
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth

from flask_login import login_user,login_required,logout_user,current_user

#Create agence
# @api.route('/agences',methods=['POST'])
# def add_agence():
#     print('Alo')

#     agence = Agence(denomination=request.json['denomination'],
#                         numero=request.json['numero'],
#                         localisation=request.json['localisation'],
#                         code=request.json['code'],
#                         entreprise_id=request.json['entreprise'],
#                         user_id=current_user.id)
#     db.session.add(agence)
#     db.session.commit()

#     return jsonify({ 'agence': agence.to_json() })


#Read agence
@api.route('/agences',methods=['GET'])
def get_agences():
    agences = Agence.query
    return jsonify({ 'agences': [ agence.to_json() for agence in agences ] })


#Read one agence
@api.route('/agences/<int:aid>',methods=['GET'])
def get_agence(agid):
    agence = Agence.query.filter_by(id=tid).first()
    return jsonify({ 'agence':  agence })


#Update agence
@api.route('/agences/<int:aid>',methods=['PATCH','UPDATE'])
def update_agence(agid):
    agence = Agence.query.filter_by(id=tid).first()

    agence(denomination=request.json['denomination'],
                        numero=request.json['numero'],
                        localisation=request.json['localisation'],
                        code=request.json['code'],
                        entreprise_id=request.json['entreprise'],
                        user_id=current_user.id)
    db.session.add(agence)
    db.session.commit()

    return jsonify({ 'agence': agence.to_json() })


#Delete agence
@api.route('/agences/<int:aid>',methods=['DELETE'])
def del_agences(aid):
    agence = Agence.query.filter_by(id=tid)
    db.session.delete(agence)
    return jsonify({'operations': 'DELETE', 'stat': "Succesfull"})



@api.route('/get_publicite/<code>', methods=['POST','GET'])
def get_publicite(code):
   agence = Agence.query.filter_by(code=code).first()
   publicites = Publicite.query.filter_by(agence_id=agence.id).all()
   print(publicites)
   return jsonify({'publicite': [publicite.to_json() for publicite in publicites]})


@api.route('/check_agences', methods=['POST','GET'])
def check_agences():
   print(request)
   agence = Agence.query.filter_by(code=code).first()
   return jsonify({'agence': "service.to_json()"})
