from datetime import datetime
from flask import render_template,session, redirect, url_for,flash,make_response,request, g, jsonify
from . import main
from ..utilities import *
from .forms import *
from flask_login import login_user,login_required,logout_user,current_user
from ..models.models import *
from ..notifications import *
import json
from ..decorators import *

@main.route('/dash_admin_entreprise', methods=['POST','GET'])
@login_required
@super_admin_required
def dash_entreprise():

   print(request.host)
   if current_user.is_authenticated:
      data = {
         "agences":Agence.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
         "services":Service.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
         "guichets":Guichet.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
         "tickets":Ticket.query.filter_by(entreprise_id=current_user.entreprise_id).count(),
      }

      val = {
         "evolution":[50000, 10000, 5000, 15000, 17000, 20000, 15000, 28000, 20000, 30000, 25000, 40000],
         "etat":[30,60]
      }

      return json.dumps(val)
   else:
      return redirect(url_for('auth.login'))


@main.route('/dash_entreprise', methods=['POST','GET'])
@login_required
@entreprise_admin_required
def dash_admin_entreprise():
   return dataReturn()


@main.route('/dash_entreprise_agence', methods=['POST','GET'])
@login_required
@entreprise_admin_required
def dash_entreprise_agence():
   return dataReturn()

@main.route('/dash_agence_agence', methods=['POST','GET'])
@login_required
@entreprise_admin_required
def dash_agence_agence():
   return dataReturn()

def dataReturn():
   print(request.host)
   if current_user.is_authenticated:
      val_list = [0,0,0,0,0,0,0,0,0,0,0,0]
      year = datetime.now().year
      data = db.session.execute("select to_char(date_create, 'MM') as mois, count(id) as nombre from tickets where to_char(date_create, 'YYYY')=:annee group by to_char(date_create, 'MM') order by 1",{'annee':str(year)})

      for v in data:
         val_list[int(v.mois)-1] = v.nombre

      val = {
         "evolution":val_list,
         "etat":[
            Ticket.query.filter_by(etat="nouveau").count(),
            Ticket.query.filter_by(etat="appeler").count(),
            Ticket.query.filter_by(etat="absent").count()
         ]
      }

      return json.dumps(val)
   else:
      return redirect(url_for('auth.login'))


@main.route('/agence_dash', methods=['POST','GET'])
@login_required
@entreprise_admin_required
def agence_dash():
   return render_template('agence_dash.html')


@main.route('/service_dash', methods=['POST','GET'])
@login_required
@entreprise_admin_required
def service_dash():
   return render_template('service_dash.html')

@main.route('/guichet_dash', methods=['POST','GET'])
@login_required
@entreprise_admin_required
def guichet_dash():
   return render_template('guichet_dash.html')