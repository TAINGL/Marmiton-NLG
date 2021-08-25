from settings import *
from app import create_app, mail
from flask_mail import Message

# Call the application factory function to construct a Flask application
# instance using the development configuration

app = create_app('settings.DevelopementConfig')

@app.route('/')
def index():
    sender = os.getenv('MAIL_USERNAME')
    recipients = [os.getenv('MAIL_USERNAME')]
    msg = Message()
    msg.subject = "Test Send"
    msg.recipients = recipients
    msg.sender = sender
    msg.body = 'testing'
    mail.send(msg)

if __name__ == '__main__':
    app.run()