from settings import *
from app import create_app
from app import mail
from flask_mail import Message

# Call the application factory function to construct a Flask application
# instance using the development configuration

#app = create_app(BaseConfig)
app = create_app('settings.DevelopementConfig') #or 'config.DevelopementConfig')

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