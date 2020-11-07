
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
