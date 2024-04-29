from flask import Blueprint, render_template, request, redirect, url_for, flash, session, app
import sys
import os
import pymongo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import get_database, connect_database
from src.db.operations import list_documents, get_model, get_keys

user_blueprint = Blueprint('user', __name__)
connect_database()
client, db = get_database()


@user_blueprint.route('/')
@user_blueprint.route('/index.html')
def index():
    """
    
    """
    
    return render_template('index.html')


@user_blueprint.route('/catalog.html')
def catalog():
    movie_query = list_documents('movies', limit = 50, sort_field='imdb_score', 
                                sort_direction=pymongo.DESCENDING)
    return render_template('catalog.html', movies = movie_query)


@user_blueprint.route('/recommendations.html', methods = ['POST'])
def rec():
    print(request.form)
    if (request.method == "POST"):
        search = request.form.get('search')    
        pref = request.form.get('pref')    
        if search is not None:    
            searched = request.form['searched_title'].split(' ')
            searched_query = ('\s').join(searched)
            movie_collection = db['movies']
            movie_query = list(movie_collection.find({'title': {'$regex': searched_query, '$options': 'i'}}).limit(3).sort({'imdb_score': -1}))
        
        elif pref is not None:
            select_type = request.form['type']
            select_genre = request.form['genre']
            actor_name = request.form['actor_name']
            dir_name = request.form['dir_name']
            
            collection = db['credits']
            actor_query = list(collection.find({'name': {'$regex': actor_name, '$options':'i'},'role':'ACTOR'}, {'movie_id': 1, '_id':0}).limit(50))
            director_query = list(collection.find({'name': {'$regex': dir_name, '$options':'i'},'role':'DIRECTOR'}, {'movie_id': 1, '_id':0}).limit(50))
            combined = actor_query + director_query
            movies_id = [item['movie_id'] for item in combined]
            print(movies_id)
            
            movie_collection = db['movies']
            movie_query = list(movie_collection.find({'genres': {'$in': [select_genre]}, 'type': select_type, '_id':{'$in': movies_id}}).limit(3).sort({'imdb_score': -1}))
            #movie_query = list(movie_collection.find({'type': select_type}))
            print(movie_query)        
        else:
            pass
    else: 
        pass
        
    return render_template('recommendations.html', movies = movie_query)