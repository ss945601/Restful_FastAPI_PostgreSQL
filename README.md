# Restful_FastAPI_PostgreSQL
Simple template for Rest API using FastAPI &amp; PostgreSQL


# Install 
1. pip install -r requirements.txt.

# Setting
1. edit "db_connect.py", set your PostgreSQL db info.
2. edit router & table name & columns in "router/user.py". # (User RestfulAPI)
3. Auto create files like "router/user.py", just edit the setting scope in the "buildModel.py"  as follow and run "python buildModel.py" 
   the .py file is added in the "router" folder.
4. user.router should add in "main.py". 
   
# Run
1. uvicorn main:app --reload
2. To test api on http://127.0.0.1:8000/docs
3. The detail of api on http://127.0.0.1:8000/redoc
