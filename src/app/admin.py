from os import access
from flask import request, redirect, render_template, Blueprint, abort, flash, url_for
from flask_login import login_required, current_user

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
        return render_template('dashboard.html')
    
    users = UserModel.query.filter_by(access=1).all()
    # users = UserModel.query.all()
    print(users)
    
    return render_template('table.html', title="Dashboard", users=users)

@admin.route('/dashboard')
@login_required
def dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin():
        #abort(403)
        return render_template('403_error.html')
    return redirect('http://localhost:5000/dashboard/overview')


@admin.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    users = UserModel.query.get_or_404(user_id)
    if users:
        db.session.delete(users)
        db.session.commit()
        flash('User Id deleted.')
        return redirect(url_for('admin.admin_dashboard'))
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/recipe_dashboard')
def recipe_dashboard():
    return render_template('dashboard.html')