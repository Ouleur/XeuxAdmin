
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import *
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import datetime
from ...email import *


#Read ticket
@api.route('/offres',methods=['GET'])
def get_offres():
    offres = Offre.query
    return jsonify({ 'offres': [ offre.to_json() for offre in offres ] })


@api.route('/contactform-process',methods=['POST','GET'])
def add_contact():
    if request.json['terms']=="Agreed-to-Terms":
        contact = Contact(nom=request.json['name'],mail=request.json['email'],message=request.json['message'])
        db.session.add(contact)
        db.session.commit()

        send_email(request.json['email'], '[Equipe Vit] Contact','contact')

    return jsonify({"response":'success'})

@api.route('/get_contact',methods=['GET'])
def get_contacts():
    contacts = Contact.query
    return jsonify({ 'Contact': [ contact.to_json() for contact in contacts ]})