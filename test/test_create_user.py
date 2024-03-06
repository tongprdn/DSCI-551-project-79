import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.operations import create_user, get_database
from src.db.connection import connect_database


class TestInsertDocument(unittest.TestCase):

    def test_insert_document(self):
        connect_database()
        user_param = {
            "username": "john001",
            "password": "password",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "token": "test",
            "admin_status": 0
        }

        inserted_id = create_user(**user_param).id
        print(inserted_id)
        # Verify that the document exists in the collection
        self.assertIsNotNone(inserted_id, msg="Insert Unsuccessfully")
        _, db = get_database()
        inserted_document = db['users'].find_one({"_id": inserted_id})
        self.assertEqual(inserted_document['username'], user_param['username'])
        if inserted_document['username'] == user_param['username']:
            print(f"\nSuccessfully inserted: {user_param['username']} to users collection")


if __name__ == '__main__':
    unittest.main()