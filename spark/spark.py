#!/usr/bin/python3

from pyspark.sql import SparkSession

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 pyspark-shell'

if __name__ == "__main__":
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("SSKafka") \
        .getOrCreate()

    # spark.sparkContext.setLogLevel("DEBUG")

    inputDF = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "sensor") \
            .option("startingOffsets", "earliest") \
            .load()

    ds = inputDF.selectExpr("CAST(value AS STRING)")

    # print(type(inputDF))
    # print(type(ds))

    writeStream = ds.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

    writeStream.awaitTermination()