import os

parent_path = os.path.abspath(os.path.dirname(__file__)+ '/static/qrcodes')

print(os.path.exists(parent_path))