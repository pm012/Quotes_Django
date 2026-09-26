import os
import sys
from pathlib import Path

# Add the project root to sys.path for correct import
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mgr_django.settings")

import django
django.setup()

from django.db import transaction
from quotes.models import Quote, Tag, Author
from mgr_django.utils.conect import get_mongo_connection



def migrate_data():
    try:
        db = get_mongo_connection()
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return

    authors_mongo = list(db.author.find())
    quotes_mongo = list(db.quote.find())

    print(f"Found {len(authors_mongo)} authors and {len(quotes_mongo)} quotes in MongoDB.")

    with transaction.atomic():
        # 1. Migration of authors
        for author in authors_mongo:
            Author.objects.get_or_create(
                fullname=author.get('fullname', '').strip(),
                defaults={
                    'born_date': author.get('born_date', ''),
                    'born_location': author.get('born_location', ''),
                    'description': author.get('description', '')
                }
            )
        print("Authors migration complete.")

        # 2. Migration of quotes and tags
        for quote in quotes_mongo:
            tags_objs = []
            for tag_name in quote.get('tags', []):
                t_obj, _ = Tag.objects.get_or_create(name=tag_name.strip().lower())
                tags_objs.append(t_obj)

            quote_text = quote.get('quote', '').strip()
            if not Quote.objects.filter(quote=quote_text).exists():
                author_data = db.author.find_one({'_id': quote['author']})
                author_obj = None
                
                if author_data:
                    author_obj = Author.objects.filter(
                        fullname=author_data.get('fullname', '').strip()
                    ).first()

                q_obj = Quote.objects.create(
                    quote=quote_text,
                    author=author_obj
                )
                q_obj.tags.add(*tags_objs)

        print("Quotes migration complete.")


if __name__ == "__main__":
    migrate_data()