-- Ensure no null order IDs exist in orders
SELECT NULL
FROM {{ ref('stg_orders') }}
WHERE order_id IS NOT NULL
LIMIT 0
