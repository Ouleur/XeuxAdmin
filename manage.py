#!/usr/bin/env python
import os

from dotenv import load_dotenv

from flask import url_for
from app import create_app,db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models.models import *

load_dotenv()

print(os.environ.get('FLASK_CONFIG'))
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

<<<<<<< HEAD

=======
>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72
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
<<<<<<< HEAD
    manager.run()
=======
    manager.run()
>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72
