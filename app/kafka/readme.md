docker exec -u 0 -it kafka /bin/bash 

kafka-topics.sh --bootstrap-server localhost:9092 --topic {{first_topic}} --create --partitions 3 --replication-factor 1

kafka-topics.sh --bootstrap-server localhost:9092 --list

kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic first_topic




