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
docker exec -ti spark-master sh -c  "cd data &&  /spark/bin/spark-submit --class com.bd.streaming.hive.CartStreamingHiveApp --master spark://spark-master:7077 cart-stream-processing-1.0-SNAPSHOT-all.jar"

        5. Bug không tạo máy ảo được trong  jupyter do thiếu cấu hình ingress
           https://aptro.github.io/server/architecture/2016/06/21/Jupyter-Notebook-Nginx-Setup.html
