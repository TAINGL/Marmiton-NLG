# TO DO -> Index
#from config import *
from settings import *
from app import create_app
from app import mail
from flask_mail import Message

# https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp

#app = create_app(BaseConfig)
app = create_app(os.getenv('FLASK_ENV') or 'config.DevelopementConfig')

@app.route('/')
def index():
    sender = 'tainglaura.contact@gmail.com'
    recipients = ['tainglaura.contact@gmail.com']
    msg = Message()
    msg.subject = "Test Send"
    msg.recipients = recipients
    msg.sender = sender
    msg.body = 'testing'
    mail.send(msg)

if __name__ == '__main__':
    app.run()