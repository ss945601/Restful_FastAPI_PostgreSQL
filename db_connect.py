import databases
import sqlalchemy
import os
import urllib
class DbConnect:
    def getDataBase():
        host_server = os.environ.get('host_server', 'xxxxxx') # replace xxxxxx to host_server
        db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432'))) # replace 5432 to your port
        database_name = os.environ.get('database_name', 'xxxxxx') # replace xxxxxx to your database_name
        db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'xxxxxx'))) # replace xxxxxx to your db_username
        db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'xxxxxx'))) # replace xxxxxx to your db_password
        ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
        DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
        database = databases.Database(DATABASE_URL)
        metadata = sqlalchemy.MetaData()
        engine = sqlalchemy.create_engine(
            DATABASE_URL, pool_size=3, max_overflow=0
        )
        metadata.create_all(engine)
        return database, metadata


