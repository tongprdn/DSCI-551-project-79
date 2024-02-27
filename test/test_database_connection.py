import unittest
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.db.connection import get_database


class TestDatabaseConnection(unittest.TestCase):
    def test_connection(self):
        """
        Test the connection to the MongoDB database.
        """
        # Replace with your actual connection string and database name
        connection_string = "mongodb+srv://tongpr:Pooridon28206@dsci551-1.ffpvw6g.mongodb.net/?retryWrites=true&w=majority"
        db_name = "netflix_data"

        try:
            db = get_database(connection_string, db_name)
            self.assertIsNotNone(db, "Failed to connect to the database.")
            print("Connected to the database successfully!")
        except Exception as e:
            self.fail(f"Connection to MongoDB failed: {e}")


if __name__ == '__main__':
    unittest.main()
