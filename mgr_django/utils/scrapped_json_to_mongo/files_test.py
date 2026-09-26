
import os
import json
from dotenv import load_dotenv

load_dotenv()

file_path = os.path.join(os.path.dirname(__file__), 'authors.json')
Mongo_URI = os.getenv("MONGO_URI")
print(f"Mongo_URI: {Mongo_URI}")


# with open(file_path, 'r', encoding='utf-8') as f:
#         authors_data = json.load(f)
#         for data in authors_data:
#             print(f"Author: {data.get('fullname')}, Born: {data.get('born_date')}, Location: {data.get('born_location')}, Description: {data.get('description')}")