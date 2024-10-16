-- models/filtered_data.sql
WITH filtered AS (
    SELECT
        date,
        pais,
        tipo cambio bs'
    FROM
        {{ ref('raw_data') }}
    WHERE
        exchange_rate > 6.5
)

SELECT * FROM filtered
