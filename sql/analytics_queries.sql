-- Revenue Analysis by Month
SELECT
    order_year_month,
    COUNT(DISTINCT order_id) as num_orders,
    COUNT(DISTINCT customer_id) as num_customers,
    SUM(total_payment) as total_revenue,
    AVG(total_payment) as avg_order_value,
    SUM(total_item_value) as total_items_value
FROM core.fct_orders
GROUP BY order_year_month
ORDER BY order_year_month DESC;

-- Top Customers by Lifetime Value
SELECT
    customer_id,
    total_orders,
    lifetime_value,
    avg_order_value,
    first_order_date,
    last_order_date,
    customer_status
FROM core.dim_customers
ORDER BY lifetime_value DESC
LIMIT 100;

-- Order Status Distribution
SELECT
    order_status,
    COUNT(*) as order_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage,
    AVG(total_payment) as avg_order_value
FROM core.fct_orders
GROUP BY order_status
ORDER BY order_count DESC;

-- Delivery Performance Metrics
SELECT
    order_year_month,
    COUNT(*) as total_orders,
    SUM(CASE WHEN is_delivered = 1 THEN 1 ELSE 0 END) as delivered_orders,
    ROUND(100.0 * SUM(CASE WHEN is_delivered = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as delivery_success_rate,
    ROUND(AVG(days_to_delivery), 1) as avg_delivery_days
FROM core.fct_orders
WHERE order_status IN ('delivered', 'canceled', 'unavailable')
GROUP BY order_year_month
ORDER BY order_year_month DESC;

-- Customer Segmentation Analysis
SELECT
    customer_status,
    COUNT(*) as num_customers,
    ROUND(AVG(lifetime_value), 2) as avg_lifetime_value,
    ROUND(AVG(total_orders), 1) as avg_orders_per_customer,
    ROUND(AVG(delivery_success_rate), 2) as avg_delivery_success_rate,
    MIN(lifetime_value) as min_customer_value,
    MAX(lifetime_value) as max_customer_value
FROM core.dim_customers
GROUP BY customer_status
ORDER BY avg_lifetime_value DESC;

-- Payment Method Analysis
SELECT
    payment_type,
    COUNT(*) as transaction_count,
    SUM(payment_value_decimal) as total_amount,
    ROUND(AVG(payment_value_decimal), 2) as avg_transaction_value,
    ROUND(AVG(payment_installments), 1) as avg_installments
FROM staging.stg_payments
GROUP BY payment_type
ORDER BY total_amount DESC;

-- Product Performance by Order Value
SELECT
    order_year_month,
    SUM(CASE WHEN total_payment < 100 THEN 1 ELSE 0 END) as orders_under_100,
    SUM(CASE WHEN total_payment BETWEEN 100 AND 500 THEN 1 ELSE 0 END) as orders_100_500,
    SUM(CASE WHEN total_payment BETWEEN 500 AND 1000 THEN 1 ELSE 0 END) as orders_500_1000,
    SUM(CASE WHEN total_payment > 1000 THEN 1 ELSE 0 END) as orders_over_1000,
    SUM(total_payment) as total_revenue
FROM core.fct_orders
GROUP BY order_year_month
ORDER BY order_year_month DESC;

-- Recent Customer Activity
SELECT
    customer_id,
    total_orders,
    lifetime_value,
    last_order_date,
    CURRENT_DATE - last_order_date as days_since_last_order,
    customer_status
FROM core.dim_customers
WHERE customer_status != 'Inactive'
ORDER BY last_order_date DESC
LIMIT 50;
