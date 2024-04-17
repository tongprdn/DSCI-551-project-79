import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import connect_database
from src.db.models import Movie
from src.db.operations import insert_movie, preprocess_json_item


with open('../res/titles.json', 'r') as file:  # Update the path to your JSON file
    data = json.load(file)

connect_database()
# for item in data:
#     processed_item = preprocess_movie(item)
#     movie = Movie(**processed_item)
#     insert_movie(movie)
for item in data:
    movie = preprocess_json_item(item, Movie)
    insert_movie(movie)


print("Data insertion complete.")
