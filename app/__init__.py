from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from config import config
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS,cross_origin

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()


def create_app(config_name):
    app = Flask(__name__,static_url_path='/app/static')
    CORS(app, resources={r"*": {"origins": "*"}})

    app.config.from_object(config[config_name])
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
<<<<<<< HEAD
=======
    
>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72

    from .main import main as main_bleuprint
    app.register_blueprint(main_bleuprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api.v1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix="/api/v1.0")

    return app