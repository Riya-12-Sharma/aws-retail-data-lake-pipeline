-- 1. Monthly completed-order revenue
SELECT order_year, order_month,
       ROUND(SUM(net_sales), 2) AS net_revenue,
       COUNT_IF(order_status = 'COMPLETED') AS completed_orders
FROM retail_analytics.curated_orders
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

-- 2. Product/category performance
SELECT category, product_name,
       SUM(quantity) AS units_sold,
       ROUND(SUM(net_sales), 2) AS net_revenue
FROM retail_analytics.curated_orders
WHERE order_status = 'COMPLETED'
GROUP BY category, product_name
ORDER BY net_revenue DESC
LIMIT 10;

-- 3. Regional performance
SELECT region, ROUND(SUM(net_sales), 2) AS net_revenue,
       COUNT(DISTINCT customer_id) AS customers
FROM retail_analytics.curated_orders
GROUP BY region
ORDER BY net_revenue DESC;

-- 4. Repeat customer summary (simple transaction-level approximation)
WITH customer_orders AS (
  SELECT customer_id, COUNT_IF(order_status = 'COMPLETED') AS completed_orders,
         SUM(net_sales) AS net_revenue
  FROM retail_analytics.curated_orders
  GROUP BY customer_id
)
SELECT
  COUNT_IF(completed_orders >= 2) AS repeat_customers,
  COUNT_IF(completed_orders = 1) AS one_time_customers,
  ROUND(AVG(net_revenue), 2) AS average_customer_revenue
FROM customer_orders;

-- 5. Data quality: null business keys (should return zero)
SELECT COUNT(*) AS bad_order_ids
FROM retail_analytics.curated_orders
WHERE order_id IS NULL OR trim(order_id) = '';

-- 6. Partition filter example: reduces scanned data when applicable
SELECT order_date, SUM(net_sales) AS daily_net_revenue
FROM retail_analytics.curated_orders
WHERE order_year = 2025 AND order_month = 3
GROUP BY order_date
ORDER BY order_date;
