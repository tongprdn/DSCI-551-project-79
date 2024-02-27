from .connection import get_database


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
