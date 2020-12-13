
from flask import jsonify, request, current_app, url_for
from . import api
from ... import db
from ...models import *
from flask import g, jsonify
from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
import datetime


#Read ticket
@api.route('/offres',methods=['GET'])
def get_offres():
    offres = Offre.query
    return jsonify({ 'offres': [ offre.to_json() for offre in offres ] })


@api.route('/contactform-process',methods=['POST'])
def add_contact():
    if request.json['terms']=="Agreed-to-Terms":
        contact = Contact(nom=request.json['name'],email=email,message=message)
        db.session.add(contact)
        bd.session.commit()
    return jsonify({ 'Contact': contact.to_json() })

@api.route('/get_contact',methods=['GET'])
def get_contacts():
    contacts = Contact.query
    return jsonify({ 'Contact': [ contact.to_json() for contact in contacts ]})