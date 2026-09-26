# search.py
import sys
import os
from dotenv import load_dotenv
import json
import redis
from mongoengine import connect
from models import Author, Quote

# Connection details
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Initialize Redis client (adjust host/port/password if using Redis Cloud)
redis_client = redis.Redis(host='localhost', port=6381, password='MySecurePassword123!', db=0, decode_responses=True)

def connect_db():
    connect(host=MONGO_URI)

def search_by_author(name_query):
    # Check cache first
    cache_key = f"author:{name_query.strip().lower()}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        print("[FROM CACHE]")
        return json.loads(cached_result)

    # Regex search for partial matching (e.g. "st" -> case-insensitive start or substring)
    authors = Author.objects(fullname__icontains=name_query.strip())
    if not authors:
        return []

    quotes = Quote.objects(author__in=authors)
    results = [q.quote for q in quotes]

    # Store result in Redis cache (TTL: 3600 seconds)
    redis_client.set(cache_key, json.dumps(results, ensure_ascii=False), ex=3600)
    print("[FROM MONODB]")
    return results

def search_by_tag(tag_query):
    # Check cache first
    cache_key = f"tag:{tag_query.strip().lower()}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        print("[FROM CACHE]")
        return json.loads(cached_result)

    # Regex search for tag starting with or containing tag_query
    quotes = Quote.objects(tags__icontains=tag_query.strip())
    results = [q.quote for q in quotes]

    # Store result in Redis cache
    redis_client.set(cache_key, json.dumps(results, ensure_ascii=False), ex=3600)
    print("[FROM MONODB]")
    return results

def search_by_tags(tags_query):
    # Parse comma-separated tags
    tags_list = [t.strip() for t in tags_query.split(',') if t.strip()]
    if not tags_list:
        return []

    # Check cache first
    cache_key = f"tags:{','.join(sorted(tags_list)).lower()}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        print("[FROM CACHE]")
        return json.loads(cached_result)

    # Retrieve quotes matching ANY of the listed tags (__in operator)
    quotes = Quote.objects(tags__in=tags_list)
    results = [q.quote for q in quotes]

    # Store result in Redis cache
    redis_client.set(cache_key, json.dumps(results, ensure_ascii=False), ex=3600)
    print("[FROM MONODB]")
    return results

def main():
    connect_db()
    # Force UTF-8 encoding for standard stdout output
    sys.stdout.reconfigure(encoding='utf-8')

    print("Quote Search Engine Started. Enter commands like 'name: Steve Martin', 'name:st', 'tag:life', 'tags:life,live'.")
    print("Type 'exit' or 'exit:' to quit.\n")

    while True:
        try:
            user_input = input("Enter command: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ('exit', 'exit:'):
                print("Exiting search script.")
                break

            if ':' not in user_input:
                print("Invalid format. Use 'command: value' (e.g., name: Steve Martin)")
                continue

            cmd, value = user_input.split(':', 1)
            cmd = cmd.strip().lower()
            value = value.strip()

            results = []
            if cmd == 'name':
                results = search_by_author(value)
            elif cmd == 'tag':
                results = search_by_tag(value)
            elif cmd == 'tags':
                results = search_by_tags(value)
            else:
                print(f"Unknown command: '{cmd}'. Supported commands: name, tag, tags, exit.")
                continue

            # Output results in pure UTF-8 string format
            if results:
                for idx, q in enumerate(results, 1):
                    # Ensure UTF-8 output print
                    print(f"{idx}. {q.encode('utf-8').decode('utf-8')}")
            else:
                print("No quotes found.")

            print("-" * 50)

        except KeyboardInterrupt:
            print("\nExiting search script.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()