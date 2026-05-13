{{ config(
    materialized='view',
    schema='staging'
) }}

SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value as payment_amount,
    CAST(payment_value AS DECIMAL(10, 2)) as payment_value_decimal
FROM payments
WHERE order_id IS NOT NULL
    AND payment_value > 0
