#!/bin/bash

./gradlew shadowJar

docker cp /home/huynt/bin/bin/app/BigDataDemo/cart-stream-processing/build/libs/cart-stream-processing-1.0-SNAPSHOT.jar spark-master:data

docker exec -ti spark-master sh -c  "cd data &&  /spark/bin/spark-submit --class com.bd.streaming.hive.CartStreamingHiveApp --master spark://spark-master:7077 cart-stream-processing-1.0-SNAPSHOT-all.jar"
