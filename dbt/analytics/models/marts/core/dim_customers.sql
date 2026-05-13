{{ config(
    materialized='table',
    schema='core'
) }}

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) as total_orders,
        SUM(total_payment) as lifetime_value,
        AVG(total_payment) as avg_order_value,
        MIN(order_purchase_timestamp) as first_order_date,
        MAX(order_purchase_timestamp) as last_order_date,
        SUM(CASE WHEN is_delivered = 1 THEN 1 ELSE 0 END) as delivered_orders,
        AVG(days_to_delivery) as avg_delivery_days
    FROM {{ ref('fct_orders') }}
    GROUP BY customer_id
)

SELECT
    customer_id,
    total_orders,
    CAST(lifetime_value AS DECIMAL(12, 2)) as lifetime_value,
    CAST(avg_order_value AS DECIMAL(10, 2)) as avg_order_value,
    first_order_date,
    last_order_date,
    DATE_DIFF('day', first_order_date, last_order_date) as customer_age_days,
    delivered_orders,
    CAST(ROUND(100.0 * delivered_orders / total_orders, 2) AS DECIMAL(5, 2)) as delivery_success_rate,
    CAST(ROUND(avg_delivery_days, 1) AS DECIMAL(5, 1)) as avg_delivery_days,
    CASE 
        WHEN DATE_DIFF('day', last_order_date, CURRENT_DATE) < 30 THEN 'Active'
        WHEN DATE_DIFF('day', last_order_date, CURRENT_DATE) < 90 THEN 'At Risk'
        ELSE 'Inactive'
    END as customer_status
FROM customer_orders
