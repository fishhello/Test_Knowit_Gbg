## Hello!

This is some funny facts about the characters in Starwars!


### Orders Table

```sql starwars_characters
select * FROM funny_facts.starwars_characters;
```

<BarChart 
    data={starwars_characters}
    x=eye_color
    y=count
    title="Most Common Eye Colors"
/>
