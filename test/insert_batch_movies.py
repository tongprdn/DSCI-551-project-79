import json
import sys
import os
import ast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import connect_database
from src.db.models import Movie
from src.db.operations import insert_movie


def preprocess_data(item):
    item['_id'] = item['id']
    del item['id']
    item['title_hash'] = custom_hash(item['title'])
    try:
        if isinstance(item['title'], int):
            item['title'] = str(item['title'])

        if item.get('genres'):
            item['genres'] = ast.literal_eval(item['genres'])
        else:
            del item['genres']

        if item.get('production_countries'):
            item['production_countries'] = ast.literal_eval(item['production_countries'])
        else:
            del item['production_countries']

        if item.get('seasons') != "":
            item['seasons'] = float(item['seasons'])
        else:
            del item['seasons']

        if item.get('imdb_score') != "":
            item['imdb_score'] = float(item['imdb_score'])
        else:
            del item['imdb_score']

        if not (item.get('description') and item['description'].strip()):
            del item['description']

        if  (item.get('imdb_id')) == "":
            del item['imdb_id']

        if item.get('imdb_votes') != "":
            item['imdb_votes'] = float(item['imdb_votes'])
        else:
            del item['imdb_votes']

        if item.get('tmdb_score'):
            item['tmdb_score'] = float(item['tmdb_score'])
        else:
            del item['tmdb_score']

        if item.get('tmdb_popularity'):
            item['tmdb_popularity'] = float(item['tmdb_popularity'])
        else:
            del item['tmdb_popularity']

    except ValueError as ve:
        # Handle or log the error if conversion fails
        print(f"Data conversion error for item: {item}")
        print(ve)
        return None  # Return None to indicate failure

    return item


def custom_hash(title):
    title = str(title).lower()
    base = 257  # A prime base is chosen to help ensure a uniform distribution
    mod = 10 ** 9 + 9  # A large modulus helps prevent overflow
    hash_value = 0
    for char in title:  # Normalize the input to lower case
        hash_value = (hash_value * base + ord(char)) % mod
    return int(hash_value % 2)  # Returns 0 or 1, for two shards


with open('../res/titles.json', 'r') as file:  # Update the path to your JSON file
    data = json.load(file)

connect_database()
for item in data:
    # print(item)
    processed_item = preprocess_data(item)
    if processed_item:  # Ensure the item is valid after preprocessing
        movie = Movie(**processed_item)
        insert_movie(movie)

print("Data insertion complete.")
