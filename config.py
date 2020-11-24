import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess strin'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
<<<<<<< HEAD
    PO_MAIL_SUBJECT_PREFIX = '[Podipo]'
    PO_MAIL_SENDER = 'Podipo Admin <info@podipo.com>'
    PO_ADMIN = os.environ.get('PO_ADMIN') or 'admin@popodipo.com'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

=======
    PO_MAIL_SUBJECT_PREFIX = '[VIT]'
    PO_MAIL_SENDER = 'VIT Admin <info@filevit.com>'
    PO_ADMIN = os.environ.get('PO_ADMIN') or 'admin@fileapp.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "ouleur000@gmail.com"
    MAIL_PASSWORD = "01709902#ouleur000"


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
    POSTGRES_DB = "popodipo_dev"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="http://127.0.0.1:5000"
<<<<<<< HEAD
    MERCURE_URL="http://127.0.0.1:3000"
    UPLOADS_DIR = "app/static/uploads/"

=======
    SITE_URL="http://127.0.0.1/vitapp"
    SCREEN_URL="http://localhost:8080/"
    MERCURE_URL="http://127.0.0.1:3000"
    UPLOADS_DIR = "app/static/uploads/"
    
>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72


    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

<<<<<<< HEAD
=======


>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72
class TestingConfig(Config):
    TESTING = True
    POSTGRES_DB = "popodipo_test"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="http://144.91.127.68/pozy"
<<<<<<< HEAD
=======
    SITE_URL="http://www.filevit.com"
    SCREEN_URL="http://144.91.127.68/screen"
>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72
    MERCURE_URL="http://144.91.127.68:4040"
    UPLOADS_DIR = "/var/www/pozy/app/static/uploads/"


    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

<<<<<<< HEAD
=======
class BetaConfig(Config):
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess strin'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    PO_MAIL_SUBJECT_PREFIX = '[VIT]'
    PO_MAIL_SENDER = 'VIT Admin <infos@filevit.com >'
    PO_ADMIN = os.environ.get('PO_ADMIN') or 'admin@fileapp.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'mail47.lwspanel.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "infos@filevit.com "
    MAIL_PASSWORD = "01709902@Vit"

    POSTGRES_DB = "popodipo_dev"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="htt://app.filevit.com"
    SITE_URL="htt://www.filevit.com"
    SCREEN_URL="htt://screen.filevit.com"
    MERCURE_URL="http://app.filevit.com:4040"
    UPLOADS_DIR = "/var/www/vitapp/app/static/uploads/"



    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72
class ProdcutionConfig(Config):
    POSTGRES_DB = "popodipo_prod"
    POSTGRES_URL="127.0.0.1:5432"
    POSTGRES_USER="odoo"
    POSTGRES_PW="odoo"
    WEB_URL="http://144.91.127.68/pozy"
    MERCURE_URL="http://144.91.127.68:4040"
    UPLOADS_DIR = "/var/www/pozy/app/static/uploads/"

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development' : DevelopmentConfig,
    'testing':TestingConfig,
<<<<<<< HEAD
=======
    'beta' : BetaConfig,
>>>>>>> d9b6f3502c686e1c5ea5988b9a2b7fac5032be72
    'production':ProdcutionConfig,
    'default':DevelopmentConfig
}
