from bson import ObjectId

from .connection import get_database
from .models import User, Movie, UserInteraction, Credit
from mongoengine.errors import NotUniqueError
import datetime
from mongoengine import ValidationError, Document, DoesNotExist
from mongoengine.fields import StringField, IntField, FloatField, ListField
import bcrypt
import pymongo
import ast


def insert_movie(movie):
    """
    Insert a new movie into the database.

    This function can be used in two ways:
    1. Pass a Movie object directly as the argument.
    2. Pass individual movie attributes as keyword arguments.

    :param movie: Movie instance
    :return: The Movie document that was inserted.
    :raises ValidationError: If there are issues with the data provided.
    """
    if not isinstance(movie, Movie):
        raise Exception('The argument must be Movie Type')

    if movie.title_hash is None:
        movie.title_hash = custom_hash(title=movie.title)
    try:
        # Data validation before saving
        movie.validate()
        # Insert the movie into the database
        Movie.objects(_id=movie._id, title=movie.title, title_hash=movie.title_hash).update_one(
            upsert=True,
            set__title=movie.title,
            set__type=movie.type,
            set__description=movie.description,
            set__release_year=movie.release_year,
            set__age_certification=movie.age_certification,
            set__runtime=movie.runtime,
            set__genres=movie.genres,
            set__production_countries=movie.production_countries,
            set__seasons=movie.seasons,
            set__imdb_id=movie.imdb_id,
            set__imdb_score=movie.imdb_score,
            set__imdb_votes=movie.imdb_votes,
            set__tmdb_popularity=movie.tmdb_popularity,
            set__tmdb_score=movie.tmdb_score,
            set__title_hash=movie.title_hash  # Ensure this does not change if document exists
        )
    except ValidationError as e:
        print(f"====DATA IS INVALID====")
        raise e
    except NotUniqueError as e:
        print(f"====MOVIE IS ALREADY EXISTED====")
        raise e
    print(f"Insert {movie.title} successfully")
    return movie


def create_user(*args, **kwargs):
    """
    Create a new user in the 'users' collection of the MongoDB database.

    This function can be used in two ways:
    1. Pass a User object directly as the argument.
    2. Pass individual user attributes as keyword arguments.

    Args:
        *args: User instance (optional).
        **kwargs: Individual user attributes (optional).

    Returns:
        User: The User document that was inserted.

    Raises:
        ValidationError: If there are issues with the data provided.
        NotUniqueError: If a user with the same username or email already exists.
    """
    if args and isinstance(args[0], User):
        new_user = args[0]
    else:
        new_user = User(**kwargs)
        new_user.createAt = datetime.datetime.utcnow()

    new_user.password = hash_password(new_user.password)
    print("hash password:", new_user.password)

    try:
        # Validate and save the new user to the 'users' collection
        new_user.validate()
        new_user.save()
        return new_user
    except ValidationError as ve:
        print(f"Data validation error: {ve}")
        raise ve
    except NotUniqueError as nue:
        print(f"User with the username '{new_user.username}' or email '{new_user.email}' already exists.")
        raise nue


def insert_credit(credit):
    """
        Insert a new movie into the database.

        This function can be used in two ways:
        1. Pass a Movie object directly as the argument.
        2. Pass individual movie attributes as keyword arguments.

        :param credit: Credit instance
        :return: The Credit document that was inserted.
        :raises ValidationError: If there are issues with the data provided.
        """
    if not isinstance(credit, Credit):
        raise Exception('The argument must be Credit Type')
    try:
        movie_id = credit['movie_id']
        Movie.objects(_id=movie_id)  # Ensure movie_id_str is a string representation of ObjectId
    except DoesNotExist:
        print(f"No movie found with id {movie_id}")
        return
    except ValidationError as e:
        print(f"Validation error for movie ID: {e}")
        return
    try:
        # Data validation before saving
        credit.validate()
        # Insert the movie into the database
        credit.save()
    except ValidationError as e:
        print(f"====DATA IS INVALID====")
        raise e
    except NotUniqueError as e:
        print(f"====CREDIT IS ALREADY EXISTED====")
        raise e
    # print(f"Insert {credit['_id']} successfully")
    return credit


