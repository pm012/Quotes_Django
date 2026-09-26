# load_data.py
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from mongoengine import connect

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mgr_django.utils.scrapped_json_to_mongo.models import Author, Quote
from mgr_django.utils.conect import get_mongo_connection_uri

MONGO_URI = get_mongo_connection_uri()[1]

# Define a folder where current script is located quotes_and_authors_to_mongoDB.py
CURRENT_DIR = Path(__file__).resolve().parent

# Go level up and enter scraping/json/
JSON_DIR = CURRENT_DIR.parent / 'scraping' / 'json'

# Формуємо фінальні шляхи до файлів
authors_file = JSON_DIR / 'authors.json'
quotes_file = JSON_DIR / 'quotes.json'


def import_data():
    # 1. Connect to MongoDB Atlas
    connect(host=MONGO_URI)

    # Clear existing collections to avoid duplicates on re-runs
    Author.objects.delete()
    Quote.objects.delete()

    # 2. Load and insert Authors
    with open(authors_file, 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        for data in authors_data:
            author = Author(
                fullname=data.get('fullname'),
                born_date=data.get('born_date'),
                born_location=data.get('born_location'),
                description=data.get('description')
            )
            author.save()

    print("Authors successfully imported.")

    # 3. Load and insert Quotes
    with open(quotes_file, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for data in quotes_data:
            # Find the referenced author document by name
            author_obj = Author.objects(fullname=data.get('author')).first()
            if author_obj:
                quote = Quote(
                    tags=data.get('tags', []),
                    author=author_obj,  # Stores the ObjectId reference automatically
                    quote=data.get('quote')
                )
                quote.save()

    print("Quotes successfully imported.")

if __name__ == '__main__':
    import_data()
   