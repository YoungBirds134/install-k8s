---https://github.com/haiphucnguyen/BigDataDemo/tree/master

        1.  Cài  Java 8 
        2. Build ra bản build jar của java 
            ./gradlew shadowJar
            gradle wrapper
        3. Làm theo hướng dẫn
        4.spark-stream-hive-submit.sh

            ------

            #!/bin/bash

            ./gradlew shadowJar

            docker cp /home/huynt/bin/bin/app/BigDataDemo/cart-stream-processing/build/libs/cart-stream-processing-1.0-SNAPSHOT.jar spark-master:data

            docker cp /home/huynt/bin/bin/app/BigDataDemo/cart-stream-processing/build/libs/cart-stream-processing-1.0-SNAPSHOT-all.jar spark-master:data            

            docker exec -ti spark-master sh -c  "cd data && /spark/bin/spark-submit --class com.bd.streaming.hive.CartStreamingHiveApp --master spark://spark-master:7077 cart-stream-processing-1.0-SNAPSHOT-all.jar "

            ------
-------

