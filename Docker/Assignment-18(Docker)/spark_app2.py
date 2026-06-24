from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("PartitionDemoApp").master("local[*]").getOrCreate()
)

# Generate 5 million records using spark.range()
df = spark.range(0, 5000000)

print("Initial DataFrame created with 5 million records.")

# Display initial number of partitions
initial_partitions = df.rdd.getNumPartitions()
print(f"Initial number of partitions: {initial_partitions}")

# Increase partitions to 12 using repartition()
df_repartitioned = df.repartition(12)
repartitions = df_repartitioned.rdd.getNumPartitions()
print(f"Number of partitions after repartition(12): {repartitions}")

# Reduce partitions to 3 using coalesce()
df_coalesced = df_repartitioned.coalesce(3)
final_partitions = df_coalesced.rdd.getNumPartitions()
print(f"Number of partitions after coalesce(3): {final_partitions}")

# Optional: Show sample
print("\nSample data from final DataFrame:")
df_coalesced.show(5)

print("\nPartition operations completed successfully.")

spark.stop()
