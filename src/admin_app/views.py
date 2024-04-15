from flask import Blueprint, render_template, request, redirect, url_for, flash, session, app
import sys
import os
import pymongo
from .forms import LoginForm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import connect_database
from src.db.operations import check_user_credentials, list_documents, get_model, get_keys
from src.db.models import User

admin_blueprint = Blueprint('admin', __name__)
connect_database()


@admin_blueprint.route('/')
def index():
    return redirect(url_for('.login'))


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Checks if the form is submitted and the data is valid
        username = form.username.data
        password = form.password.data
        user = check_user_credentials(username, password)  # Check credentials

        if not isinstance(user, User):
            flash(user)
        elif user.admin_status == 0:
            flash("You're not authorized.")
        else:
            session['admin_id'] = str(user.id)
            return redirect(url_for('admin.dashboard', collection_name='movies'))

    return render_template('login.html', form=form)


@admin_blueprint.route('/dashboard/<collection_name>')
def dashboard(collection_name):
    if 'admin_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('.login'))
    sort_field = None
    if collection_name == 'movies':
        sort_field = request.args.get('sort', 'title')
    elif collection_name == 'credits':
        sort_field = request.args.get('sort', '_id')
    elif collection_name == 'users':
        sort_field = request.args.get('sort', 'createAt')
    elif collection_name == 'user_interactions':
        sort_field = request.args.get('sort', '_id')
    sort_order = request.args.get('order', 'asc')
    filter_field = request.args.get('field', None)
    filter_op = request.args.get('op', None)
    filter_value = request.args.get('value', None)
    sort_direction = pymongo.ASCENDING if sort_order == 'asc' else pymongo.DESCENDING
    filter_by = {filter_field: filter_value} if filter_field and filter_value else None

    collection_keys = get_keys(collection_name)

    documents = list_documents(
        collection=collection_name,
        limit=100,
        sort_field=sort_field,
        sort_direction=sort_direction,
        filter_by=filter_by,
        filter_op=filter_op
    )
    return render_template('dashboard.html', documents=documents, collection_keys=collection_keys
                           , collection_name=collection_name)
