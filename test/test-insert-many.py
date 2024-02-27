import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint


uri = "mongodb+srv://tongpr:Pooridon28206@dsci551-1.ffpvw6g.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['netflix_data']
movies_collection = db['movies']
persons_collection = db['person']


director_id = persons_collection.insert_one({"name": "Christopher Nolan", "role": ["Director"], "bio": "British-American film director..."}).inserted_id
cast_ids = [
    persons_collection.insert_one({"name": "Leonardo DiCaprio", "role": ["Actor"], "bio": "..."}).inserted_id,
    persons_collection.insert_one({"name": "Ellen Page", "role": ["Actor"], "bio": "..."}).inserted_id,
]

movie_data = {
    "title": "Inception",
    "director": director_id,
    "cast": cast_ids,
    "genres": ["Action", "Sci-Fi", "Thriller"],
    "year_release": 2010,
    "description": "A thief who steals corporate secrets through dream-sharing technology is tasked with planting an "
                   "idea into the mind of a CEO.",
    "age_restriction": "PG-13",
    "rating": 8.8,
    "votes": 2500000,
    "production_country": ["US"]
}

movie_id = movies_collection.insert_one(movie_data).inserted_id

last_10_movies = movies_collection.find({}).sort("_id", pymongo.DESCENDING).limit(5)
for movie in last_10_movies:
    pprint(movie)