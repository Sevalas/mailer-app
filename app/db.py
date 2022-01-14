import mysql.connector
import click

from flask import config, current_app, g
from flask import cli
from flask.cli import with_appcontext
from .schema import instructions
from app.domain.mail import Mail

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE'],
        )
        g.db_cursor = g.db.cursor(dictionary=True)
    return g.db, g.db_cursor

def close_db(e = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('database initialized')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_mails():
    db, db_cursor = get_db()
    mails = []
    db_cursor.execute("SELECT * FROM email")
    rows = db_cursor.fetchall()
    for row in rows:
        mail = Mail(id = row['id'],email = row['email'], subject = row['subject'], content = row['content'])
        mails.append(mail)
    return mails

def get_filtered_mails(filter):
    db, db_cursor = get_db()
    mails = []
    db_cursor.execute("SELECT * FROM email where LOWER(CONCAT_WS(email, subject, content)) LIKE %s", ('%' + filter.lower() + '%',))
    rows = db_cursor.fetchall()
    for row in rows:
        mail = Mail(id = row['id'],email = row['email'], subject = row['subject'], content = row['content'])
        mails.append(mail)
    return mails

def insert_mail(mail: Mail):
    db, db_cursor = get_db()
    db_cursor.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (mail.email, mail.subject, mail.content))
    db.commit()