def insert_interaction(interaction):
    """
    Insert a new interaction into the 'user_interactions' collection.

    This function can be used in two ways:
    1. Pass a UserInteraction object directly as the argument.
    2. Pass individual interaction attributes as keyword arguments.

    :param interaction: UserInteraction instance

    :return: The UserInteraction document that was inserted or an error message.
    """
    if not isinstance(interaction, UserInteraction):
        raise Exception('The argument must be UserInteraction Type')
    try:
        movie_id = interaction['movie_id']
        Movie.objects(_id=movie_id)  # Ensure movie_id_str is a string representation of ObjectId
    except DoesNotExist:
        print(f"No movie found with id {movie_id}")
        return
    except ValidationError as e:
        print(f"Validation error for movie ID: {e}")
        return
    try:
        interaction.validate()
        interaction.save()
        return interaction
    except NotUniqueError as nue:
        print("An interaction with the given user and movie already exists.")
        raise nue
    except ValidationError as ve:
        print(f"Data validation error: {ve}")
        raise ve


def check_user_credentials(username, password):
    """
    Check if the user exists and the password is correct.

    Args:
        username (str): The username to check.
        password (str): The password to check.

    Returns:
        The User object if credentials are valid, None otherwise.
    """
    user = User.objects(username=username).first()
    if not user:
        return "User not found."
    else:
        if not check_password(password, user.password):
            return "Password Incorrect."
        else:
            return user


def list_documents(collection, limit=None, sort_field='title', sort_direction=pymongo.ASCENDING, filter_by=None,
                   filter_op=None, skip=None):
    """
    List documents from the specified MongoDB collection.

    Args:
        collection (str): The name of the collection to list documents from.
        limit (int): The maximum number of documents to return.
        sort_field (str): The field to sort the documents by.
        sort_direction (str): pymongo.ASCENDING or pymongo.DESCENDING
        filter_by (dict): A dictionary for filtering results.
        filter_op (str): A string to specify filtering operation.
        skip (int): A number of documents to skip.

    Returns:
        A list of documents from the collection.
    """
    model = get_model(collection)
    if not model:
        return []

    query = model.objects()
    if filter_by and filter_op:
        for field, value in filter_by.items():
            if filter_op == 'eq':
                query = query.filter(**{field: value})
            elif filter_op == 'ne':
                query = query.filter(**{f'{field}__ne': value})
            elif filter_op == 'contains':
                query = query.filter(**{f'{field}__contains': value})
            elif filter_op == 'gt':
                query = query.filter(**{f'{field}__gt': value})
            elif filter_op == 'lt':
                query = query.filter(**{f'{field}__lt': value})
            elif filter_op == 'gte':
                query = query.filter(**{f'{field}__gte': value})
            elif filter_op == 'lte':
                query = query.filter(**{f'{field}__lte': value})
    if sort_field:
        order = '+' if sort_direction == 1 else '-'
        query = query.order_by(f'{order}{sort_field}')
    if skip:
        query = query.skip(skip)
    if limit:
        query = query.limit(limit)
    documents = query.all()
    documents_dict_list = [doc.to_mongo().to_dict() for doc in documents]
    return documents_dict_list


def get_model(collection_name):
    """
    Get the model class based on the collection name.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        The model class if found, None otherwise.
    """
    # Assuming you have a way to map collection names to models
    # You would need to implement this mapping
    mapping = {
        'movies': Movie,
        'credits': Credit,
        'user_interactions': UserInteraction,
        'users': User
    }
    return mapping.get(collection_name)


