
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import *
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import datetime
from ... import wait_time_Average

#Create ticket
@api.route('/tickets/<int:sid>',methods=['POST'])
def add_ticket(sid):
    cur_date = datetime.datetime.now()
    cur = "{} {}".format(cur_date.strftime("%Y-%m-%d"),"00:00:00")
    tickets = Ticket.query.filter(Ticket.date_create>=cur ,Ticket.date_create<=cur_date,Ticket.service_id==sid)

    #recuperer la liste des tickets du service pour creer le numero
    service = Service.query.filter_by(id=sid).first()

    ticket = Ticket(servstr=service.denomination[0:2].upper(),
                        numero=tickets.count()+1,
                        etat='nouveau',
                        client_hash=request.json['client_hash'],
                        entreprise_id=service.entreprise_id,
                        agence_id=service.agences_id,
                        service_id=service.id)
    db.session.add(ticket)
    db.session.commit()

    return jsonify({ 'ticket': ticket.to_json() })


#Read ticket
@api.route('/tickets',methods=['GET'])
def get_tickets():
    tickets = Ticket.query
    return jsonify({ 'tickets': [ ticket.to_json() for ticket in tickets ] })



#Read ticket
@api.route('/call_ticket',methods=['GET'])
def call_tickets(service,agence):
    tickets = Ticket.query.filter_by()
    return jsonify({ 'ticket': [ ticket.to_json() for ticket in tickets ] })

#Read ticket
@api.route('/checkTicket/<int:sid>',methods=['GET'])
def check_tickets(sid):
    service = Service.query.filter_by(id=sid).first()
    agence = Agence.query.filter_by(id=service.agences_id).first()
    cur_date = datetime.datetime.now()
    cur = "{} {}".format(cur_date.strftime("%Y-%m-%d"),"00:00:00")
    tickets = Ticket.query.filter(Ticket.date_create>=cur ,Ticket.date_create<=cur_date,Ticket.service_id==sid)
    
    tickets_new = Ticket.query.filter(Ticket.date_create>=cur ,Ticket.date_create<=cur_date,Ticket.service_id==sid,Ticket.etat=="nouveau")
    tickets_servir = Ticket.query.filter(Ticket.date_create>=cur ,Ticket.date_create<=cur_date,Ticket.service_id==sid,Ticket.etat=="appeler")
    
    ticket = {
            'servstr': service.denomination[0:2],
            'numero': tickets.count()+1,
        }

    return jsonify({ 'tickets': ticket,
                    'agence':agence.to_json(),
                    'service':service.to_json(),
                    'info':{"tm":"{} min".format(wait_time_Average(tickets_servir,tickets_new))}})


#Read one ticket
@api.route('/tickets/<int:tid>',methods=['GET'])
def get_ticket(tid):
    ticket = Ticket.query.filter_by(id=tid).first()
    return jsonify({ 'ticket':  ticket })


#Update ticket
@api.route('/tickets/<int:tid>',methods=['PATCH','UPDATE'])
def update_ticket(tid):
    ticket = Ticket.query.filter_by(id=tid).first()

    ticket(numero=request.json['numero'],
                        etat=request.json['etat'],
                        date_appel=request.json['date_appel'],
                        client_hash=request.json['client_hash'],
                        entreprise_id=request.json['entreprise'],
                        agence_id=request.json['agence'],
                        service_id=request.json['service'])
    db.session.add(ticket)
    db.session.commit()

    return jsonify({ 'ticket': ticket.to_json() })


#Delete ticket
@api.route('/tickets/<int:tid>',methods=['DELETE'])
def del_tickets(tid):
    ticket = Ticket.query.filter_by(id=tid)
    db.session.delete(ticket)
    return jsonify({'operations': 'DELETE', 'stat': "Succesfull"})