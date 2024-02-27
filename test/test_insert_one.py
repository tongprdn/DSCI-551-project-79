import sys
import os
import unittest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.operations import insert_document
from src.db.connection import get_database


class TestInsertDocument(unittest.TestCase):
    db = None
    client = None


    @classmethod
    def setUpClass(cls):
        # Set up the MongoDB connection for the entire test class
        connection_string = "mongodb+srv://tongpr:Pooridon28206@dsci551-1.ffpvw6g.mongodb.net/?retryWrites=true&w=majority"
        db_name = "netflix_data"

        try:
            cls.client, cls.db = get_database(connection_string, db_name)
            cls.assertIsNotNone(cls.db, "Failed to connect to the database.")
            cls.client.server_info()  # Force a call to check if connected to server
            print("Connected to the database successfully!")
        except Exception as e:
            cls.fail(cls, f"Connection to MongoDB failed: {e}")

    def test_insert_document(self):
        # Assuming that the 'persons' collection and document data are the same as in the second screenshot
        collection_name = 'person'
        document = {
            "name": "Tony Ratta",
            "role": ["Director"],
            "bio": "Thai film director..."
        }

        # Insert document and get the inserted ID
        inserted_id = insert_document(self.db, collection_name, document)

        # Verify that the document exists in the collection
        inserted_document = self.db[collection_name].find_one({"_id": inserted_id})
        self.assertIsNotNone(inserted_document)
        self.assertEqual(inserted_document['name'], document['name'])

    @classmethod
    def tearDownClass(cls):
        # Clean up operations after all tests have run
        cls.client.close()


if __name__ == '__main__':
    unittest.main()
