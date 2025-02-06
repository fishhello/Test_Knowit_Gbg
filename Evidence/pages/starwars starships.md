## Hello!

This is some funny facts about the starships in Starwars!


### Orders Table

```sql starwars_ships
select * FROM funny_facts.starwars_starships;
```

<BarChart 
    data={starwars_ships}
    x=manufacturer
    y=vehicle_count
    title="Manufacturers That Has Produced the Most Starships"
/>
