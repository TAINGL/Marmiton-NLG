from flask import render_template
from flask_mail import Message
from threading import Thread
from app import mail
import os

from settings import *
import logging.config


from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.cfg')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
#logging.config.fileConfig('logging.cfg', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

def send_email(user):

    token = user.get_reset_token()

    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [user.email]
    msg.html = render_template('reset_email.html', user=user, token=token)

    mail.send(msg)

def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail_thrd(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=os.getenv('MAIL_DEFAULT_SENDER'), recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thrd = Thread(target=async_send_mail, args=[app, msg])
    thrd.start()
    return thrd