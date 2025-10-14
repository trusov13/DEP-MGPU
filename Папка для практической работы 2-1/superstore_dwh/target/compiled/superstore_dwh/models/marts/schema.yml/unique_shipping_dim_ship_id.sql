
    
    

select
    ship_id as unique_field,
    count(*) as n_records

from "superstore"."dw_test"."shipping_dim"
where ship_id is not null
group by ship_id
having count(*) > 1


