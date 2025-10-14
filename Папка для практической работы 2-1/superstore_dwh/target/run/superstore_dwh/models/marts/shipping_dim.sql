
  
    

  create  table "superstore"."dw_test"."shipping_dim__dbt_tmp"
  
  
    as
  
  (
    -- Создает справочник видов доставки
SELECT
    100 + row_number() OVER (ORDER BY "ship_mode") as ship_id,
    "ship_mode"
FROM (
    SELECT DISTINCT "ship_mode" FROM "superstore"."stg"."stg_orders"
) as unique_shipping_modes
  );
  