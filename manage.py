#!/usr/bin/env python
import os

from flask import url_for
from app import create_app,db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models.models import *

print(os.getenv('FLASK_CONFIG') or 'default')
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        
        for arg in rule.arguments:
            options[arg] = "1"

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{} {} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)



manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()