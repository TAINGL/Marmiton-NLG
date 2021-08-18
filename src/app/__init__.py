import sys
sys.path.append('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/src/')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from elasticsearch import Elasticsearch
from app.database import mongoinit
import os, config

# initializes extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
jwt = JWTManager()
mail = Mail()
es = Elasticsearch()

# https://www.fullstackpython.com/flask-templating-render-template-examples.html (Exemple)
# def register_errorhandlers(app):
#     def render_error(e):
#         return render_template('errors/%s.html' % e.code), e.code

def create_app(config):
    
    # create application instance
    app = Flask(__name__)
    app.config.from_object(config)
    mongoinit.init()
    #app.elasticsearch = Elasticsearch(app.config['ELASTICSEARCH_URL']) if app.config['ELASTICSEARCH_URL'] else None

    # register blueprints
    from app.views import app_routes
    app.register_blueprint(app_routes)
    

    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'app_routes.login'
    jwt.init_app(app)
    mail.init_app(app)


    return app