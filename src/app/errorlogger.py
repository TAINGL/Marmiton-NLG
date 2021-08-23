import app

import smtplib
from logging.handlers import RotatingFileHandler, SMTPHandler
from email.message import EmailMessage
import email.utils
from settings import *
import logging.config

from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.cfg')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# Provide a class to allow SSL (Not TLS) connection for mail handlers by overloading the emit() method
class SSLSMTPHandler(SMTPHandler):

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(msg, self.fromaddr, self.toaddrs)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


# Set the level according to whether we're debugging or not
logger = logging.getLogger('Admin Alert')
if DevelopementConfig.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARN)

# Create equivalent mail handler
mail_handler = SSLSMTPHandler(mailhost=(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT')),
                           fromaddr=os.getenv('MAIL_USERNAME'),
                           toaddrs=[os.getenv('MAIL_USERNAME')],
                           subject='Error Log Mail',
                           credentials=(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD')))

# Set the email format
mail_handler.setFormatter(logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''))

# Only email errors, not warnings
mail_handler.setLevel(logging.ERROR)