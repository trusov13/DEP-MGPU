
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ship_id
from "superstore"."dw_test"."shipping_dim"
where ship_id is null



  
  
      
    ) dbt_internal_test