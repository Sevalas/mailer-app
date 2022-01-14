import os

from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config.from_mapping(
        SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY'),
        SENDGRID_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL'),
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )

    from . import db
    
    db.init_app(app)

    from . import mailer

    app.register_blueprint(mailer.blue_print)

    return app
