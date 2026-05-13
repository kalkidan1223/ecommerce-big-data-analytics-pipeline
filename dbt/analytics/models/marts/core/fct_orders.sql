{{ config(
    materialized='table',
    schema='core'
) }}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

payments AS (
    SELECT 
        order_id,
        SUM(payment_value_decimal) as total_payment,
        COUNT(DISTINCT payment_type) as num_payment_methods,
        MAX(payment_installments) as max_installments
    FROM {{ ref('stg_payments') }}
    GROUP BY order_id
),

items AS (
    SELECT 
        order_id,
        COUNT(*) as num_items,
        SUM(price) as total_item_price,
        SUM(freight_value) as total_freight,
        SUM(item_total_value) as total_item_value,
        AVG(price) as avg_item_price
    FROM {{ ref('stg_items') }}
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_year_month,
    o.is_delivered,
    o.days_to_delivery,
    COALESCE(p.total_payment, 0) as total_payment,
    COALESCE(p.num_payment_methods, 0) as num_payment_methods,
    COALESCE(i.num_items, 0) as num_items,
    COALESCE(i.total_item_price, 0) as total_item_price,
    COALESCE(i.total_freight, 0) as total_freight,
    COALESCE(i.total_item_value, 0) as total_item_value
FROM orders o
LEFT JOIN payments p ON o.order_id = p.order_id
LEFT JOIN items i ON o.order_id = i.order_id
