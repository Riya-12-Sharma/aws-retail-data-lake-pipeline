"""
AWS Glue 4.0+ PySpark batch ETL.
Required job args:
--SOURCE_S3_PATH s3://bucket/raw/orders/
--TARGET_S3_PATH s3://bucket/curated/orders/
--QUALITY_S3_PATH s3://bucket/quality/orders/
--DATABASE_NAME retail_analytics
--TABLE_NAME curated_orders
"""
import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.window import Window

args = getResolvedOptions(sys.argv, [
    "JOB_NAME", "SOURCE_S3_PATH", "TARGET_S3_PATH", "QUALITY_S3_PATH",
    "DATABASE_NAME", "TABLE_NAME"
])

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

required = [
    "order_id", "order_date", "customer_id", "product_id", "product_name",
    "category", "quantity", "unit_price", "region", "sales_channel", "order_status"
]
raw = spark.read.option("header", True).option("mode", "PERMISSIVE").csv(args["SOURCE_S3_PATH"])
missing = [c for c in required if c not in raw.columns]
if missing:
    raise ValueError("Source is missing required columns: " + ", ".join(missing))

df = raw.select(*required)
df = (df
    .withColumn("order_id", F.trim(F.col("order_id")))
    .withColumn("customer_id", F.trim(F.col("customer_id")))
    .withColumn("order_date_parsed", F.to_date("order_date", "yyyy-MM-dd"))
    .withColumn("quantity_num", F.col("quantity").cast("int"))
    .withColumn("unit_price_num", F.col("unit_price").cast("decimal(12,2)"))
    .withColumn("order_status", F.upper(F.trim(F.col("order_status"))))
)

reason = F.when(F.col("order_id").isNull() | (F.col("order_id") == ""), "missing_order_id") \
    .when(F.col("order_date_parsed").isNull(), "invalid_order_date") \
    .when(F.col("customer_id").isNull() | (F.col("customer_id") == ""), "missing_customer_id") \
    .when(F.col("quantity_num").isNull() | (F.col("quantity_num") <= 0), "invalid_quantity") \
    .when(F.col("unit_price_num").isNull() | (F.col("unit_price_num") < 0), "invalid_unit_price") \
    .when(~F.col("region").isin("North", "South", "East", "West"), "invalid_region") \
    .when(~F.col("order_status").isin("COMPLETED", "CANCELLED", "RETURNED"), "invalid_order_status")

df = df.withColumn("rejection_reason", reason)
dedupe_window = Window.partitionBy("order_id").orderBy(F.col("order_date_parsed").asc_nulls_last())
df = df.withColumn("_row_num", F.row_number().over(dedupe_window))
df = df.withColumn(
    "rejection_reason",
    F.when((F.col("rejection_reason").isNull()) & (F.col("_row_num") > 1), "duplicate_order_id")
     .otherwise(F.col("rejection_reason"))
)

rejected = df.filter(F.col("rejection_reason").isNotNull())
valid = df.filter(F.col("rejection_reason").isNull())

curated = (valid
    .withColumn("quantity", F.col("quantity_num"))
    .withColumn("unit_price", F.col("unit_price_num"))
    .withColumn("gross_sales", (F.col("quantity_num") * F.col("unit_price_num")).cast("decimal(14,2)"))
    .withColumn("net_sales", F.when(F.col("order_status") == "COMPLETED", F.col("gross_sales")).otherwise(F.lit(0).cast("decimal(14,2)")))
    .withColumn("order_year", F.year("order_date_parsed"))
    .withColumn("order_month", F.month("order_date_parsed"))
    .withColumn("order_date", F.col("order_date_parsed"))
    .select(
        "order_id", "order_date", "customer_id", "product_id", "product_name", "category",
        "quantity", "unit_price", "gross_sales", "net_sales", "region", "sales_channel",
        "order_status", "order_year", "order_month"
    )
)

quality_path = args["QUALITY_S3_PATH"].rstrip("/")
(rejected
    .drop("_row_num", "order_date_parsed", "quantity_num", "unit_price_num")
    .write.mode("overwrite").option("header", True)
    .csv(quality_path + "/rejected_records/"))

curated_path = args["TARGET_S3_PATH"].rstrip("/")
(curated.write.mode("overwrite").format("parquet")
    .partitionBy("order_year", "order_month")
    .save(curated_path))

summary = spark.createDataFrame(
    [(raw.count(), curated.count(), rejected.count())],
    ["input_rows", "curated_rows", "rejected_rows"]
)
summary = summary.withColumn("processed_at_utc", F.current_timestamp())
(summary.coalesce(1).write.mode("overwrite").json(quality_path + "/run_summary/"))

# Create/update catalog metadata for the Parquet location. The job role needs Glue catalog permissions.
spark.sql("CREATE DATABASE IF NOT EXISTS " + args["DATABASE_NAME"])
spark.sql(
    "CREATE TABLE IF NOT EXISTS " + args["DATABASE_NAME"] + "." + args["TABLE_NAME"] +
    " USING PARQUET LOCATION '" + curated_path + "'"
)
job.commit()
