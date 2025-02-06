select 
    illustrator,
    count(*) as cards_illustrated
from netrunnerdb_data
where illustrator is not null
group by illustrator
order by cards_illustrated desc
limit 5