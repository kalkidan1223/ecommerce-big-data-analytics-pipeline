SELECT
    order_id,
    payment_sequential,
    'invalid_payment_value' AS failure_type
FROM {{ ref('stg_payments') }}
WHERE payment_value_decimal IS NULL OR payment_value_decimal <= 0

UNION ALL

SELECT
    order_id,
    payment_sequential,
    'invalid_payment_type' AS failure_type
FROM {{ ref('stg_payments') }}
WHERE payment_type NOT IN ('credit_card', 'debit_card', 'boleto', 'voucher', 'not_defined')

UNION ALL

SELECT
    order_id,
    payment_sequential,
    'invalid_installments' AS failure_type
FROM {{ ref('stg_payments') }}
WHERE payment_installments < 1

UNION ALL

SELECT
    order_id,
    payment_sequential,
    'duplicate_payment' AS failure_type
FROM {{ ref('stg_payments') }}
GROUP BY order_id, payment_sequential
HAVING COUNT(*) > 1
