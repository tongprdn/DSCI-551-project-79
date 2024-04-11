from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sys
import os
from .forms import LoginForm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import connect_database
from src.db.operations import check_user_credentials, list_documents
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
            return redirect(url_for('admin.dashboard'))

    return render_template('login.html', form=form)


@admin_blueprint.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('.login'))

    # Example of listing first 10 documents from 'movies' collection
    movies = list_documents(collection='movies', limit=100, sort='id')
    # You would need similar logic for 'credits', 'users', 'user_interactions'
    return render_template('dashboard.html', movies=movies)
