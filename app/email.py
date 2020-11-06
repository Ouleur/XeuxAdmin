from threading import Thread
import os
from flask_mail import Message
from flask import current_app,render_template
from . import mail



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email_with_file(to,cc, subject, template,document, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['PO_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['PO_MAIL_SENDER'], recipients=[to])
    msg.body = render_template('email/'+template + '.txt', **kwargs)
    msg.html = render_template('email/'+template + '.html', **kwargs)
    msg.cc = []
    working_dir = '/var/www/PO4driver/app/static/uploads/'
    with open(working_dir+document,'rb') as fh:
        msg.attach(filename="something.pdf",disposition="attachment",content_type="application/pdf",data=fh.read())
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['PO_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['PO_MAIL_SENDER'], recipients=[to])
    # msg.body = render_template('email/'+template+ '.txt', **kwargs)
    msg.html = render_template('email/'+template+ '.html', **kwargs)
    msg.cc = []
    
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr