from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

import requests as fetcher
import json
from datetime import datetime

# Create your views here.
from main.models import Playlist

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

def playlistsApi(request) :
    playlists = list()

    for playlist in request.user.playlist_set.all() :
        pl = {
            'title': playlist.title,
            'username': playlist.creator.username,
            'created_date': round(datetime.timestamp(playlist.created_date) * 1000),
            'updated_date': round(datetime.timestamp(playlist.updated_date) * 1000),
            'items' : list()
        }
        
        print(playlist.playlistitem_set.all())

        playlists.append(pl)

    print(playlists)
    context = {}
    context = json.dumps(context) 
    return HttpResponse(context, content_type='application/json')