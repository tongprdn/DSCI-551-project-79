import unittest
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import get_database
from src.db.config import MONGO_CONNECTION_STRING, DATABASE_NAME


class TestDatabaseConnection(unittest.TestCase):
    def test_connection(self):
        """
        Test the connection to the MongoDB database.
        """

        try:
            db = get_database(MONGO_CONNECTION_STRING, DATABASE_NAME)
            self.assertIsNotNone(db, "Failed to connect to the database.")
            print("Connected to the database successfully!")
        except Exception as e:
            self.fail(f"Connection to MongoDB failed: {e}")


if __name__ == '__main__':
    unittest.main()
