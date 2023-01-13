#!/usr/bin/python3

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

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
            .option("subscribe", "sensors") \
            .option("startingOffsets", "earliest") \
            .load()

#     rawDF = inputDF.selectExpr("CAST(value AS STRING)").alias("value")
#     expandedDF = rawDF.rdd.map(lambda x: x.value.split(", "))

    splitDF = inputDF.select(F.split(F.col("value"), ", ").alias("value"))
    df = splitDF.withColumn("timestamp", splitDF.value.getItem(0).cast("String")) \
        .withColumn("device", splitDF.value.getItem(1)) \
        .withColumn("temp", splitDF.value.getItem(2).cast("float")) \
        .withColumn("humd", splitDF.value.getItem(3).cast("float")) \
        .withColumn("pres", splitDF.value.getItem(4).cast("float")) \
        .drop("value")

    query = df.writeStream \
        .outputMode("update") \
        .format("console") \
        .start()

    query.awaitTermination()