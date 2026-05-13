{{ config(
    materialized='view',
    schema='staging'
) }}

SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    order_year_month,
    CAST(DATE_DIFF('day', order_purchase_timestamp, COALESCE(order_delivered_customer_date, CURRENT_DATE)) AS INT) as days_to_delivery,
    CASE 
        WHEN order_status = 'delivered' THEN 1 
        ELSE 0 
    END as is_delivered
FROM orders
WHERE order_id IS NOT NULL
