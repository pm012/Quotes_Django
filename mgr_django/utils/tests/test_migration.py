import pytest
from unittest.mock import MagicMock, patch
from mgr_django.utils.conect import get_mongo_connection_uri
from mgr_django.utils.migration import migrate_data
from quotes.models import Author, Quote, Tag


def test_get_mongo_connection_uri():
    db_name, uri = get_mongo_connection_uri()
    assert db_name is not None
    assert uri.startswith("mongodb")


@pytest.mark.django_db
@patch('mgr_django.utils.migration.get_mongo_connection')
def test_migrate_data(mock_get_mongo):
    # Mocking collections of MongoDB
    mock_db = MagicMock()
    mock_get_mongo.return_value = mock_db

    mock_db.authors.find.return_value = [{
        'fullname': 'Mocked Author',
        'born_date': 'Jan 1, 1900',
        'born_location': 'Mock City',
        'description': 'Mock Desc'
    }]
    
    mock_db.quotes.find.return_value = [{
        '_id': '12345',
        'quote': 'Mocked Quote Text',
        'author': '12345',
        'tags': ['mocktag']
    }]
    
    mock_db.authors.find_one.return_value = {'fullname': 'Mocked Author'}

    migrate_data()

    assert Author.objects.filter(fullname='Mocked Author').exists()
    assert Tag.objects.filter(name='mocktag').exists()
    assert Quote.objects.filter(quote='Mocked Quote Text').exists()