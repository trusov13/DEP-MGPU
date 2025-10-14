
    
    

with child as (
    select cust_id as from_field
    from "superstore"."dw_test"."sales_fact"
    where cust_id is not null
),

parent as (
    select cust_id as to_field
    from "superstore"."dw_test"."customer_dim"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


