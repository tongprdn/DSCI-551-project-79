## Code requirement
1. Deployment of four instances of MongoDB Atlas, with two dedicated to sharding and two to replication processes.
2. Each database instance shall comprise four collections named: 'movies', 'person', 'users', and 'user_interactions'.
3. Provision of an additional MongoDB Atlas instance to function as a metadata repository, analogous to the NameNode in Hadoop, which will manage the storage locations of data.
4. Development of two web applications:
   - An end-user application that provides functionality for searching, querying, and interacting with the database, including features to like, dislike, and view details. This application will perform read operations from the database for search and filter actions, and write operations for user interactions.
   - An administrative application with a simple interface that allows for the addition, deletion, and editing of database content.
## project_root/
### db/
    ├── __init__.py
    └── connection.py    
    └── utils.py
    └── models.py
    └── name_node.py
### admin_app/
    ├── __init__.py
    └── main.py    
    └── utils.py
### user_app/
    ├── __init__.py
    └── main.py    
    └── utils.py
### common/
    ├── __init__.py
    └── helpers.py

### db/ Directory: 
Contains all database-related operations, including connection setup, schema definitions, and interactions with the NameNode-like MongoDB Atlas instance for data location management.
- connection.py: Establishes connections to MongoDB Atlas clusters and handles the logic for choosing the right shard/replica based on the operation or query.
- models.py: Defines the schema for your collections (movies, person, users, user_interactions) using a library like pymongo or an ODM (Object-Document Mapper) like mongoengine.
- name_node.py: Manages the logic for storing and retrieving the location of data, mimicking a NameNode's functionality in a Hadoop environment. This could involve mapping document IDs or key ranges to specific database instances.

### admin_app/ Directory: 
Contains the code for the admin web application. This application facilitates database management tasks such as adding, deleting, and editing data.
- main.py: The entry point for the admin app, setting up the web server and routing.
- utils.py: Utility functions specifically for the admin app, like form processing or validation logic.

### user_app/ Directory: 
Contains the code for the end-user web application. This application allows users to search, query, and interact with the data.
- main.py: The entry point for the user app, including web server setup, routing, and integration with the db module for data retrieval and updates.
- utils.py: Utility functions for the user app, such as search query processing or user interaction logging.

### common/ Directory: 
Shared utilities and helper functions that are common across both web applications and the database operations.
- helpers.py: Common utility functions, such as connection string parsing, logging setup, or shared validation functions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>