from django.shortcuts import render
from hw10_django.utils import conect
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def main(request):
    db = conect.get_mongo_connection()
    quotes = db.quote.find()
    logger.info("------------"+quotes)
    return render(request, 'quotes/index.html', context ={'quotes': quotes})
    

if __name__ == "__main__":
    db = conect.get_mongo_connection()
    quotes = db.quotes.find()
    print(quotes)