from .connection import get_database
from .models import User, Movie, UserInteraction, Credit
from mongoengine.errors import NotUniqueError
import datetime
from mongoengine import ValidationError
from werkzeug.security import check_password_hash
from mongoengine.queryset.visitor import Q


def insert_document(db, collection_name, document):
    """
    Insert a document into a MongoDB collection.

    :param db: The database object
    :param collection_name: The name of the collection to insert the document into.
    :param document: A dictionary representing the document to insert.
    :return: The ID of the inserted document.
    """
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id


def insert_movie(*args, **kwargs):
    """
    Insert a new movie into the database.

    This function can be used in two ways:
    1. Pass a Movie object directly as the argument.
    2. Pass individual movie attributes as keyword arguments.

    :param args: Movie instance (optional)
    :param kwargs: Individual movie attributes (optional)
    :return: The Movie document that was inserted.
    :raises ValidationError: If there are issues with the data provided.
    """
    if args and isinstance(args[0], Movie):
        # A Movie instance is provided
        movie = args[0]
    else:
        # Individual movie attributes are provided
        movie = Movie(**kwargs)
    try:
        # Data validation before saving
        movie.validate()
        # Insert the movie into the database
        movie.save()
    except ValidationError as e:
        print(f"====DATA IS INVALID====")
        raise e
    except NotUniqueError as e:
        print(f"====MOVIE IS ALREADY EXISTED====")
        raise e
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
        # Ensure password hashing and other preprocessing as needed here
        new_user.createAt = datetime.datetime.utcnow()

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


def insert_interaction(*args, **kwargs):
    """
    Insert a new interaction into the 'user_interactions' collection.

    This function can be used in two ways:
    1. Pass a UserInteraction object directly as the argument.
    2. Pass individual interaction attributes as keyword arguments.

    :param args: UserInteraction instance (optional).
    :param kwargs: Individual interaction attributes (optional).

    :return: The UserInteraction document that was inserted or an error message.
    """
    if args and isinstance(args[0], UserInteraction):
        interaction = args[0]
    else:
        interaction = UserInteraction(**kwargs)

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
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


from mongoengine.queryset.visitor import Q


def list_documents(collection, limit=10, sort='id', filter_by=None, order_by=None):
    """
    List documents from the specified MongoDB collection.

    Args:
        collection (str): The name of the collection to list documents from.
        limit (int): The maximum number of documents to return.
        sort (str): The field to sort the documents by.
        filter_by (dict): A dictionary for filtering results.
        order_by (str): Field name to order by.

    Returns:
        A list of documents from the collection.
    """
    model = get_model(collection)
    if not model:
        return []

    query = model.objects()
    if filter_by:
        query = query.filter(**filter_by)
    if order_by:
        query = query.order_by(order_by)
    else:
        query = query.order_by(sort)

    return query[:limit].as_pymongo()


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
