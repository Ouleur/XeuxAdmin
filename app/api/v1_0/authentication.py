from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from .errors import forbidden,unauthorized
from ...models import User,AnonymousUser,Permission
from ...email import send_email
from . import api
from .decorators import permission_required
from flask_cors import CORS,cross_origin

auth = HTTPBasicAuth()
CORS(api, supports_credentials=True)

@auth.verify_password
def verify_password(email_or_token,password):

    print(email_or_token)
    if email_or_token=='':
        g.current_user = AnonymousUser()
        return True
        
    if password == '':
        print(email_or_token)
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    
    user = User.query.filter((User.email==email_or_token) & (User.role=="AUTOMOBILISTE")).first()
    if not user :
        return False 
    
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials'),401

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/tokens/', methods=['POST'])
@cross_origin()
@auth.login_required
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token':  g.current_user.generate_auth_token(expiration=3600).decode("utf-8") , 'expiration': 3600})



