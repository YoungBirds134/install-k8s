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





------ Cấu hình Cho Spark kết nối Kafka (https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#deploying)

    --------Cài thư viện trong từng spark container 

    docker exec -ti spark-master sh -c  " /spark/bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"

    docker exec -ti spark-worker-1 sh -c  " /spark/bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"

    --------------------- Cấu hình version cho spark session ---

        https://stackoverflow.com/questions/70374571/connecting-pyspark-with-kafka

        scala_version = '2.12'
        spark_version = '3.1.2'
        # TODO: Ensure match above values match the correct versions
        packages = [
            f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
            'org.apache.kafka:kafka-clients:3.2.1'
        ]
        # Create a Spark session
        spark = SparkSession.builder \
            .appName("Cart Streaming Processing") \
            .config("spark.driver.allowMultipleContexts", "true") \
            .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
            .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/hive") \
            .config("spark.jars.packages", ",".join(packages))\
            .enableHiveSupport() \
            .getOrCreate()

    --------------------- Cấu hình version cho spark session ---

