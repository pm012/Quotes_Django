import re
from unittest.mock import Mock, patch

from mgr_django.utils.conect import get_mongo_connection, get_mongo_connection_uri


def test_connect_exception():
    client = Mock()
    client.admin.command.side_effect = Exception("Connection error")
    with patch('mgr_django.utils.conect.MongoClient', return_value=client):
        try:
            get_mongo_connection()
        except Exception as error:
            assert str(error) == "Connection error"
        else:
            raise AssertionError("Expected the MongoDB ping to fail.")


def test_get_uri():
    db_name, uri = get_mongo_connection_uri()
    assert isinstance(db_name, str)
    assert re.match(r'^mongodb(\+srv)?://', uri)
