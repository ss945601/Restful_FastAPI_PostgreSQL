# Restful_FastAPI_PostgreSQL
Simple template for Rest API using FastAPI &amp; PostgreSQL


# Install 
1. pip install -r requirements.txt.

# Setting
1. edit "db_connect.py", set your PostgreSQL db info.
2. edit router & table name & columns in "router/user.py". # (User RestfulAPI)
3. user.router should add in "main.py". 
   
# Run
1. uvicorn main:app --reload
