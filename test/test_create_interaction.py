import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.operations import insert_interaction, get_database
from src.db.connection import connect_database
from src.db.models import UserInteraction


class TestInsertDocument(unittest.TestCase):

    def test_insert_document(self):

        _, db = get_database()
        random_user = db['users'].find_one({"username": "tongpr"})
        random_movie = db['movies'].find_one({"_id": "tm84618"})
        connect_database()
        print(random_movie)
        interaction = UserInteraction(
            user_id=random_user["_id"],
            movie_id=random_movie["_id"]
        )

        inserted_id = insert_interaction(interaction).id
        print(inserted_id)
        # Verify that the document exists in the collection
        self.assertIsNotNone(inserted_id, msg="Insert Unsuccessfully")
        inserted_document = db['user_interactions'].find_one({"_id": inserted_id})
        self.assertEqual(inserted_document['user_id'], interaction['user_id'].id)
        if inserted_document['user_id'] == interaction['user_id'].id:
            print(f"\nSuccessfully inserted: {inserted_document['_id']} to collection")


if __name__ == '__main__':
    unittest.main()
