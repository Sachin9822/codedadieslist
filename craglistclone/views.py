from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAGLIST_URL = 'https://pune.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL ='https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.
def home(request):
    return render (request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    print(search)
    models.Search.objects.create(search=search)
    final_url = BASE_CRAGLIST_URL.format(quote_plus(search))
    
    response_ = requests.get(final_url)
    data_ = response_.text
    
    
    soup = BeautifulSoup(data_, features='html.parser')
    post_listing = soup.find_all('li',{'class':'result-row'})
    
    final_posting = []

    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')      
        if post.find(class_='result-price'):
           post_prize = post.find(class_='result-price').text
        else:
            post_prize = "N/A"
        


        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        
        final_posting.append((post_title,post_url,post_prize,post_image_url))
    
    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting,
    }
    return render(request, 'craglistclone/new_search.html', stuff_for_frontend)