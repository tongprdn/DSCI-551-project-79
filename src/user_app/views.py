from flask import Blueprint, request, flash, redirect, url_for, render_template, session, app, jsonify
import sys
import os
import pymongo
from forms import LoginForm

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from db.connection import get_database, connect_database
from db.operations import list_documents, get_model, get_keys, check_user_credentials, create_user, insert_one
from db.models import User, UserInteraction

user_blueprint = Blueprint('user', __name__)
connect_database()
client, db = get_database()

#Creating test-user
@user_blueprint.route('/')
def home():
    try:
        new_user = create_user(User(username='Pannawat', password='12345', 
                            email='justinbieber@gmail.com', admin_status=0))
    except:
        pass
    return redirect(url_for('.login'))

@user_blueprint.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Checks if the form is submitted and the data is valid
        username = form.username.data
        password = form.password.data
        user = check_user_credentials(username, password)  # Check credentials

        if not isinstance(user, User):
            flash(user)
            print(2)
        else:
            session['user_id'] = str(user.id)
            print(3)
            print(session)
            return redirect(url_for('user.index'))

    return render_template('login.html', form=form)


@user_blueprint.route('/index.html', methods = ['GET'])
def index():
    """
    
    """
    return render_template('index.html')


@user_blueprint.route('/catalog.html', methods = ['POST', 'GET'])
def catalog():
    movie_query = list_documents('movies', limit = 100, sort_field='imdb_score', sort_direction=pymongo.DESCENDING)
    
    if request.method == 'POST':
        favorite_movies = request.form.getlist("like_movies")
        print(favorite_movies)
        movie_collection = db['movies']
        n = 0
        for movie in favorite_movies:
            print(movie)
            movie_full = list(movie_collection.find({'title': {'$regex': movie, '$options': 'i'}}))
            movie_id = movie_full[0]['_id']
            
            user_id = session['user_id'] + str(n)
            print(user_id)
            print(movie_id)
            
            interaction = UserInteraction(user_id=user_id, movie_id=movie_id, liked = True)
            interactions = insert_one('user_interactions', interaction)
            
            n += 1
        movie_query = movie_collection.find({'title': {'$nin': favorite_movies}}).sort({'imdb_score': -1}).limit(100)
    else:
        pass
    #Create a generator to send in new movies
    return render_template('catalog.html', movies = movie_query)


@user_blueprint.route('/recommendations.html', methods = ['POST', 'GET'])
def rec():
    print(request.form)
    if (request.method == "POST"):
        search = request.form.get('searched_title')    
        print(search)
        pref = request.form.get('actor_name')  
        print(pref)  
        if search is not None:    
            searched = request.form['searched_title'].split(' ')
            searched_query = ('\s').join(searched)
            movie_collection = db['movies']
            movie_query = list(movie_collection.find({'title': {'$regex': searched_query, '$options': 'i'}}).limit(3).sort({'imdb_score': -1}))
            pass
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
        return render_template('recommendations.html')
        
    return render_template('recommendations.html', movies = movie_query)