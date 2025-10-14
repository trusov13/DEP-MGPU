
    
    

select
    sub_category as unique_field,
    count(*) as n_records

from "superstore"."dw_test"."mart_office_supplies_drilldown"
where sub_category is not null
group by sub_category
having count(*) > 1


