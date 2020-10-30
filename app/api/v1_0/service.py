
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import *
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth

from flask_login import login_user,login_required,logout_user,current_user


#Create service
@api.route('/services',methods=['POST'])
def add_service():
    print('Alo')
    service = Service(denomination=request.json['denomination'],
                        numero=request.json['numero'],
                        localisation=request.json['localisation'],
                        code=request.json['code'],
                        entreprise_id=request.json['entreprise'],
                        agences_id=request.json['agence'],
                        user_id=current_user.id)
    db.session.add(service)
    db.session.commit()

    return jsonify({ 'service': service.to_json() })


#Read service
@api.route('/services',methods=['GET'])
def get_services():
    services = Service.query
    return jsonify({ 'services': [ service.to_json() for service in services ] })


#Read one service
@api.route('/services/<int:sid>',methods=['GET'])
def get_service(sid):
    service = Service.query.filter_by(id=sid).first()
    return jsonify({ 'service':  service })


#Read one service
@api.route('/agences_services/<int:aid>',methods=['GET'])
def get_agence_service(aid):
    services = Service.query.filter_by(agences_id=aid)
    agence = Agence.query.filter_by(id=aid).first()
    tickets = Ticket.query.filter_by(agence_id=aid)
    return jsonify({ 'services':  [ service.to_json() for service in services ],
                     "agence":{
                         "denomination":agence.denomination,
                         "evolution":"0/{}".format(tickets.count()),
                         "tm":"3",
                         "crenau":"08h00-16h30"
                        }
                    }
                )


#Update service
@api.route('/services/<int:sid>',methods=['PATCH','UPDATE'])
def update_service(sid):
    service = Service.query.filter_by(id=sid).first()

    service(denomination=request.json['denomination'],
                        numero=request.json['numero'],
                        localisation=request.json['localisation'],
                        code=request.json['code'],
                        entreprise_id=request.json['entreprise'],
                        agences_id=request.json['agence'],
                        user_id=current_user.id)
    db.session.add(service)
    db.session.commit()

    return jsonify({ 'service': service.to_json() })


#Delete service
@api.route('/services/<int:sid>',methods=['DELETE'])
def del_services(sid):
    service = Service.query.filter_by(id=sid)
    db.session.delete(service)
    return jsonify({'operations': 'DELETE', 'stat': "Succesfull"})