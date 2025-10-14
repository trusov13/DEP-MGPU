
  
    

  create  table "superstore"."dw_test"."sales_fact__dbt_tmp"
  
  
    as
  
  (
    -- Создает таблицу фактов, объединяя все измерения
SELECT
    -- Суррогатные ключи из измерений
    cd.cust_id,
    pd.prod_id,
    sd.ship_id,
    gd.geo_id,
    -- Ключи для календаря
    to_char(o.order_date, 'yyyymmdd')::int AS order_date_id,
    to_char(o.ship_date, 'yyyymmdd')::int AS ship_date_id,
    -- Бизнес-ключ и метрики
    o.order_id,
    o.sales,
    o.profit,
    o.quantity,
    o.discount
FROM "superstore"."stg"."stg_orders" AS o
LEFT JOIN "superstore"."dw_test"."customer_dim" AS cd ON o.customer_id = cd.customer_id
LEFT JOIN "superstore"."dw_test"."product_dim" AS pd ON o.product_id = pd.product_id
LEFT JOIN "superstore"."dw_test"."shipping_dim" AS sd ON o.ship_mode = sd.ship_mode
LEFT JOIN "superstore"."dw_test"."geo_dim" AS gd ON o.postal_code = gd.postal_code AND o.city = gd.city AND o.state = gd.state
  );
  