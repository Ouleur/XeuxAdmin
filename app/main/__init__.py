from flask import Blueprint
from ..models.models import Permission

main = Blueprint('main', __name__)

from . import views, dashboard




@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
