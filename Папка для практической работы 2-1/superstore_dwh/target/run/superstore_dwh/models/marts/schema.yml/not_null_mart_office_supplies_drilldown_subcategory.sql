
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select subcategory
from "superstore"."dw_test"."mart_office_supplies_drilldown"
where subcategory is null



  
  
      
    ) dbt_internal_test