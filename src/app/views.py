from flask import request, redirect, url_for, render_template, Blueprint, abort, flash
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app import db, mail, create_admin
from .emails import send_email
from .forms import RegisterForm, LoginForm, ResetPasswordForm, NewPasswordForm
from .models import UserModel
from .database import mongoinit
from .gpt2 import *

import json
from os import path
import logging.config

################
#### routes ####
################

app_routes = Blueprint('app_routes', __name__)
admin = Blueprint('admin', __name__)
user = Blueprint('user', __name__)



log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.cfg')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

@app_routes.before_app_first_request
def create_all():
    create_admin(exist = UserModel.admin_exist())
    db.create_all()
    logger.info('Create the tables and database if not exist')

@app_routes.route('/', methods=['GET','POST'])
def homepage():
    return redirect(url_for('app_routes.login'))
    

@app_routes.route('/home', methods=['GET','POST'])
@login_required
def home():

    #if request.method == 'GET':
    #    logger.info('Homepage with login session')
    #    return render_template('home.html'), 200

    if request.method == 'POST': 

        if request.form.get("instructions_button"):
            title = request.form['title'] # preprocessing sur les inputs
            ingredients = request.form['ingredients'] # preprocessing sur les inputs
            # Converting str to list
            keywords = ingredients.split(', ')
            print(ingredients)
            print(keywords)
            result_instruction = get_instruction(title, keywords)

            collection = 'recipeNLG'
            get_id = current_user.id
            print(get_id)
            recipeNLG_dict = { "titles": title, 
                               "ingredients": keywords,
                               "instructions": result_instruction,
                               "rate": None,
                               "review": None,
                               "id_user": get_id                             
                               }
            mongoinit.insert(collection, recipeNLG_dict)
            logger.info('Generation of instructions')
            logger.info('Generation of instructions storage in MongoDB')
            print('Data Storage in DB!')
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
                result = mongoinit.find_one(collection,
                    {
                        "$and": [
                                {"titles":{ "$regex" : title}},
                                {"NER":{ "$all" : keywords}} # $in
                            ]
                    }
                    )
            elif title != "" and ingredients == "":
                result = mongoinit.find_one(collection, {"titles" : { "$regex" : title }})
            elif ingredients != "" and title == "":
                result = mongoinit.find_one(collection, {"NER" : { "$all" : keywords }})

            else:
                result = mongoinit.get_random_doc(collection)
                

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
                return render_template('result_similar.html', title = title[0], ingredients = ingredients[0][0], result_instruction = instructions[0], image_link=image_link[0]), 200

    return render_template('home.html'), 200


@app_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    # If the User is already logged in, don't allow them to try to register
    if current_user.is_authenticated:
        flash('Already registered!  Redirecting to your User Profile page...')
        logger.info('Already authenticated')
        return render_template('home.html'), 200

    form = RegisterForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form), 200

    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user = UserModel(form.username.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Thanks for registering, {}!'.format(new_user.username))
            logger.info('{} registered'.format(new_user.username))
            return render_template('home.html'), 200
        except IntegrityError:
            db.session.rollback()
            logger.error('This member already exists')
            return render_template('integrityerror.html'), 200

    logger.error('Missing informations or error for signup')  
    return render_template('signup.html', form=form), 400


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    # If the User is already logged in, don't allow them to try to log in again
    if current_user.is_authenticated:
        flash('Already logged in!  Redirecting to your User Profile page...')
        logger.info('Already authenticated')
        return redirect(url_for('app_routes.home'))        

    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form), 200

    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                flash('Thanks for logging in, {}!'.format(current_user.username))
                logger.info('{} logging in'.format(current_user.username))
                #return redirect(url_for('app_routes.home')), 200
                return render_template('home.html'), 200

    flash('ERROR! Incorrect login credentials.')
    logger.error('Missing informations or error for login')
    return render_template('login.html', form=form), 400


@app_routes.route('/password_reset', methods=['GET', 'POST'])
def reset():
    form = ResetPasswordForm()
    if request.method == 'GET':
        return render_template('reset.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserModel.verify_email(email=form.email.data)
            if user:
                send_email(user)
                logger.info('The email has been sent')
                return render_template('send_confirmation.html'), 200

        flash('ERROR! Incorrect email credentials.')    
        logger.error('This email does not exist in the database')
    return render_template('reset.html', form=form)

@app_routes.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    form = NewPasswordForm()
    user = UserModel.verify_reset_token(token)
    if not user:
        print('no user found')
        logger.error('User not found') 
        return redirect(url_for('app_routes.login')) # redirect('/login') 

    if request.method == 'POST':
        if form.validate_on_submit():
            user.set_password(form.password.data, commit=True)
            logger.info('New password set up')
            return redirect(url_for('app_routes.login'))

        flash('ERROR! Incorrect password credentials.')    
        logger.error('This password does not registered')
    return render_template('reset_verified.html', form=form)


@app_routes.route('/logout')
@login_required
def logout():
    user = current_user
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!')
    logger.info('You are log out')
    return redirect(url_for('app_routes.login'))

#@app_routes.route('/add_comments', methods=['GET', 'POST'])
#def add_comments():
#    if request.form.get("instructions_button"):
#        pass
#    elif request.form.get("instructions_button"):
#        pass
#    else:
#        pass
#    return render_template('result.html', title = title, ingredients = ingredients, result_instruction = result_instruction), 200

