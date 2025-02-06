select 
    eye_color,
    count(*) as count
from swapi_data
where eye_color != 'unknown'
group by eye_color
order by count desc
limit 5