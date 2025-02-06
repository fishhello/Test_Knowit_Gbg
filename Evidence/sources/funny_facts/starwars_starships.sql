select 
    manufacturer,
    count(*) as vehicle_count
from starwars_data
group by manufacturer
order by vehicle_count desc
limit 5