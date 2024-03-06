import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.operations import insert_document
from src.db.connection import get_database
from src.db.config import MONGO_CONNECTION_STRING, DATABASE_NAME


class TestInsertDocument(unittest.TestCase):
    db = None
    client = None


    @classmethod
    def setUpClass(cls):

        try:
            cls.client, cls.db = get_database(MONGO_CONNECTION_STRING, DATABASE_NAME)
            cls.assertIsNotNone(cls.db, "Failed to connect to the database.")
            cls.client.server_info()  # Force a call to check if connected to server
            print("Connected to the database successfully!")
        except Exception as e:
            cls.fail(cls, f"Connection to MongoDB failed: {e}")

    def test_insert_document(self):
        # Assuming that the 'persons' collection and document data are the same as in the second screenshot
        collection_name = 'users'
        document = {
            "username": "tongpr",
            "password": "12345678",
            "first_name": "Pooridon",
            "last_name": "Rattanapairote",
            "email": "tong28206@gmail.com",
            "token": "aaaaaaaa"
        }

        # Insert document and get the inserted ID
        inserted_id = insert_document(self.db, collection_name, document)

        # Verify that the document exists in the collection
        inserted_document = self.db[collection_name].find_one({"_id": inserted_id})
        self.assertIsNotNone(inserted_document)
        self.assertEqual(inserted_document['username'], document['username'])
        if inserted_document['username'] == document['username']:
            print(f"\nSuccessfully inserted: {document['username']} to {collection_name} collection")
    @classmethod
    def tearDownClass(cls):
        # Clean up operations after all tests have run
        cls.client.close()


if __name__ == '__main__':
    unittest.main()
