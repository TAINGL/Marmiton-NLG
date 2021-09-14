from flask import request, render_template, redirect, url_for, Blueprint, abort, flash
from flask_login import login_required, current_user

from app import db
from .forms import *
from .models import UserModel
from .database import mongoinit

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



@user.route('/review', methods=['GET','POST'])
@login_required
def review():
    collection = 'recipeNLG'
    get_id = current_user.id
    get_ref_id_doc = mongoinit.get_last_doc(collection, get_id)

    ref_id_doc = get_ref_id_doc.get('_id')
    ref_titles = get_ref_id_doc.get('titles')
    ref_ingredients = get_ref_id_doc.get('ingredients')
    ref_instructions = get_ref_id_doc.get('instructions')
    ref_id_user = get_ref_id_doc.get('id_user')

    if request.form.get("review_button"):
        try: 
            rate = request.form['rate']
            review = request.form['review']

            if get_id == ref_id_user:
                if rate != None and review != None:
                    update_dict = {"rate":rate,"review":review}
                elif rate == None and review != None:
                    update_dict = {"review":review}
                elif rate != None and review == None:
                    update_dict = {"rate":rate}
                else:
                    update_dict = {}
                mongoinit.update_recipeNLG(collection, ref_id_doc, update_dict)
                message = "Data update!"
                print('Data update!')
                return render_template('result_nlg.html', ref_titles=ref_titles, ref_ingredients=ref_ingredients, ref_instructions=ref_instructions, rate=rate, review=review, message=message), 200
            else:
                message = "Error, data no updated!"
                logger.error('Bad Request - invalid credendtial') 
                return render_template('result_nlg.html', ref_titles=ref_titles, ref_ingredients=ref_ingredients, ref_instructions=ref_instructions, rate=rate, review=review, message=message), 400

        except:
            return render_template('result_nlg.html', ref_titles=ref_titles, ref_ingredients=ref_ingredients, ref_instructions=ref_instructions), 200

    return render_template('result_nlg.html', ref_titles=ref_titles, ref_ingredients=ref_ingredients, ref_instructions=ref_instructions), 200


@user.route('/recipe_dashboard')
def recipe_dashboard():
    collection = 'recipeNLG'
    get_id = current_user.id
    query = ({'id_user': get_id})
    review_user = mongoinit.find_similar(collection, query)
    return render_template('dashboard.html', review_user=review_user)


@user.route('/delete/<recipe_id>', methods=['POST'])
def delete(recipe_id):
    collection = 'recipeNLG'
    mongoinit.delete_one(collection, recipe_id)
    return redirect(url_for('user.recipe_dashboard'))