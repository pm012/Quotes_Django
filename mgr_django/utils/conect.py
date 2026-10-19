from pathlib import Path
import configparser
from pymongo import MongoClient
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')


def get_mongo_connection_uri() -> tuple[str, str]:
    mongo_user = env('MONGO_USER', default=None)
    mongo_pass = env('MONGO_PASS', default=None)
    db_name = env('MONGO_DB_NAME', default='quotes')
    domain = env('MONGO_DOMAIN', default=None)

    if not all([mongo_user, mongo_pass, domain]):
        conf_file_path = BASE_DIR / 'mgr_django' / 'utils' / 'conf.ini'
        if conf_file_path.exists():
            config = configparser.ConfigParser()
            config.read(conf_file_path)
            mongo_user = config.get('DB', 'USER', fallback='')
            mongo_pass = config.get('DB', 'PASS', fallback='')
            db_name = config.get('DB', 'DB_NAME', fallback='quotes')
            domain = config.get('DB', 'DOMAIN', fallback='')

    if mongo_user and mongo_pass and domain:
        connection_uri = (
            f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}"
            "?retryWrites=true&w=majority"
        )
    else:
        connection_uri = f"mongodb://localhost:27017/{db_name}"

    return db_name, connection_uri


def get_mongo_connection():
    db_name, connection_uri = get_mongo_connection_uri()
    client = MongoClient(connection_uri)
    client.admin.command('ping')
    return client[db_name]


if __name__ == "__main__":
    db_name, connection_uri = get_mongo_connection_uri()
    print(connection_uri)
    print(db_name)