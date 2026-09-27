from unittest.mock import patch
import re
from mgr_django.utils.conect import get_mongo_connection, get_mongo_connection_uri

def test_connect_exception():
    with patch('pymongo.MongoClient', side_effect=Exception("Connection error")):
        # Перевіряємо обробку помилки підключення
        try:
            get_mongo_connection()
        except Exception as e:
            assert str(e) == "Connection error"



def test_get_uri():
    # MongoDB Atlas connection string pattern
    pattern = r"^mongodb\+srv://[a-zA-Z0-9_.]+:[^@]+@([a-zA-Z0-9_-]+\.)+mongodb\.net/[^?]+(\?.*)?$"

    connection_uri_tuple = get_mongo_connection_uri()
    uri = str(connection_uri_tuple[1])

    assert isinstance(connection_uri_tuple[0], str), "First element of the tuple should be string"
    assert re.match(pattern, uri) is not None, f"URI '{uri}' is not a  MongoDB SRV connection uri"
