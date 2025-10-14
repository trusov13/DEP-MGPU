-- models/marts/mart_office_supplies_drilldown.sql
SELECT
    p.sub_category,
    SUM(f.profit) AS total_profit
FROM {{ ref('sales_fact') }} AS f
LEFT JOIN {{ ref('product_dim') }} AS p ON f.prod_id = p.prod_id
WHERE p.category = 'Office Supplies'
GROUP BY p.sub_category
ORDER BY total_profit DESC