A project using the APIs from various sorces to come up with fun facts.

Overview 
- Get data from SWAPI, PokeAPI and NetrunnerDB
- Process the data using dbt models
- Using Evidence to visulize the data 

Prerequisites
- python 3.8+
- duckdb
- dbt
- Evidence

How to use
1. Clone the project from GitHub

2. Set up Python environment 
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt

3. Innit dbt
cd dbt_project 
dbt deps

4. Install Evidence
https://docs.evidence.dev/install-evidence

5. Process the data 
cd dbt_project 
dbt run

6. Start Evidence, it will launch Evidence localy  
cd evidence_project
npx evidence dev
