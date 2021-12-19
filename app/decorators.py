from functools import wraps
from flask import abort
from flask_login import current_user
from .models.models import *

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                print(current_user.can(permission))
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def entreprise_admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

def super_admin_required(f):
    return permission_required(Permission.SUP_ADMINISTER)(f)


def entreprise_offre_active(f):
    
    return permission_required(Permission.SUP_ADMINISTER)(f)