select 
    replace(name, '-gmax', '') as name,
    weight,
    height
from pokeapi_data
order by weight desc
limit 5