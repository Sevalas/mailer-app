from flask.scaffold import F
from werkzeug.datastructures import MultiDict
import app.db as db
import sendgrid
import sendgrid.helpers.mail as sg_helpers

from flask import ( Blueprint, render_template, request, flash, url_for, redirect, current_app )
from app.domain.mail import Mail

blue_print = Blueprint('mailer', __name__, url_prefix='/')

@blue_print.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    if search is not None:
        mails = db.get_filtered_mails(search)
    else:
        mails = db.get_mails()
    return render_template('mails/index.html', mails=mails)

@blue_print.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        mail = Mail(email= request.form.get('email'),subject= request.form.get('subject'), content= request.form.get('content'))
        errors = []

        if not mail.email: errors.append('The email field is required.')
        if not mail.subject: errors.append('The subject field is required.')
        if not mail.content: errors.append('The content field is required.')

        if not len(errors) == 0:
            for error in errors:
                flash(error)
        else:
            is_email_sent = send(mail)
            if is_email_sent:
                db.insert_mail(mail)
                return(redirect(url_for('mailer.index')))
            else:
                flash('Error sending Email, please try again.')

    return render_template('mails/create.html')

def send(mail):
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_API_KEY'])
    from_email = sg_helpers.Email(current_app.config['SENDGRID_FROM_EMAIL'])
    to_email = sg_helpers.To(mail.email)
    content = sg_helpers.Content('text/plain', mail.content)
    sg_mail= sg_helpers.Mail(from_email, to_email, mail.subject, content)
    
    is_email_sent = False
    try:
        response = sg.client.mail.send.post(request_body=sg_mail.get())
        if response and response.status_code == 202: 
            is_email_sent = True
        else:
            print('Error sending mail, {}'.format(response.status_code))

    except Exception as e:
        print('Error sending mail, {}'.format(e))
    
    return is_email_sent