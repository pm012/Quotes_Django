import configparser
from pymongo import MongoClient
import os

conf_file_path = os.path.abspath('./hw10_django/utils/conf.ini')
config = configparser.ConfigParser()
config.read(conf_file_path)
mongo_user = config.get('DB', 'USER')
mongo_pass = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')


def get_mongo_connection():
    # Construct the MongoDB connection URI
    connection_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
    
    # Connect to the MongoDB cluster
    client = MongoClient(connection_uri)
    
    # Select the database
    db = client[db_name]
    
    return db
