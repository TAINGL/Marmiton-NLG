from app import db, mail
from app.emails import send_email
from app.models import UserModel,db,login
from app.gpt2 import *
from flask import request, redirect, url_for, render_template, Blueprint, Flask, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_login import login_required, current_user, login_user, logout_user
from elasticsearch import Elasticsearch
from app.database import mongoinit

from bson import json_util
import json

import logging.config

app_routes = Blueprint('app_routes', __name__)

logging.config.fileConfig('../src/app/logging.cfg', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

@app_routes.before_app_first_request
def create_all():
    db.create_all()
    logger.info('Create the tables and database if not exist')

@app_routes.route('/')
def athome():
    if current_user.is_authenticated:
        logger.info('Homepage with login session')
        return redirect('/home')
    logger.info('Homepage without login session')
    return render_template('accueil.html'), 200

@app_routes.route('/home', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'GET':
        logger.info('Homepage with login session')
        return render_template('home.html'), 200

    if request.method == 'POST': 

        if request.form.get("Instructions_button"):
            title = request.form['title'] # preprocessing sur les inputs
            ingredients = request.form['ingredients'] # preprocessing sur les inputs
            # Converting str to list
            keywords = ingredients.split(', ')
            print(ingredients)
            print(keywords)
            result_instruction = get_instruction(title, keywords)
            logger.info('Generation of instructions')
            return render_template('result_nlg.html', title = title, ingredients = ingredients, result_instruction = result_instruction), 200

        elif request.form.get("recipe_button"): 
            title = request.form['title'] # preprocessing sur les inputs
            ingredients = request.form['ingredients'] # preprocessing sur les inputs
            collection = 'recipe'
            print("title ", title)
            print("ingredients ", ingredients)
            print(type(ingredients))
            
            # Converting str to list
            keywords = ingredients.split(', ')
            #print(ingredients)
            #print(keywords)

            if title != "" and ingredients != "":
                result = mongoinit.find_one('recipe',
                    {
                        "$and": [
                                {"titles":{ "$regex" : title}},
                                {"NER":{ "$all" : keywords}} # $in
                            ]
                    }
                    )
            elif title != "" and ingredients == "":
                result = mongoinit.find_one('recipe', {"titles" : { "$regex" : title }})
            elif ingredients != "" and title == "":
                result = mongoinit.find_one('recipe', {"NER" : { "$all" : keywords }})

            else:
                result = mongoinit.get_random_doc('recipe')
                

            if result == None:
                noresult = 'Pas de résultat avec les mots clés choisis'
                logger.info('No result from search')
                return render_template('result_404.html')
            else:
                title = [value for key, value in result.items() if key == "titles"]
                total_times = [value for key, value in result.items() if key == "total_times"]
                yields = [value for key, value in result.items() if key == "yields"]
                ingredients = [value for key, value in result.items() if key == "ingredients"]
                instructions = [value for key, value in result.items() if key == "instructions"]
                image_link = [value for key, value in result.items() if key == "images"]
                links = [value for key, value in result.items() if key == "links"]
                NER = [value for key, value in result.items() if key == "NER"]
                print(title)
                print(ingredients)
                print(instructions)

                img_tag = '<img src="{0}">'.format(image_link[0])
                print(img_tag)

                logger.info('Similar recipe from mongoDB')
                #return json.dumps(result, indent=4, default=json_util.default, ensure_ascii=False).encode('utf8')
                return render_template('result_similar.html', title = title[0], ingredients = ingredients[0][0], result_instruction = instructions[0], image_link=image_link[0]), 200

    return render_template('home.html'), 200

@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.info('Already authenticated')
        return redirect(url_for('app_routes.home'))

    if request.method == 'GET':
        logger.info('Not authenticated')
        return render_template('login.html'), 200

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['pass']):
            login_user(user)
            logger.info('Profil login')
            return redirect(url_for('app_routes.home')), 200

        logger.error('Missing informations or error for login')
        return render_template('login.html'), 400

    logger.error('Missing informations or error for login')
    return render_template('login.html'), 400

@app_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        logger.info('Already authenticated')
        return redirect(url_for('app_routes.home'))

    if request.method == 'GET':
        logger.info('No authenticated')
        return render_template('signup.html'), 200

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['pass']
        ctrlpass = request.form['ctrlpass']
 
        if UserModel.query.filter_by(email=email).first():
            logger.info('Email already Present')
            return ('Email already Present')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info('Profil signup')
        return redirect(url_for('app_routes.login'))
    logger.error('Missing informations or error for signup')    
    return render_template('signup.html'), 400

@app_routes.route('/password_reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        return render_template('reset.html')

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.verify_email(email)
        if user:
            send_email(user)
            logger.info('The email has been sent')
            return render_template('send_confirmation.html'), 200
        return redirect(url_for('app_routes.login'))

@app_routes.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    user = UserModel.verify_reset_token(token)
    if not user:
        print('no user found')
        logger.error('User not found') 
        return redirect(url_for('app_routes.login')) # redirect('/login') 

    if request.method == 'POST':
        password = request.form['pass'] # request.form.get('pass')
        if password:
            user.set_password(password, commit=True)
            logger.info('New password set up')
            return redirect(url_for('app_routes.login')) 

    logger.info('The email has been reset')
    return render_template('reset_verified.html')

@app_routes.route('/logout')
def logout():
    logout_user()
    logger.info('Disconnection validated')
    return redirect(url_for('app_routes.home'))

@app_routes.route('/add_comments', methods=['GET', 'POST'])
def add_comments():
    if request.form.get("instructions_button"):
        pass
    elif request.form.get("instructions_button"):
        pass
    else:
        pass
    return render_template('result.html', title = title, ingredients = ingredients, result_instruction = result_instruction), 200

