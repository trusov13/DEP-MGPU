
    
    

select
    prod_id as unique_field,
    count(*) as n_records

from "superstore"."dw_test"."product_dim"
where prod_id is not null
group by prod_id
having count(*) > 1