def hash_password(plain_text_password):
    hashed = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_keys(collection):
    keys = []
    if collection == 'movies':
        keys = ['_id', 'title', 'type', 'description', 'release_year', 'age_certification', 'runtime', 'genres'
            , 'production_countries', 'seasons', 'imdb_id', 'imdb_score', 'imdb_votes', 'tmdb_popularity', 'tmdb_score']
    elif collection == 'credits':
        keys = ['person_id', 'movie_id', 'name', 'character', 'role']
    elif collection == 'users':
        keys = ['_id', "username", "password", "email", "admin_status", "createAt"]
    elif collection == 'user_interactions':
        keys = ['user_id', 'movie_id', 'liked', 'liked_on']
    return keys


def preprocess_json_item(item, document_cls):
    if not issubclass(document_cls, Document):
        raise ValueError("The document_cls must be a subclass of mongoengine.Document.")
    processed_item = {}
    for field_name, field in document_cls._fields.items():
        if field_name == '_id' and 'id' in item:
            processed_item[field_name] = item['id']
        elif field_name == '_id' and '_id' in item:
            processed_item[field_name] = item['_id']
        elif field_name in item:
            value = item[field_name]
            if value == '':
                continue
            if isinstance(field, StringField) and not isinstance(value, str):
                processed_item[field_name] = str(value)
            elif isinstance(field, IntField) and value != '':
                processed_item[field_name] = int(value)
            elif isinstance(field, FloatField) and value != '':
                processed_item[field_name] = float(value)
            elif isinstance(field, ListField) and isinstance(value, str):
                processed_item[field_name] = ast.literal_eval(value)
            else:
                processed_item[field_name] = value
        elif field.required:
            if field_name != '_id':
                raise ValueError(f"The required field '{field_name}' is missing from the input item.")
    print("Processed done:", processed_item)
    return document_cls(**processed_item)


def custom_hash(title):
    title = str(title).lower()
    base = 257
    mod = 10 ** 9 + 9
    hash_value = 0
    for char in title:
        hash_value = (hash_value * base + ord(char)) % mod
    return int(hash_value % 2)


def insert_one(collection_name, document):
    """
    Insert a document into a MongoDB collection.

    :param collection_name: The name of the collection to insert the document into.
    :param document: A dictionary representing the document to insert.
    :return: The ID of the inserted document.
    """
    if collection_name == 'movies':
        return insert_movie(document)
    elif collection_name == 'credits':
        return insert_credit(document)
    elif collection_name == 'users':
        return create_user(document)
    elif collection_name == 'user_interactions':
        return insert_interaction(document)
    else:
        raise Exception('Invalid collection name')


def delete_documents(collection_name, criteria):
    model = get_model(collection_name)
    print("Documents matching the filter:", model.objects(**criteria))
    return model.objects(**criteria).delete()


def get_item_by_id(collection_name, item_id):
    print('get_item_by_id', collection_name, item_id)
    try:
        model = get_model(collection_name)
        if collection_name == 'movies':
            item = model.objects.get(_id=item_id)
        else:
            item = model.objects.get(id=item_id)
        return item.to_dict()
    except (DoesNotExist, ValidationError) as e:
        raise Exception(e)


def update_one(collection_name, item_id, update_data):
    """
    Update a document in a collection.

    :param collection_name: The name of the collection
    :param item_id: The ID of the document to update
    :param update_data: A dictionary of updates to apply
    :return: The updated document or None if not found
    """
    model = get_model(collection_name)
    if not model:
        raise ValueError("No model found for collection: {}".format(collection_name))

    try:
        if collection_name == 'movies':
            document = model.objects.get(_id=item_id)
        else:
            document = model.objects.get(id=item_id)

        for field_name, value in update_data.items():
            if hasattr(document, field_name):
                if field_name == 'liked':
                    value = value in ['true', 'True', 1]
                if field_name == 'password':
                    value = hash_password(value)
                if field_name == 'movie_id':
                    try:
                        value = Movie.objects.get(_id=value)
                    except Exception as e:
                        raise Exception(e)
                elif field_name == 'user_id':
                    try:
                        value = User.objects.get(id=value)
                    except Exception as e:
                        raise Exception(e)
                setattr(document, field_name, value)

        # Save the changes to the database
        document.save()
        return document
    except DoesNotExist:
        return None  # Or you can raise an exception as per your use case
