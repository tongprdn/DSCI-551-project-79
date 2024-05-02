# Final Project Team 79

<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://upload.wikimedia.org/wikipedia/commons/9/94/USC_Trojans_logo.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DSCI 551 - Final Project</h3>

  <p align="center">
    Team #79 - Spring 2024
    <br />
    <a href="https://drive.google.com/drive/folders/1p96bKQpGfEkJU8u73eAg4Mwy787ojNMP?usp=sharing"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="">View Demo</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
## 📔 Table of Contents
- [About The Project](#about-the-project)
  - [Project Scope](#project-scope)
  - [Database Specifications](#database-specifications)
  - [Frontend Specification](#frontend-specifications)
  - [Built With](#-built-with)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Clone the repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
  - [Start MondoDB](#start-mondodb)
  - [Running Admin Application](#running-the-admin-application)
  - [Running User Application](#running-the-end-user-application)
- [Optional Command](#-optional-command)
  - [Troubleshooting](#troubleshooting-in-case-of-refused-connection)
- [Online Documentation](#-online-documentation)
- [Roadmap](#-roadmap)
- [Contact](#-contact)





<!-- ABOUT THE PROJECT -->
## About The Project


This project is a part of the final project in the University of Southern California for the course DSCI 551 - Foundations of Data Management. It is designed to create a scalable movie database with user interaction capabilities that solve real-world problems and improve user engagement with movie content.

#### Project Scope
* Objective: To design and implement a robust MongoDB database that facilitates efficient storage and management of movie data along with user interactions.

#### Key Features:

* Admin Application: A web-based interface that provides CRUD (Create, Read, Update, Delete) functionality for managing movie data.
* User Application: Allows users to search, explore, and interact with movie information. Features include liking, disliking, marking movies as watched, and more. These interactions are stored for further data analysis to enhance recommendations and user experience.

#### Database Specifications
* Database System: MongoDB hosted on EC2 Ubuntu instances.
* MongoDB Sharding: Implemented for horizontal scalability and fault tolerance.
  * 2 Shard Servers: Each with 3 replicas.
  * 1 Config Server: With 3 replicas.
  * 1 Mongos Server: For application access.
* Collections: Movies, Users, User Interactions.

#### Frontend Specifications
* Technologies Used: HTML, CSS, JavaScript, Flask.
* Hosting Platform: GitHub.
* Key Pages:
  * Home Page: Features search and movie recommendations.
  * Recommendation Page: Dynamically suggests movies based on user interactions.
  * Catalog Page: Extensive list of movies with filtering options.

<p align="right">(<a href="#final-project-team-79">back to top</a>)</p>



### ⚙️ Built With

* [![Mongo][mongo.js]][mongo-url]
* [![flask][flask.js]][flask-url]
* [![Javascript][javascript.js]][javascript-url]
* [![Html][html.js]][html-url]
* [![Css][css.js]][css-url]
* [![AWS][aws.js]][aws-url]

<p align="right">(<a href="#final-project-team-79">back to top</a>)</p>

<!-- PROJECT STRUCTURE -->
## 🏗️ Project Structure

This project is organized into several directories and files structured as follows:

- `.github/`
  - Various files for github usage.
- `dep/`
  - `requirements.txt` - List of dependencies for the project.
- `doc/`
  - Various documentation files and proposals related to the project.
- `res/`
  - Resource files like CSVs and JSON documents used in the project.
- `src/`
  - Source code for the project including the two main applications:
    - `admin_app/` - Administrative web application.
      - `static/` - Static files like CSS and JavaScript for the admin app.
      - `templates/` - HTML templates for rendering admin app views.
      - `__init__.py`, `config.py`, `forms.py`, `views.py` - Python modules for Flask app configuration, form definitions, and view functions.
    - `db/`
      - `connection.py` - Database connection configurations.
      - `models.py` - Definitions of MongoDB models.
      - `operations.py` - Database operations such as insert and update functions.
    - `user_app/` - User-facing web application.
      - `static/`, `templates/`, similar structure to `admin_app`.
      - `__init__.py`, `config.py`, `views.py` - Python modules specific to the user app.
- `test/`
  - Python scripts for testing various components of the applications.
- `README.md` - Overview and general information about the project.
- `LICENSE` - The license under which the project is released.
- `.gitignore`, `.editorconfig`, `.gitattributes`, `VERSIONING.md` - Configuration files for git, editor settings, attribute specifications, and versioning guidelines.

<p align="right">(<a href="#final-project-team-79">back to top</a>)</p>

<!-- GETTING STARTED -->
## ✅ Getting Started

<!-- CLONE THE REPOSITORY -->
### Clone the repository

```bash
   git clone https://github.com/tongprdn/DSCI-551-project-79.git
   cd yourrepositoryname
```

<!-- INSTALL DEPENDENCIES -->
### Install Dependencies
Navigate to the root directory of the project and run:
```bash
   pip install -r dep/requirements.txt
```

<!-- START MONGODB -->
### Start MondoDB

#### EC2 Private Key
* EC2 key is contains in 
```path
    /res/dsci551-team79.pem
```
* Copy this to where you want to run shell command

#### Config Server
1. Connect to EC2
    ```sh
    ssh -i "dsci551-team79.pem" ubuntu@ec2-54-193-107-112.us-west-1.compute.amazonaws.com
    ```
2. Start mongoDB replica set for config server
    ```sh
    nohup mongod --configsvr  --port 28041 --bind_ip localhost,ec2-54-193-107-112.us-west-1.compute.amazonaws.com --replSet config_repl --dbpath shard-demo/configsrv &
		
    nohup mongod --configsvr  --port 28042 --bind_ip localhost,ec2-54-193-107-112.us-west-1.compute.amazonaws.com --replSet config_repl --dbpath shard-demo/configsrv1 &
   
   nohup mongod --configsvr  --port 28043 --bind_ip localhost,ec2-54-193-107-112.us-west-1.compute.amazonaws.com --replSet config_repl --dbpath shard-demo/configsrv2 &
    ```
3. Connect to one of the replica set node 
    ```sh
    mongosh --host 54.193.107.112  --port 28041
    ```
4. Check replica set status
    ```sh
    rs.status()
    ```
 <p align="right">(<a href="#final-project-team-79">back to top</a>)</p>

#### Shard 1
1. Connect to EC2
    ```sh
    ssh -i "dsci551-team79.pem" ubuntu@ec2-18-144-138-11.us-west-1.compute.amazonaws.com
    ```
2. Start mongoDB replica set for the shard
    ```sh
    nohup mongod --shardsvr --port 28081 --bind_ip localhost,ec2-18-144-138-11.us-west-1.compute.amazonaws.com --replSet shard_repl --dbpath shard-demo/shardrep1 &
		
			nohup mongod --shardsvr --port 28082 --bind_ip localhost,ec2-18-144-138-11.us-west-1.compute.amazonaws.com --replSet shard_repl --dbpath shard-demo/shardrep2 &
			
			nohup mongod --shardsvr --port 28083 --bind_ip localhost,ec2-18-144-138-11.us-west-1.compute.amazonaws.com --replSet shard_repl --dbpath shard-demo/shardrep3 &
    ```
3. Connect to one of the replica set node 
    ```sh
    mongosh --host 18.144.138.11  --port 28081
    ```
4. Check replica set status
    ```sh
    rs.status()
    ```
 <p align="right">(<a href="#final-project-team-79">back to top</a>)</p>

#### Shard 2
1. Connect to EC2
    ```sh
    ssh -i "dsci551-team79.pem" ubuntu@ec2-50-18-187-166.us-west-1.compute.amazonaws.com
    ```
2. Start mongoDB replica set for the shard
    ```sh
    nohup mongod --shardsvr --port 29081 --bind_ip localhost,ec2-50-18-187-166.us-west-1.compute.amazonaws.com --replSet shard2_repl --dbpath shard-demo/shard2rep1 &
		
			nohup mongod --shardsvr --port 29082 --bind_ip localhost,ec2-50-18-187-166.us-west-1.compute.amazonaws.com --replSet shard2_repl --dbpath shard-demo/shard2rep2 &
			
			nohup mongod --shardsvr --port 29083 --bind_ip localhost,ec2-50-18-187-166.us-west-1.compute.amazonaws.com --replSet shard2_repl --dbpath shard-demo/shard2rep3 &
    ```
3. Connect to one of the replica set node 
    ```sh
    mongosh --host 50.18.187.166  --port 29081
    ```
4. Check replica set status
    ```sh
    rs.status()
    ```
 <p align="right">(<a href="#final-project-team-79">back to top</a>)</p>

#### Mongos
1. Connect to EC2
    ```sh
    ssh -i "dsci551-team79.pem" ubuntu@ec2-13-57-137-224.us-west-1.compute.amazonaws.com
    ```
2. Start mongos service, connecting to the config server
    ```sh
    nohup mongos --configdb config_repl/ec2-54-193-107-112.us-west-1.compute.amazonaws.com:28041,ec2-54-193-107-112.us-west-1.compute.amazonaws.com:28042,ec2-54-193-107-112.us-west-1.compute.amazonaws.com:28043 --bind_ip localhost,ec2-13-57-137-224.us-west-1.compute.amazonaws.com &
    ```
3. Connect to mongos
    ```sh
    mongosh --host ec2-13-57-137-224.us-west-1.compute.amazonaws.com --port 27017
    ```
4. Check shard status
    ```sh
    sh.status()
    ```
 <p align="right">(<a href="#final-project-team-79">back to top</a>)</p>

<!-- RUNNING ADMIN APPLICATION -->
### Running the Admin Application
* Set Flask Environment Variables:
  * For a development environment, you can set the environment variables like so:
  <a href="https://ibb.co/SRH8wvs"><img src="https://i.ibb.co/4PCGRNm/Screenshot-2567-05-01-at-16-50-30.png" alt="Screenshot-2567-05-01-at-16-50-30" border="0"></a>
  ```bash
  export FLASK_APP=src/admin_app
  export FLASK_ENV=development
  ```
* Run the Flask Application:
  * From the root of your project directory, execute:
  ```bash
    flask run
  ```
* 
    This will start the admin application on http://127.0.0.1:5000/.

<!-- RUNNING END-USER APPLICATION -->
### Running the End-User Application
* Set Flask Environment Variables:
  * For a development environment, you can set the environment variables like so:
  <a href="https://ibb.co/q0KpYv5"><img src="https://i.ibb.co/8zq9gHc/Screenshot-2567-05-01-at-16-51-22.png" alt="Screenshot-2567-05-01-at-16-51-22" border="0"></a>
  ```bash
  export FLASK_APP=src/user_app
  export FLASK_ENV=development
  ```
* Run the Flask Application:
  * From the root of your project directory, execute:
  ```bash
    flask run
  ```
* 
    This will start the admin application on http://127.0.0.1:5000/.

<!-- OPTIONAL COMMAND -->
## ⌥ Optional Command

### Shard Distribution (For Checking)  
- Database sharding status
   ```sh
    db.printShardingStatus()
   ```
- Balancer State
   ```sh
    sh.getBalancerState()
   ```
- Collection shard distribution
   ```sh
    db.movies.getShardDistribution()
   ```
  
### Shard Configuration (Don't need to run again)
- Enable Sharding
   ```sh
    sh.enableSharding("netflix_data")
   ```
- Create index
   ```sh
   use netflix_data
   db.movies.createIndex({"title_hash": 1})
   ```
- Shard Collection
   ```sh
    sh.shardCollection("netflix_data.movies", {"title_hash": 1})
   ```
- Shard Collection
   ```sh
    sh.splitAt('netflix_data.movies', {'title_hash': 1})
   ```
- Move Chunk
   ```sh
    sh.moveChunk(
	  "netflix_data.movies",
	  { "title_hash": 1 },  // Lower bound of the shard key range for the chunk
	  "shard2_repl"         // Target shard where you want to move the chunk
	)
   ```


<!-- TROUBLESHOOTING -->
### Troubleshooting (In case of refused connection)
- Check MongoDB process
   ```sh
    ps -aef  | grep "mongo"
   ```
  or check TCP running
   ```sh
    sudo lsof -iTCP -sTCP:LISTEN -n -P
   ```
- Delete socket file (to fix permission issue)
   ```sh
    sudo rm -r /tmp/mongodb-*.sock
   ```
- Check MongoDB connection log
   ```sh
    cat ~/.mongodb/mongosh/<LogID>_log
   ```
- Forcing primary on replica set
   ```sh
    cfg = rs.conf()
   cfg.members[0].priority = 1
   cfg.members[1].priority = 0.5
   cfg.members[2].priority = 0.5
   rs.reconfig(cfg) 
   ```
  if it's not working, use "force"
  ```sh
  rs.reconfig(cfg, {force:true})
   ```
      
  
<p align="right">(<a href="#final-project-team-79">back to top</a>)</p>

<!-- ONLINE DOCUMENTATION -->
## 📚 Online Documentation

List of online documentations needed in this project

* [Google Drive](https://drive.google.com/drive/u/0/folders/1p96bKQpGfEkJU8u73eAg4Mwy787ojNMP)
* [Project Proposal](https://docs.google.com/document/d/1rSKMuVN15UCtYD5BoVMNZgrb_VtyGrW0GbE4PmHNac0/edit?usp=sharing)
* [Progression Report](https://docs.google.com/document/d/1KXXet0OK6BldWUDonNF7j6mLJ_OmFQige_xx4EZLFTQ/edit#heading=h.14yodgbfx7y8)
* [Demo Presentation](https://docs.google.com/presentation/d/1Du0f4_SO0B37q01UTuK1pHd8LOc6M_KUy8gqVuJKlHY/edit?usp=sharing)
* [Final Report](https://docs.google.com/document/d/1SaELOd2xxvorXVx_5k9DLIc-z-BvJazkcU_zMrAllh8/edit?usp=sharing)

<p align="right">(<a href="#final-project-team-79">back to top</a>)</p>


<!-- ROADMAP -->
## 🗺️ Roadmap

- [x] Add Security Group
- [x] Super Admin control
- [x] Add favorite function
- [x] Add bulk operation
    - [x] Bulk insertion
    - [x] Bulk deletion

<p align="right">(<a href="#final-project-team-79">back to top</a>)</p>


<!-- CONTACT -->
## ☎️ Contact

* Pooridon Rattanapairote - prattana@usc.edu
* Pannawat Chauychoo - pchauych@usc.edu


Project Link: [https://github.com/tongprdn/DSCI-551-project-79/](https://github.com/tongprdn/DSCI-551-project-79/)

<p align="right">(<a href="#final-project-team-79">back to top</a>)</p>






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[flask.js]: https://img.shields.io/badge/Flask-FFFFFF?style=for-the-badge&logo=flask&logoColor=55F0E9
[flask-url]: https://flask.palletsprojects.com/
[mongo.js]: https://img.shields.io/badge/MongoDB-0B0947?style=for-the-badge&logo=mongodb&logoColor=89FF6F
[mongo-url]: https://www.mongodb.com/
[javascript.js]: https://img.shields.io/badge/JavaScript-F7DB16?style=for-the-badge&logo=javascript&logoColor=000000
[javascript-url]: https://www.javascript.com/
[aws.js]: https://img.shields.io/badge/Amazon%20AWS-000000?style=for-the-badge&logo=amazonaws&logoColor=FF9900
[aws-url]: https://aws.amazon.com/
[html.js]: https://img.shields.io/badge/HTML5-FFFFFF?style=for-the-badge&logo=html5&logoColor=26418B
[html-url]: https://www.w3.org/html/
[css.js]: https://img.shields.io/badge/CSS3-FFFFFF?style=for-the-badge&logo=html5&logoColor=26418B
[css-url]: https://www.w3.org/Style/CSS/Overview.en.html
