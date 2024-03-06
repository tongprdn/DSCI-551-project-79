## Code Scope
Project: Develop a scalable movie database with user interaction capabilities

### Objectives:

- Design and implement a MongoDB database to store movie, user, and user interaction data.
- Utilize MongoDB sharding on EC2 Ubuntu instances for horizontal scalability and fault tolerance.
- Build two web applications:
   - Admin application: Provides CRUD (Create, Read, Update, Delete) functionality for managing movie data.
   - User application: Enables users to search and explore movie information, with functionalities such as liking, disliking, marking as watched, and clicking to view content. These interactions will be stored in the database for further analysis.

### Technical Specifications:

Database: MongoDB
Hosting platform: EC2 Ubuntu instances
MongoDB sharding:
2 shard servers (3 replicas each)
1 config server (3 replicas)
1 mongos server for application access
Database collections:
- movies
- users
- user_interactions

Deliverables:
- Functional MongoDB database with sharding
- Two fully operational web applications (admin and user)

Success Criteria:
- Database successfully stores and retrieves movie, user, and user interaction data.
- Admin application facilitates data management tasks.
- User application allows users to search, interact with, and view movie information.

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
