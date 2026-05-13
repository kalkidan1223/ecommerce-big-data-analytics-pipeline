{{ config(
    materialized='view',
    schema='staging'
) }}

SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value,
    price + COALESCE(freight_value, 0) as item_total_value,
    CASE 
        WHEN freight_value IS NULL THEN 0 
        ELSE 1 
    END as has_freight
FROM items
WHERE order_id IS NOT NULL
    AND product_id IS NOT NULL
