-----------------CRITICAL----------------------------------


        1. Khi khởi động lại cụm Hadoop phải cài lại python 3.9 và Java 8 cho Jupyter Notebook

        2. sudo apt-get update 
           && sudo apt-get install openjdk-8-jdk -y

        3.
            sudo apt update
            && sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
            && wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
            && tar -xf Python-3.9.1.tgz
            && cd Python-3.9.1
               ./configure --enable-optimizations
            && make -j 12
            && sudo make altinstall
            && alias python3=python3.9


         4.
         docker exec -it -u 0 jupyter /bin/bash
             pip install --upgrade pip  
             pip install requests-html  
             pip install selenium  
             pip install kafka-python
             pip install pyspark 
             pip install --force-reinstall pyspark==2.4.6

-----------------CRITICAL----------------------------------

---https://github.com/haiphucnguyen/BigDataDemo/tree/master

        1.  Cài  Java 8 
            sudo apt update
            sudo apt install openjdk-8-jdk  -y
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

            docker cp /home/huynt/bin/bin/app/BigDataDemo/cart-stream-processing/build/libs/cart-stream-processing-1.0-SNAPSHOT.jar spark-master:data

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

    ----*END POINT
            http://localhost:8088/cluster/nodes reource manager
            http://localhost:8082/ spark master
            http://localhost:50075/ data node
            http://localhost:50070/dfshealth.html#tab-overview name node
            http://localhost:8042/node node manager
            http://localhost:8188/applicationhistory history server



              docker cp D:\dataset\MillionSongSubset jupyter:~/project/code    
              ssh -L 8888:localhost:8888 huynt@congcu24h.ddns.net
              ssh -L 50070:localhost:50070 huynt@congcu24h.ddns.net
              ssh -L 9092:localhost:9092 huynt@congcu24h.ddns.net
              ssh -L 9093:kafka:9093 huynt@congcu24h.ddns.net
              ssh -L 2181:localhost:2182 huynt@congcu24h.ddns.net
              ssh -L 10000:localhost:10000 huynt@congcu24h.ddns.net
              ssh -L 8042:localhost:8042 huynt@congcu24h.ddns.net
              ssh -L 50075:localhost:50075 huynt@congcu24h.ddns.net
              ssh -L 8088:localhost:8088 huynt@congcu24h.ddns.net
              ssh -L 8899:localhost:8899 huynt@congcu24h.ddns.net
              ssh -L 5000:localhost:5000 huynt@congcu24h.ddns.net

