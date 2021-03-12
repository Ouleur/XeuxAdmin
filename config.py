import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess strin'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    PO_MAIL_SUBJECT_PREFIX = 'Mail Subject'
    PO_MAIL_SENDER = 'SENDER NAME'
    PO_ADMIN = os.environ.get('PO_ADMIN') or 'mail@mail.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "addre@gmail.com"
    MAIL_PASSWORD = "password"


    @staticmethod
    def init_app(app):
        pass

    def resetdb(DB_URL):
        """Destroys and creates the database + tables."""

        from sqlalchemy_utils import database_exists, create_database, drop_database
        if database_exists(DB_URL):
            print('Deleting database.')
            drop_database(DB_URL)
        if not database_exists(DB_URL):
            print('Creating database.')
            create_database(DB_URL)

        print('Creating tables.')
        db.create_all()
        print('Shiny!')


class DevelopmentConfig(Config):
    DEBUG = True
    POSTGRES_DB = "db_xeux"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="http://127.0.0.1:5000"
    SITE_URL="http://127.0.0.1/vitapp"
    SCREEN_URL="http://localhost:8080/"
    MERCURE_URL="http://127.0.0.1:3000"
    UPLOADS_DIR = "app/static/uploads/"
    


    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')



class TestingConfig(Config):
    TESTING = True
    POSTGRES_DB = "db_name"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="http://127.0.0.1:5000"
    SITE_URL="http://127.0.0.1/vitapp"
    SCREEN_URL="http://localhost:8080/"
    MERCURE_URL="http://127.0.0.1:3000"
    UPLOADS_DIR = "app/static/uploads/"


    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class BetaConfig(Config):
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess strin'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    PO_MAIL_SUBJECT_PREFIX = 'Mail Subject'
    PO_MAIL_SENDER = 'SENDER NAME'
    PO_ADMIN = os.environ.get('PO_ADMIN') or 'mail@mail.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "addre@gmail.com"
    MAIL_PASSWORD = "password"

    POSTGRES_DB = "db_name"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="http://127.0.0.1:5000"
    SITE_URL="http://127.0.0.1/vitapp"
    SCREEN_URL="http://localhost:8080/"
    MERCURE_URL="http://127.0.0.1:3000"
    UPLOADS_DIR = "app/static/uploads/"



    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProdcutionConfig(Config):
    POSTGRES_DB = "db_name"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="http://127.0.0.1:5000"
    SITE_URL="http://127.0.0.1/vitapp"
    SCREEN_URL="http://localhost:8080/"
    MERCURE_URL="http://127.0.0.1:3000"
    UPLOADS_DIR = "app/static/uploads/"

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development' : DevelopmentConfig,
    'testing':TestingConfig,
    'beta' : BetaConfig,
    'production':ProdcutionConfig,
    'default':DevelopmentConfig
}
