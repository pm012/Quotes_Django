import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mgr_django.settings")

import django
django.setup()

from django.db import transaction
from quotes.models import Quote, Tag, Author
from mgr_django.utils.conect import get_mongo_connection


def migrate_data():
    db = get_mongo_connection()
    print(f"Connected to MongoDB database: '{db.name}' successfully.")

    # Call callections as documents are called: authors та quotes
    authors_mongo = list(db.authors.find())
    quotes_mongo = list(db.quotes.find())

    print(f"Found {len(authors_mongo)} authors and {len(quotes_mongo)} quotes in MongoDB.")

    with transaction.atomic():
        authors_by_id: dict[object, Author] = {}

        # 1. Міграція авторів
        for author in authors_mongo:
            author_obj, _ = Author.objects.get_or_create(
                fullname=author.get('fullname', '').strip(),
                defaults={
                    'born_date': author.get('born_date', ''),
                    'born_location': author.get('born_location', ''),
                    'description': author.get('description', '')
                }
            )
            authors_by_id[author['_id']] = author_obj
        print("Authors migration complete.")

        # 2. Migration of quotes and tags
        tags_by_name: dict[str, Tag] = {}
        for quote in quotes_mongo:
            tags_objs = []
            for tag_name in quote.get('tags', []):
                normalized_name = tag_name.strip().lower()
                if normalized_name not in tags_by_name:
                    tags_by_name[normalized_name], _ = Tag.objects.get_or_create(
                        name=normalized_name
                    )
                tags_objs.append(tags_by_name[normalized_name])

            quote_text = quote.get('quote', '').strip()
            if not Quote.objects.filter(quote=quote_text).exists():
                q_obj = Quote.objects.create(
                    quote=quote_text,
                    author=authors_by_id.get(quote.get('author'))
                )
                q_obj.tags.add(*tags_objs)

        print("Quotes migration complete.")


if __name__ == "__main__":
    migrate_data()