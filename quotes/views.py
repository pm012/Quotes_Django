import sys
import os
from django.shortcuts import render
#from models import Quote, Author


# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hw10_django.utils import conect

#import logging

#logger = logging.getLogger(__name__)

# Create your views here.
def main(request):
    db = conect.get_mongo_connection()
    #logger.info("------------"+str(db))
    quotes = db.quote.find()
    #quotes = Quote.objects.all()
    
    return render(request, 'quotes/index.html', context={'quotes': quotes})
    

if __name__ == "__main__":
    db = conect.get_mongo_connection()
    quotes = db.quote.find()
    #quotes = Quote.objects.all()
    for quote in quotes:
        print(quote)
