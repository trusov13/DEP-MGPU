
  
    

  create  table "superstore"."dw_test"."geo_dim__dbt_tmp"
  
  
    as
  
  (
    -- Создает географический справочник
SELECT
    100 + row_number() OVER (ORDER BY "postal_code", "city", "state") as geo_id,
    "country",
    "city",
    "state",
    "postal_code"
FROM (
    SELECT DISTINCT "country", "city", "state", "postal_code" FROM "superstore"."stg"."stg_orders"
) as unique_geo
  );
  