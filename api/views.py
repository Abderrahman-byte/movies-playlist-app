from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import requests as fetcher
import json
from datetime import datetime

# Create your views here.
from main.models import Playlist, PlaylistItem

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
            result = {'media_type': item.media_type, **result}
            pl['items'].append(result)

        playlists.append(pl)

    context = json.dumps(playlists) 
    return HttpResponse(context, content_type='application/json')

@csrf_exempt
def deleteItemFromPlaylist(request, id) :
    if request.method == 'POST' :
        body = json.loads(request.body)
        item_id = str(body['item_id'])
        media_type = body['media_type']

        try :
            playlist = Playlist.objects.get(pk=id) 
            item = playlist.playlistitem_set.get(item_id=item_id, media_type=media_type)
            item.delete()
            return HttpResponse(f'item {item_id} deleted from {playlist.title}', status=201)
        except Exception as ex :
            return HttpResponse(ex, status=403)

@csrf_exempt
def deletePlaylist(request, id) :
    if request.method == 'POST' :
        try :
            playlist = Playlist.objects.get(pk=id)
            playlist.delete()
            return HttpResponse(f'playlist {id} deleted', status=201)
        except Exception as ex :
            return HttpResponse(ex, status=403)

def PlaylistLiteView(request) :
    playlists = request.user.playlist_set.all()
    context = [
        {
            'uid': str(playlist.uid),
            'title': playlist.title,
            'items_count': playlist.playlistitem_set.all().count()
        } for playlist in playlists
    ]

    context = json.dumps(context)
    return HttpResponse(context, content_type='application/json')

@csrf_exempt
def addToPlaylistView(request, id) :
    if request.method == 'POST' :
        body = json.loads(request.body)
        item_id = body['item_id']
        media_type = body['media_type']

        try :
            playlist = Playlist.objects.get(pk=id)
            PlaylistItem(item_id=item_id, media_type=media_type, playlist=playlist).save()
        except :
            pass

        return HttpResponse('Done', 201)