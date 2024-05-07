import configparser
from mongoengine import connect
import os

conf_file_path = os.path.abspath('./hw10_django/utils/conf.ini')
config = configparser.ConfigParser()
config.read(conf_file_path)
mongo_user = config.get('DB', 'USER')
mongo_pass = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')


def get_mongo_connection():
    connection_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"
    return connect(host=connection_uri, ssl=True)