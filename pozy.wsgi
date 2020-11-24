#!/usr/bin/python3
import logging
import sys
from flask import url_for, Flask, request
import os


os.environ['FLASK_CONFIG'] = "testing"
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/pozy')

from manage import app as application
