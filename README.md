# Restful_FastAPI_PostgreSQL
Simple template for Rest API using FastAPI &amp; PostgreSQL


# Install 
1. pip install -r requirements.txt.

# Setting
1. Edit "db_connect.py",and set your PostgreSQL db info.
2. Edit router & table name & columns in "router/user.py". # (User RestfulAPI)
3. Auto create files like "router/user.py", just edit the setting scope in the "buildModel.py" and run "python buildModel.py" 
   the .py file will be added in the "router" folder.
4. Finally, user.router should be added in "main.py". 
   
# Run
1. uvicorn main:app --reload
2. To test api on http://127.0.0.1:8000/docs
3. The document of api on http://127.0.0.1:8000/redoc
