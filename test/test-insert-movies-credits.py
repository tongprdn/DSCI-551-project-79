import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.models import Movie, Credit
from src.db.connection import connect_database


def insert_sample_movie():
    # Create a sample movie
    movie = Movie(
        id="m123",
        title="Sample Movie",
        type="Movie",
        description="This is a sample movie.",
        release_year=2021,
        age_certification="PG-13",
        runtime=120,
        genres=["Drama", "Adventure"],
        production_countries=["USA"],
        seasons=1,
        imdb_id="tt1234567",
        imdb_score=7.5,
        imdb_votes=10000,
        tmdb_popularity=10.0,
        tmdb_score=8.0
    )
    movie.save()
    return movie


def insert_sample_credits(movie):
    # Create sample credits for the movie
    actor_credit = Credit(
        person_id="a123",
        movie_id=movie,
        name="Sample Actor",
        character="Main Character",
        role="ACTOR"
    )
    actor_credit.save()

    director_credit = Credit(
        person_id="d123",
        movie_id=movie,
        name="Sample Director",
        character="",
        role="DIRECTOR"
    )
    director_credit.save()


connect_database()
movie = insert_sample_movie()
insert_sample_credits(movie)
