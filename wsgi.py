#!/usr/bin/python3
import logging
import sys
from flask import url_for, Flask, request
import os


os.environ['FLASK_CONFIG'] = "development"
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/XeuXAdmin')

from manage import app as application
if __name__ == "__main__":
    application.run(debug=True)
