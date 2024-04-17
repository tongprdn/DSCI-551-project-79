# This is models.py inside db/
# Define your MongoDB models or schemas here if you're using a ODM like MongoEngine.

from mongoengine import Document, StringField, IntField, ListField, ReferenceField, DateTimeField, BooleanField, \
    FloatField
from mongoengine.base.fields import ComplexBaseField
import datetime


class BaseDocument(Document):
    meta = {'abstract': True}  # This makes it so this class isn't used to create a MongoDB collection

    def to_dict(self):
        data = {}
        for field_name, field in self._fields.items():
            value = self[field_name]

            # Handle ReferenceFields (and potentially other complex fields)
            if isinstance(field, ReferenceField):
                if value:
                    # Serialize ReferenceField to just the ID
                    data[field_name] = str(value.id)
                else:
                    # If the ReferenceField is None
                    data[field_name] = None
            else:
                # Handle all other fields normally
                data[field_name] = value

        # Add the 'id' field
        data['id'] = str(self.pk)
        return data


class Movie(BaseDocument):
    """
    Schema definition for a Movie within the application.
    """
    _id = StringField(required=True, primary_key=True)
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
    title_hash = IntField()

    meta = {
        'collection': 'movies',
        'shard_key': ('title_hash',)
    }


class Credit(BaseDocument):
    """
    Schema definition for a Credit within the application, linking actors and directors to movies.
    """
    movie_id = ReferenceField(Movie, required=True)
    person_id = StringField(required=True)
    name = StringField(required=True)
    character = StringField()
    role = StringField(required=True, choices=('ACTOR', 'DIRECTOR'))

    meta = {
        'collection': 'credits',
        'indexes': [
            {'fields': ('movie_id', 'person_id', 'role', 'character'), 'unique': True}
        ]
    }

    # def save(self, *args, **kwargs):
    #     if not self._created:  # A flag to check if this document has been saved before
    #         self._id = {'movie_id': self.movie_id, 'person_id': self.person_id}
    #     super().save(*args, **kwargs)


class User(BaseDocument):
    """
    Schema definition for a User within the application.

    Attributes:
        username (str): Unique username for the user account.
        password (str): Password for the user account.
        email (str): Unique email address for the user account.
        admin_status (int): Indicates whether the user has admin privileges (0 for no, 1 for yes).
        createAt (datetime): The timestamp when the user account was created.
    """
    username = StringField(required=True, unique=True, max_length=50)
    password = StringField(required=True)
    email = StringField(required=True, unique=True, max_length=100)
    admin_status = IntField(default=0)
    createAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'users'}


class UserInteraction(BaseDocument):
    user_id = ReferenceField('User', required=True)
    movie_id = ReferenceField('Movie', required=True)
    liked = BooleanField(default=False)
    liked_on = DateTimeField()  # time when clicked turn true

    meta = {
        'collection': 'user_interactions',
        'indexes': [
            {
                'fields': ['user_id', 'movie_id'],
                'unique': True
            }
        ]
    }

    def save(self, *args, **kwargs):
        if not self.liked_on and self.liked:
            self.liked_on = datetime.datetime.utcnow()
        return super(UserInteraction, self).save(*args, **kwargs)

