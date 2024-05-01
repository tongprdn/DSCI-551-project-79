# Final Project - Team 79

<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DSCI 551 - Final Project</h3>

  <p align="center">
    Team #79 - Spring 2024
    <br />
    <a href=""><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="">View Demo</a>
    ·
    <a href="">Report Bug</a>
    ·
    <a href="">Request Feature</a>
  </p>
</div>

### Folder Structure
- src Folder: The source code folder! However, in languages that use headers (or if you have a framework for your application) don’t put those files in here
- test Folder: Unit tests, integration tests… go here
- .config Folder: It should local configuration related to setup on local machine
- build Folder: This folder should contain all scripts related to build process (PowerShell, Docker compose…)
- dep Folder: This is the directory where all your dependencies should be stored
- doc Folder: The documentation folder
- res Folder: For all static resources in your project. For example, images
- samples Folder: Providing “Hello World” & Co code that supports the documentation
- tools Folder: Convenience directory for your use. Should contain scripts to automate tasks in the project, for example, build scripts, rename scripts. Usually contains .sh, .cmd files for example


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ACKNOWLEDGMENTS -->
## Online Documentation

Use this space to list online documentations needed in this project

* [Google Drive](https://drive.google.com/drive/u/0/folders/1p96bKQpGfEkJU8u73eAg4Mwy787ojNMP)
* [Project Proposal](https://docs.google.com/document/d/1rSKMuVN15UCtYD5BoVMNZgrb_VtyGrW0GbE4PmHNac0/edit?usp=sharing)
* [Progression Report](https://docs.google.com/document/d/1KXXet0OK6BldWUDonNF7j6mLJ_OmFQige_xx4EZLFTQ/edit#heading=h.14yodgbfx7y8)
* [Demo Presentation](https://docs.google.com/presentation/d/1Du0f4_SO0B37q01UTuK1pHd8LOc6M_KUy8gqVuJKlHY/edit?usp=sharing)
* [Final Report]()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to start all MondoDB Instances

### Config Server
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
 <p align="right">(<a href="#readme-top">back to top</a>)</p>

### Shard 1
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
 <p align="right">(<a href="#readme-top">back to top</a>)</p>

### Shard 2
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
 <p align="right">(<a href="#readme-top">back to top</a>)</p>

### Mongos
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
 <p align="right">(<a href="#readme-top">back to top</a>)</p>

## Shard Configuration
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

## Shard Distribution Checking  
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



## Troubleshooting
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
      
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template!

Use the `BLANK_README.md` to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
