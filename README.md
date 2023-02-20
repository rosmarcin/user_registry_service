# Django Boilerplate Backend

A boilerplate for common backend use cases

# Testing PostgreSQL container

```
docker run --name postgresql_mr2 -e POSTGRES_PASSWORD=Admin123! -p 5432:5432 -d postgres

```

 

# DevOps CI/CD
For this project we use containers to streamline operations and allow further migration to other platforms and cloud. 

For the CI/CD we use GitLab pipelines. GitLab will run the tests for on every update and, if there are no bugs, build the Docker image automatically.

We decided to use one docker container for the entire application to simplify the deployment and migrations. For the production ready deployment the database layer and the application backend can be run as a separate containers. 

Project pipeline is configured in : .gitlab-ci.yml. This file would contain the instructions to build our project. Pipeline is executed on each commit - GitLab invokes a Runner to build and test the project.

For development we used local GitLab Runner with Docker:Python 3.7 executor.

To start mysql server:

```
$ docker-compose up -d --force-recreate db
```

To start Sales Model server

```
$ docker-compose up -d web

```

Cleaning system 

```
$ docker system prune -a
$ docker volume prune

```
Or

```
$ docker container stop $(docker container ls –aq) && docker system prune –af ––volumes

```

# Communication with other microservices

Two options of communication
1. Self deployed kafka message broker
2. Cloud managed messaging service (e.g. AWS )

Kafka can be used as a message broker

## Install Kafka 


### Install Java

sudo apt-get update && sudo apt-get upgrade -y
java -version
sudo apt install openjdk-8-jdk -y

### Install Zookeeper 

```
sudo apt-get install zookeeperd

```

Check if Zookeeper has started

```
telnet localhost 2181
```

Check if Zookeeper has started

```
telnet localhost 2181
>ruok
>imok
```

### Install Kafka

```
wget https://ftp.wayne.edu/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz
curl http://kafka.apache.org/KEYS | gpg --import
gpg --verify kafka_2.12-1.0.1.tgz.asc kafka_2.12-1.0.1.tgz

tar -xzf kafka_2.13-2.6.0.tgz
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Start Kafka server
```
bin/kafka-server-start.sh config/server.properties
```

Kreate quickstart topic:
```
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```

Start producer and consumer in a separate sessions

```
~/kafka_2.12-2.8.0$ bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
```

```
~/kafka_2.12-2.8.0$ bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
```

### List topics

```
bin/kafka-topics.sh --list --zookeeper localhost:2181
```


### Stop Kafka

Stop the consumer and producer clients with Ctrl+C
Stop the Kafka broker with Ctrl+C
Stop the ZooKeeper server with Ctrl+C

Run the following command to clean up:
```
rm -rf /tmp/kafka-logs /tmp/zookeeper
```


## Start ZooKeeper using Docker

```
docker pull wurstmeister/zookeeper:latest
docker run -d \
  -p 2181:2181 \
  --name zookeeper \
  wurstmeister/zookeeper:latest
```

### Start Kafka using Docker

```
docker pull wurstmeister/kafka:latest

KAFKA_BROKER_ID="001"
KAFKA_CREATE_TOPICS="test0:1:3,test1:1:1:compact"
## test0 will have 1 partition and 3 replicas
## test1 will have 1 partition, 1 replica and a cleanup.policy set to compact.


docker run -d -p 9094:9094 \
  -e KAFKA_BROKER_ID="${KAFKA_BROKER_ID}" \
  -e KAFKA_CREATE_TOPICS="${KAFKA_CREATE_TOPICS}" \
  -e HOSTNAME_COMMAND="docker info | grep ^Name: | cut -d' ' -f 2" \
  -e KAFKA_ZOOKEEPER_CONNECT="zookeeper:2181" \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP="INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT" \
  -e KAFKA_ADVERTISED_LISTENERS="INSIDE://:9092,OUTSIDE://_{HOSTNAME_COMMAND}:9094" \
  -e KAFKA_LISTENERS="INSIDE://:9092,OUTSIDE://:9094" \
  -e KAFKA_INTER_BROKER_LISTENER_NAME="INSIDE" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --link zookeeper:zookeeper \
  --name kafka \
  wurstmeister/kafka:latest

```

List running containers
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}'
View stdout logs
docker logs kafka
docker logs zookeeper
Run Kafka Commands inside the container
## List Brokers
docker exec -ti kafka /usr/bin/broker-list.sh

## List Topics
docker exec -ti kafka /opt/kafka/bin/kafka-topics.sh --list --zookeeper zookeeper:2181

## Create a Topic
docker exec -ti kafka /opt/kafka/bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic test2


## List Topics
docker exec -ti kafka /opt/kafka/bin/kafka-topics.sh --list --zookeeper zookeeper:2181
