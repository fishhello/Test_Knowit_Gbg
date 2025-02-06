import os
import duckdb
import requests
import pandas as pd
import time
import json

# Ensure 'data/' directory exists
os.makedirs("data", exist_ok=True)

# Database connection
conn = duckdb.connect("data/funny_facts.db")

# Define API endpoints
apis = {
    "swapi": "https://swapi.dev/api/people/",
    "pokeapi": "https://pokeapi.co/api/v2/pokemon?limit=100",
    "netrunnerdb": "https://netrunnerdb.com/api/2.0/public/cards",
    "starwars": "https://www.swapi.tech/api/starships/"
}

# Fetch data and load into DuckDB
for api_name, api_url in apis.items():
    print(f"Fetching data from {api_name}...")
    all_data = []

    next_url = api_url
    while next_url:
        try:
            response = requests.get(next_url)
            response.raise_for_status()
            data = response.json()
            #print(json.dumps(data, indent=4)) #Uncomment this to see the raw JSON data
            if api_name == "starwars":
                for item in data.get("results", []):
                    try:
                        # Extract details directly from the item
                        starship_info = {
                            "uid": item.get("uid"),
                            "name": item.get("name"),
                            "url": item.get("url")
                        }

                        # If you want more details, fetch them here
                        # But do it more efficiently
                        detail_response = requests.get(item["url"])
                        detail_response.raise_for_status()
                        detail_data = detail_response.json().get("result", {}).get("properties", {})

                        # Merge additional details
                        starship_info.update({
                            "model": detail_data.get("model"),
                            "manufacturer": detail_data.get("manufacturer"),
                            "length": detail_data.get("length"),
                            "crew": detail_data.get("crew"),
                            "passengers": detail_data.get("passengers")
                        })
                        all_data.append(starship_info)
                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching details for {item.get('name', 'starship')}: {e}")
                # Check for next page
                next_url = data.get("next")

            elif api_name == "netrunnerdb":
                image_template = data.get("imageUrlTemplate", "")
                for card in data.get("data", []):
                    card_data = {
                        "title": card.get("title"),
                        "faction": card.get("faction_code"),
                        "cost": int(card.get("faction_cost", 0)) if card.get("faction_cost") is not None else None,
                        "illustrator": card.get("illustrator"),
                        "keywords": card.get("keywords"),
                        "flavor": card.get("flavor"),
                        "text": card.get("text"),
                        "unique": card.get("uniqueness", False),
                        "side": card.get("side_code"),
                        "deck_limit": card.get("deck_limit"),
                        "image_url": f"https://card-images.netrunnerdb.com/v2/large/{card.get('code')}.jpg" if card.get('code') else None,
                    }
                    all_data.append(card_data)
                next_url = data.get("next")
            elif api_name == "pokeapi":
                for pokemon in data.get("results", []):
                    try:
                        detail_response = requests.get(pokemon["url"])
                        detail_response.raise_for_status()
                        pokemon_data = detail_response.json()
                        all_data.append({
                            "name": pokemon_data["name"],
                            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
                            "weight": pokemon_data["weight"],
                            "height": pokemon_data["height"],
                        })
                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching Pokemon details: {e}")
                next_url = data.get("next")
            else:  # swapi.dev
                all_data.extend(data.get("results", []))
                next_url = data.get("next")
    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {api_name}: {e}")
            break

    df = pd.json_normalize(all_data)
    if not df.empty:
        try:
            conn.execute(f"CREATE OR REPLACE TABLE {api_name}_data AS SELECT * FROM df")
            print(f"Data from {api_name} saved to DuckDB.")
        except Exception as e:
            print(f"Error inserting data into DuckDB for {api_name}: {e}")
    else:
        print(f"No data retrieved from {api_name}. Skipping database insert.")
    time.sleep(0.5)

conn.close()
print("Data loading complete.")