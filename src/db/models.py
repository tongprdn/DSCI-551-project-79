# This is models.py inside db/
# Define your MongoDB models or schemas here if you're using a ODM like MongoEngine.

from mongoengine import Document, StringField, IntField, ListField, ReferenceField, DateTimeField, BooleanField, \
    FloatField
import datetime


class Movie(Document):
    """
    Schema definition for a Movie within the application.
    """
    id = StringField(required=True, primary_key=True)
    title = StringField(required=True)
    type = StringField(required=True)
    description = StringField()
    release_year = IntField()
    age_certification = StringField()
    runtime = IntField()
    genres = ListField(StringField())
    production_countries = ListField(StringField())
    seasons = IntField()
    imdb_id = StringField()
    imdb_score = FloatField()
    imdb_votes = IntField()
    tmdb_popularity = FloatField()
    tmdb_score = FloatField()

    meta = {'collection': 'movies'}


class Credit(Document):
    """
    Schema definition for a Credit within the application, linking actors and directors to movies.
    """
    person_id = StringField(required=True)
    movie_id = ReferenceField(Movie, required=True)
    name = StringField(required=True)
    character = StringField()
    role = StringField(required=True, choices=('ACTOR', 'DIRECTOR'))

    meta = {'collection': 'credits'}


class User(Document):
    """
    Schema definition for a User within the application.

    Attributes:
        username (str): Unique username for the user account.
        password (str): Password for the user account.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): Unique email address for the user account.
        token (str): Authentication token for the user's session.
        admin_status (int): Indicates whether the user has admin privileges (0 for no, 1 for yes).
        createAt (datetime): The timestamp when the user account was created.
    """
    username = StringField(required=True, unique=True, max_length=50)
    password = StringField(required=True, max_length=50)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    email = StringField(required=True, unique=True, max_length=100)
    token = StringField(unique=True, max_length=50)
    admin_status = IntField(default=0)
    createAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'users'}


class UserInteraction(Document):
    user = ReferenceField('User', required=True)
    movie = ReferenceField('Movie', required=True)
    watched = BooleanField(default=False)
    liked = BooleanField(default=False)
    disliked = BooleanField(default=False)
    clicked = BooleanField(default=True)
    clicked_on = DateTimeField()  # time when clicked turn true

    meta = {
        'collection': 'user_interactions',
        'indexes': [
            {
                'fields': ['user', 'movie'],
                'unique': True
            }
        ]
    }

    def save(self, *args, **kwargs):
        if not self.clicked_on and self.clicked:
            self.clicked_on = datetime.datetime.utcnow()
        return super(UserInteraction, self).save(*args, **kwargs)

