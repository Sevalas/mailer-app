import os

from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = os.urandom(24)

    app.config.from_mapping(
        SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY'),
        SENDGRID_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL'),
        MONGO_URI = os.environ.get('MONGO_URI')
    )

    from . import db
    
    db.init_app(app)

    from . import mailer

    app.register_blueprint(mailer.blue_print)

    return app
