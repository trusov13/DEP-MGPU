
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    subcategory as unique_field,
    count(*) as n_records

from "superstore"."dw_test"."mart_office_supplies_drilldown"
where subcategory is not null
group by subcategory
having count(*) > 1



  
  
      
    ) dbt_internal_test