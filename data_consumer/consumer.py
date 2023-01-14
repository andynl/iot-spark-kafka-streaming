#!/usr/bin/python3

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, FloatType

import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 pyspark-shell'

def write_mongo_row(df, batch_id):
    df.write.format("com.mongodb.spark.sql.DefaultSource") \
        .mode("append") \
        .save()

if __name__ == "__main__":
    spark = SparkSession.builder \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/sensors.sensors") \
        .config("spark.mongodb.output.uri", "mongodb://localhost:27017/sensors.sensors") \
        .master("local[1]") \
        .appName("SSKafka") \
        .getOrCreate()

    schema = StructType([
        StructField("time", StringType(), True),
        StructField("device", StringType(), True),
        StructField("temp", FloatType(), True),
        StructField("humd", FloatType(), True),
        StructField("pres", FloatType(), True),
    ])

    inputDF = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "sensors") \
            .load()

    rawDF = inputDF.select(F.from_json(F.col("value").cast("string"), schema).alias("parsed_value")) \
        .select(F.col("parsed_value.time"), 
        F.col("parsed_value.device"),
        F.col("parsed_value.temp"),
        F.col("parsed_value.humd"),
        F.col("parsed_value.pres"))

    summaryDF = rawDF.groupBy("device") \
        .agg(F.avg("temp"),
        F.avg("humd"),
        F.avg("pres"))

    renamedDF = summaryDF.withColumnRenamed("avg(temp)", "temp") \
        .withColumnRenamed("avg(humd)", "humd") \
        .withColumnRenamed("avg(pres)", "pres")

    query = renamedDF.writeStream \
        .trigger(processingTime='5 seconds') \
        .foreachBatch(write_mongo_row) \
        .outputMode("update") \
        .start()

    query.awaitTermination()