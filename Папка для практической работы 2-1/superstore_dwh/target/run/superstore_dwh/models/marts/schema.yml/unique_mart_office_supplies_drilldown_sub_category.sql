
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    sub_category as unique_field,
    count(*) as n_records

from "superstore"."dw_test"."mart_office_supplies_drilldown"
where sub_category is not null
group by sub_category
having count(*) > 1



  
  
      
    ) dbt_internal_test