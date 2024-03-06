from pymongo import MongoClient
import subprocess
import re
from pymongo import MongoClient, errors
from .config import MONGO_CONNECTION_STRING, DATABASE_NAME
from mongoengine import connect


def get_database(connection_string=MONGO_CONNECTION_STRING, db_name=DATABASE_NAME):
    """
    Create a connection to a MongoDB Atlas database and return the database object.

    Args:
        connection_string (str): The connection URI provided by MongoDB Atlas.
        db_name (str): The name of the database to connect to.

    Returns:
        Database: The database object if the connection is successful.

    Raises:
        ConnectionFailure: If the client cannot connect to MongoDB.
        ConfigurationError: If the URI is incorrect or misconfigured.
        OperationFailure: If the operation fails, e.g., due to wrong credentials.
    """
    try:
        client = MongoClient(connection_string)
        client.admin.command('ismaster')  # The "ismaster" command is cheap and does not require auth.
        database = client[db_name]
        return client, database

    except errors.ConnectionFailure as e:
        print(f"Connection to MongoDB failed: {e}")
        raise

    except errors.ConfigurationError as e:
        print(f"Configuration Error: {e}")
        raise

    except errors.OperationFailure as e:
        print(f"Operation Failure: {e}")
        raise


def connect_database():
    connect(db=DATABASE_NAME, host=MONGO_CONNECTION_STRING)


def check_server_latency(uri):
    """
    Check the latency to a MongoDB server.

    Args:
    uri (str): The MongoDB URI of the server to check.

    Returns:
    float: The latency to the server in seconds.

    # Example usage:
        latency = check_server_latency("mongodb://username:password@host:port/dbname")
        if latency is not None:
            print(f"Latency: {latency} ms")
        else:
            print("Failed to check server latency")
    """
    # Extract the host from the URI and ping it
    host = uri.split("@")[-1].split("/")[0].split(":")[0]

    # Ping the host and parse the output to find the latency
    try:
        output = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, text=True)
        # Look for a line that includes 'time=' and extract the value
        match = re.search(r"time=([\d.]+)", output.stdout)
        if match:
            return float(match.group(1))
        else:
            return None
    except Exception as e:
        print(f"Error pinging server: {e}")
        return None
