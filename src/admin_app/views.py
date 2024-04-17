import ast

from bson import SON
from flask import Blueprint, request, flash, redirect, url_for, render_template, session, app, jsonify
import sys
import os
import pymongo
from .forms import LoginForm
import json
from urllib import parse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import connect_database
from src.db.operations import (check_user_credentials, list_documents, get_keys, insert_one, preprocess_json_item,
                               get_model, delete_documents, get_item_by_id, update_one)
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
        limit=1000,
        sort_field=sort_field,
        sort_direction=sort_direction,
        filter_by=filter_by,
        filter_op=filter_op
    )
    return render_template('dashboard.html', documents=documents, collection_keys=collection_keys
                           , collection_name=collection_name)


@admin_blueprint.route('/insert_document', methods=['POST'])
def insert_document():
    collection_name = request.form.get('collection_name')
    if 'jsonFile' in request.files:
        file = request.files['jsonFile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            try:
                data = json.load(file)
                for item in data:
                    document = preprocess_json_item(item, get_model(collection_name))
                    insert_one(collection_name, document)
            except Exception as e:
                return jsonify({'status': 'error', 'message': f'Cannot insert file due to: {e}'})
    else:
        try:
            data = request.form.to_dict()
            print(data)
            if 'admin_status' in data and int(data['admin_status']) == 2:
                print("checking admin status")
                if not check_admin_status(session['admin_id']):
                    return jsonify({'status': 'error', 'message': f'You are not authorized to add super admin'})
            document = preprocess_json_item(data, get_model(collection_name))
            insert_one(collection_name, document)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Cannot insert file due to: {e}'})

    return jsonify({'status': 'success', 'message': f'Document inserted successfully'})


def check_admin_status(admin_id):
    if session['admin_id']:
        user = get_item_by_id('users', admin_id)
        print(user['admin_status'])
        if user['admin_status'] < 2:
            return False
        else:
            return True


@admin_blueprint.route('/delete_document', methods=['POST'])
def delete_document():
    collection_name = request.form.get('collection_name')
    if request.form.get('select-all'):
        if session['admin_id']:
            user = get_item_by_id('users', session['admin_id'])
            if user['admin_status'] < 2:
                return jsonify({'status': 'error', 'message': f'You are not authorized on this action. '
                                                              f'Please contact super admin'})
        params = request.form.get('params')
        params_dict = parse.parse_qs(parse.urlsplit(params).query)
        filterField = params_dict['field'][0]
        filterOp = params_dict['op'][0]
        filterValue = params_dict['value'][0]
        criteria = {filterField: {}}
        if filterOp == 'contains':
            criteria = {f'{filterField}__icontains': filterValue}
        elif filterOp == 'eq':
            criteria[filterField] = filterValue
        elif filterOp == 'ne':
            criteria = {f"{filterField}__ne": filterValue}
        else:
            raise ValueError("Unsupported filter operator: {}".format(filterOp))
    else:
        id_list = ast.literal_eval(request.form.get('ids'))
        if collection_name == "movies":
            criteria = {'_id__in': id_list}
        else:
            criteria = {'id__in': id_list}
    try:
        print(f'Deleting document matching : {criteria}')
        count = delete_documents(collection_name, criteria)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Cannot delete file due to: {e}'})
    return jsonify({'status': 'success', 'message': f'{count} document(s) deleted successfully'})


@admin_blueprint.route('/get-item-data/<collection_name>/<item_id>', methods=['GET'])
def get_item_data(collection_name, item_id):
    # Assuming get_item_by_id is a function that queries your database and returns the item data as a dictionary
    item_data = get_item_by_id(collection_name, item_id)
    print('get_item_data', item_data)
    if item_data:
        # If the item data was found, return it as JSON
        return jsonify(item_data), 200
    else:
        # If no item was found with the given ID, return a not found error
        return jsonify({"error": "Item not found"}), 404


@admin_blueprint.route('/edit_document/<collection_name>/<item_id>', methods=['POST'])
def edit_document(collection_name, item_id):
    data = request.form.to_dict()
    if 'title' in data:
        del data['title']
    if 'createAt' in data:
        del data['creatAt']
    if 'liked_on' in data:
        del data['liked_on']
    print('edit_document', data)
    try:
        update_one(collection_name, item_id, data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Cannot edit file due to: {e}'})

    return jsonify({'status': 'success', 'message': f'Document edited successfully'})


@admin_blueprint.route('/load-more-data', methods=['GET'])
def load_more_data():
    collection_name = request.args.get('collection')
    limit = 1000
    skip = int(request.args.get('skip', 0))
    sort_field = request.args.get('sort_field')
    sort_order = request.args.get('sort_order')
    filter_field = request.args.get('filter_field')
    filter_op = request.args.get('filter_op')
    filter_value = request.args.get('filter_value')
    print(request.args)
    sort_direction = pymongo.ASCENDING if sort_order == 'asc' else pymongo.DESCENDING
    filter_by = {filter_field: filter_value}
    documents = list_documents(
        collection=collection_name,
        limit=limit,
        sort_field=sort_field,
        sort_direction=sort_direction,
        filter_by=filter_by,
        filter_op=filter_op,
        skip=skip
    )

    response = {
        'newRows': documents,
        'totalRows': len(documents)
    }

    return response
