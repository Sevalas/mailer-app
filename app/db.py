
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_pymongo import PyMongo
from app.domain.mail import Mail

def get_db():
    if 'db' not in g:
        mongodb_client = PyMongo(current_app, uri=current_app.config['MONGO_URI'])
        g.db = mongodb_client.db
    return g.db

def close_db(e = None):
    g.pop('db', None)

def init_db():
    db = get_db()
    print(db)

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('database initialized')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_mails():
    db = get_db()
    mails = []
    fetchMails = db.mails.find();
    for mail in fetchMails:
        mail = Mail(id = mail['_id'],email = mail['email'], subject = mail['subject'], content = mail['content'])
        mails.append(mail)
    return mails

def get_filtered_mails(filter):
    db = get_db()
    mails = []
    fetchMails = db.mails.find({
         '$or': [
            {'email': {'$regex': filter.lower()}},
            {'subject': {'$regex': filter.lower()}},
            {'content': {'$regex': filter.lower()}},
     ]})
    for mail in fetchMails:
        mail = Mail(id = mail['_id'],email = mail['email'], subject = mail['subject'], content = mail['content'])
        mails.append(mail)
    return mails

def insert_mail(mail: Mail):
    db = get_db()
    db.mails.insert_one({'email':mail.email, 'subject':mail.subject, 'content':mail.content})