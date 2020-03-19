from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views import View

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
    key = settings.TMDB_API_KEY
    playlists = list()

    for playlist in request.user.playlist_set.all() :
        pl = {
            'id': str(playlist.uid),
            'title': playlist.title,
            'username': playlist.creator.username,
            'created_date': round(datetime.timestamp(playlist.created_date) * 1000),
            'updated_date': round(datetime.timestamp(playlist.updated_date) * 1000),
            'items_count' : playlist.playlistitem_set.all().count(),
            'items' : list()
        }

        for item in playlist.playlistitem_set.all() :
            if item.media_type == 'movie' :
                url = f'https://api.themoviedb.org/3/movie/{item.item_id}?api_key={key}'
            elif item.media_type == 'tv' :
                url = f'https://api.themoviedb.org/3/tv/{item.item_id}?api_key={key}'

            res = fetcher.get(url)
            result = json.loads(res.text)
            pl['items'].append(result)

        playlists.append(pl)

    context = json.dumps(playlists) 
    return HttpResponse(context, content_type='application/json')

class deleteItemFromPlaylist(View) :
    def post(self, request, id) :
        item_id = request.POST.get('item_id')
        try :
            playlist = Playlist.objects.get(pk=id) 
            item = playlist.playlistitem_set.get(item_id=item_id)
            item.delete()
            return HttpResponse(f'item {item_id} delete from {playlist.title}', status=201)
        except Exception as ex :
            return HttpResponse(ex, status=403)
