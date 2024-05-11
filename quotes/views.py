from django.shortcuts import render
from django.core.paginator import Paginator

from hw10_django.utils import conect


# Create your views here.
def main(request, page=1):
    db = conect.get_mongo_connection()    
    quotes = db.quote.find()
    #quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})
    

if __name__ == "__main__":
    db = conect.get_mongo_connection()
    quotes = db.quote.find()
    #quotes = Quote.objects.all()
    for quote in quotes:
        print(quote)
