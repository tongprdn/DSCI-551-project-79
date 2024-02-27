
# This is models.py inside db/
# Define your MongoDB models or schemas here if you're using a ODM like MongoEngine.

# Example schema using MongoEngine
from mongoengine import Document, StringField, IntField


class Movie(Document):
    title = StringField(required=True, max_length=200)
    year = IntField(required=True)
    # Add other fields/metadata as necessary
