
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_profit
from "superstore"."dw_test"."mart_office_supplies_drilldown"
where total_profit is null



  
  
      
    ) dbt_internal_test