#!/usr/bin/python3

from pyspark.sql import SparkSession

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0,org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0 pyspark-shell'

spark = SparkSession.builder \
        .master("local[1]") \
        .appName("SSKafka") \
        .getOrCreate()

inputDF = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "sensor") \
        .option("startingOffsets", "earliest") \
        .load()

ds = inputDF.selectExpr("CAST(value AS STRING)")

print(type(inputDF))
print(type(ds))