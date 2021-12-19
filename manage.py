#!/usr/bin/env python
import os

from dotenv import load_dotenv

from flask import url_for
from app import create_app,db
from flask_migrate import Migrate
from app.models.models import *

load_dotenv()

print(os.environ.get('FLASK_CONFIG'))
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)


# @manager.command
# def list_routes():
#     import urllib
#     output = []
#     for rule in app.url_map.iter_rules():

#         options = {}
        
#         for arg in rule.arguments:
#             options[arg] = "1"

#         methods = ','.join(rule.methods)
#         url = url_for(rule.endpoint, **options)
#         line = urllib.parse.unquote("{} {} {}".format(rule.endpoint, methods, url))
#         output.append(line)

#     for line in sorted(output):
#         print(line)



if __name__ == '__main__':
    app.run()
