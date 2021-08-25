#import sys
#sys.path.append('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/src/')

import flask_monitoringdashboard as dashboard
from flask import Flask, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from werkzeug.security import generate_password_hash
from app.database import mongoinit
from settings import *




#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = "users.login"


######################################
#### Application Factory Function ####
######################################

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    initialize_extensions(app)
    register_blueprints(app)
    dashboard.bind(app)
    return app

##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    mongoinit.init()

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    #csrf.init_app(app)

    # Flask-Login configuration
    from .models import UserModel

    @login.user_loader
    def load_user(user_id):
        """Check if user is logged-in on every page load."""
        try:
            return UserModel.query.filter(UserModel.id == int(user_id)).first()
        except:
            return None    
        #return UserModel.query.filter(UserModel.id == int(user_id)).first()

    @login.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to Login page."""
        flash('You must be logged in to view that page.')
        return redirect(url_for('app_routes.login'))    

    @app.errorhandler(404)
    def page_not_found(e):
        if e == 404:
            return redirect(url_for('app_routes.handle_unexpected_error'))
        if e == 500:
            return redirect(url_for('app_routes.handle_unexpected_error'))
        #return render_template('404.html'), 404


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from .views import app_routes
    from .admin import admin

    app.register_blueprint(app_routes)
    app.register_blueprint(admin)

from .models import UserModel, ACCESS
def create_admin(exist = False):
    if exist == False:
        admin = UserModel(username=ADMIN_USERNAME,email=ADMIN_EMAIL,plaintext_password=ADMIN_PASSWORD,access= ADMIN_ACCESS)
        db.session.add(admin)
        db.session.commit()



######################################
#### Application Error Handling ####
######################################
# Register the handlers against all the loggers we have in play
# This is done after app configuration and SQLAlchemy initialisation, 
# drop the sqlalchemy if not using - I thought a full example would be helpful.
import logging
from settings import DevelopementConfig
from app.errorlogger import mail_handler

#from .utils.logs import mail_handler, file_handler
#loggers = [app.logger, logging.getLogger('sqlalchemy'), logging.getLogger('werkzeug')]
import logging.config

from os import path
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.cfg')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

logger.addHandler(mail_handler)
# Note - I added a boolean configuration parameter, MAIL_ON_ERROR, 
# to allow direct control over whether to email on errors. 
# You may wish to use 'if not app.debug' instead.
if not DevelopementConfig.DEBUG:
    logger.addHandler(mail_handler)