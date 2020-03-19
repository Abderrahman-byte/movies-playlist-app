from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

import requests as fetcher
import json

# Create your views here.
def trendingApi(request) :
    page = request.GET.get('page', 1)
    key = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/trending/all/day?api_key={key}&page={page}'

    if int(page) > 1000 :
        context = {
            'status': '404', 
            'results': 'Invalid page: Pages start at 1 and max at 1000. They are expected to be an integer.'
        }

        context = json.dumps(context)
        return HttpResponse(context, content_type='applications/json', status=404)

    res = fetcher.get(url)
    return HttpResponse(res.text, content_type='application/json')
