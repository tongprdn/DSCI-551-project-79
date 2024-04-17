<!-- ACKNOWLEDGMENTS -->
## Online Documentation

Use this space to list online documentations needed in this project

* [Google Drive](https://drive.google.com/drive/u/0/folders/1p96bKQpGfEkJU8u73eAg4Mwy787ojNMP)
* [Project Proposal](https://docs.google.com/document/d/1rSKMuVN15UCtYD5BoVMNZgrb_VtyGrW0GbE4PmHNac0/edit?usp=sharing)
* [Progression Report](https://docs.google.com/document/d/1KXXet0OK6BldWUDonNF7j6mLJ_OmFQige_xx4EZLFTQ/edit#heading=h.14yodgbfx7y8)
* [Demo Presentation]()
* [Final Report]()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to start all MondoDB Instances

### Config Server
1. Connect to EC2
    ```sh
    ssh -i "dsci551-t3eam79.pem" ubuntu@ec2-54-193-107-112.us-west-1.compute.amazonaws.com
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





