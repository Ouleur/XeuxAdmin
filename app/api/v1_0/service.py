
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import *
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user,login_required,logout_user,current_user
from ... import time_Average


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
    cur_date = datetime.now()
    cur = "{} {}".format(cur_date.strftime("%Y-%m-%d"),"00:00:00")
    tickets = Ticket.query.filter(Ticket.date_create>=cur ,Ticket.date_create<=cur_date,Ticket.agence_id==aid)
    tickets_servir = Ticket.query.filter(Ticket.date_create>=cur ,Ticket.date_create<=cur_date,Ticket.agence_id==aid,Ticket.etat=="appeler")
    
    ######### - get time average - #############
    

    ######### - get time average - #############

    return jsonify({ 'services':  [ service.to_json() for service in services ],
                     "agence":{
                         "denomination":agence.denomination,
                         "evolution":"{}/{}".format(tickets_servir.count(),tickets.count()),
                         "tm":time_Average(tickets_servir),
                         "crenau":"{}-{}".format(agence.ouverture.strftime("%H:%M"),agence.fermerture.strftime("%H:%M"))
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


