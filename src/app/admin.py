from flask import request, redirect, render_template, Blueprint, abort, flash
from flask_login import login_required, current_user, login_user, logout_user
# from sqlalchemy.exc import IntegrityError

from app import db
from .forms import *
from .models import UserModel


################
#### routes ####
################

app_routes = Blueprint('app_routes', __name__)
admin = Blueprint('admin', __name__)
    
@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin():
        #abort(403)
        return render_template('403_error.html')

    users = UserModel.query.all()
    print(users)
    
    return render_template('tabletest.html', title="Dashboard", users=users)

@admin.route('/dashboard')
@login_required
def dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin():
        #abort(403)
        return render_template('403_error.html')
    return redirect('http://localhost:5000/dashboard/overview')

#@admin.route('/add', methods=['POST'])
#def add():
#    if request.method == 'POST':
#        form = request.form
#        username = form.get('username')
#        email = form.get('email')
#        if not username or email:
#            users = UserModel(username = username, email = email)
#            db.session.add(users)
#            db.session.commit()
#            return redirect('/')
#
#    return "of the jedi"


@admin.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        users = UserModel.query.get(id)
        if users:
            return render_template('update.html', users=users)

    return "of the jedi"


@admin.route('/update', methods=['POST'])
def update():
    if not id or id != 0:
        users = UserModel.query.get(id)
        if users:
            db.session.delete(users)
            db.session.commit()
        return redirect('/')

    return "of the jedi"


@admin.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        users = UserModel.query.get(id)
        if users:
            db.session.delete(users)
            db.session.commit()
        return redirect('/')

    return "of the jedi"


@admin.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        users = UserModel.query.get(id)
        if users:
            users.status = not users.status
            db.session.commit()
        return redirect('/')

    return "of the jedi"