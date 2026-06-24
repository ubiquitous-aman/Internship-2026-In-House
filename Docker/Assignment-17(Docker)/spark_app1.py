from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("SalesDataFrameApp").master("local[*]").getOrCreate()
)

df = spark.read.csv("sales.csv", header=True, inferSchema=True)

print("Original Data:")
df.show()

# Sort by sales descending
sorted_df = df.orderBy("sales", ascending=False)
print("Products sorted by sales descending:")
sorted_df.show()

# Top 3 highest sales
top3_df = sorted_df.limit(3)
print("Top 3 products with highest sales:")
top3_df.show()

# Filter sales > 80000
filtered_df = df.filter(df.sales > 80000)
print("Products with sales > 80000:")
filtered_df.show()

# Save as CSV
filtered_df.write.mode("overwrite").csv("/app/filtered_sales.csv", header=True)

print("Filtered data saved to filtered_sales.csv")

spark.stop()
