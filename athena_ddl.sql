-- Run in Athena after replacing YOUR_BUCKET with your bucket name.
CREATE DATABASE IF NOT EXISTS retail_analytics;

CREATE EXTERNAL TABLE IF NOT EXISTS retail_analytics.curated_orders (
  order_id string,
  order_date date,
  customer_id string,
  product_id string,
  product_name string,
  category string,
  quantity int,
  unit_price decimal(12,2),
  gross_sales decimal(14,2),
  net_sales decimal(14,2),
  region string,
  sales_channel string,
  order_status string
)
PARTITIONED BY (order_year int, order_month int)
STORED AS PARQUET
LOCATION 's3://YOUR_BUCKET/curated/orders/';

-- If you create the table manually, run this after Glue has written output:
MSCK REPAIR TABLE retail_analytics.curated_orders;
