from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.forms.models import model_to_dict
import datetime
from myapp.models import *
import json
from types import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def create(request, model):
    #Create a new object of type model
    try:
        if (model == 'users'):
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['passwordHash']
            u = User(first_name=first_name, last_name=last_name, email=email, passwordHash=password)
            u.save()
            data = {
                'id': u.id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'passwordHash': password
            }
        elif (model == 'artists'):
            name = request.POST['name']
            a = Artist(name=name)
            a.save()
            data = {
                'id': a.id,
                'name': name
            }
        elif (model == 'records'):
            artist_id = request.POST['artist']
            artist = Artist.objects.get(pk=artist_id)
            name = request.POST['name']
            release_date = request.POST['release_date']
            pressing = request.POST['pressing']
            r = Record(artist=artist, name=name, release_date=release_date, pressing=pressing)
            r.save()
            data = {
                'id': r.id,
                'artist_id': artist_id,
                'name': name,
                'release_date': release_date,
                'pressing': pressing
            }
        elif (model == 'songs'):
            name = request.POST['name']
            duration = datetime.datetime.strptime(request.POST['duration'], "%H:%M:%S")
            dur = datetime.timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
            artist_id = request.POST['artist']
            artist = Artist.objects.get(pk=artist_id)
            record_id = request.POST['record']
            record = Record.objects.get(pk=record_id)
            s = Song(name=name, duration=dur, artist=artist, record=record)
            s.save()
            data = {
                'id': s.id,
                'name': name,
                'duration': "%d:%d:%d" % (duration.hour, duration.minute, duration.second),
                'artist_id': artist_id,
                'record_id': record_id
            }
        elif (model == 'listings'):
            price = request.POST['price']
            seller_id = request.POST['seller']
            seller = User.objects.get(pk=seller_id)
            buyer_id = request.POST['buyer']
            buyer = User.objects.get(pk=buyer_id)
            record_id = request.POST['record']
            record = Record.objects.get(pk=record_id)
            date_posted = request.POST['date_posted']
            l = Listing(price=price, seller=seller, buyer=buyer, record=record, date_posted=date_posted)
            l.save()
            data = {
                'id': l.id,
                'price': price,
                'seller_id': seller_id,
                'buyer_id': buyer_id,
                'record_id': record_id,
                'date_posted': date_posted
            }
        elif (model == 'genres'):
            record_id = request.POST['record']
            record = Record.objects.get(pk=record_id)
            name = request.POST['name']
            g = Genre(record=record, name=name)
            g.save()
            data = {
                'id': g.id,
                'record_id': record_id,
                'name': name
            }
        result = {
            'ok': True,
            'data': data
        }

    except ObjectDoesNotExist:
        result = {
            'ok': False,
            'data': ""
        }
    return JsonResponse(result)

@require_GET
def read(request, model, model_id):
    #Read model_id of type model
    try:
        if (model == 'users'):
            u = User.objects.get(pk=model_id)
            data = {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email,
                'passwordHash': u.passwordHash
            }
        elif (model == 'artists'):
            a = Artist.objects.get(pk=model_id)
            data = {
                'id': a.id,
                'name': a.name
            }
        elif (model == 'records'):
            r = Record.objects.get(pk=model_id)
            data = {
                'id': r.id,
                'artist_id': r.artist.id,
                'name': r.name,
                'release_date': r.release_date,
                'pressing': r.pressing
            }
        elif (model == 'songs'):
            s = Song.objects.get(pk=model_id)
            data = {
                'id': s.id,
                'name': s.name,
                'duration': str(s.duration),
                'artist_id': s.artist.id,
                'record_id': s.record.id
            }
        elif (model == 'listings'):
            l = Listing.objects.get(pk=model_id)
            data = {
                'id': l.id,
                'price': l.price,
                'seller_id': l.seller.id,
                'buyer_id': l.buyer.id,
                'record_id': l.record.id,
                'date_posted': l.date_posted
            }
        elif (model == 'genres'):
            g = Genre.objects.get(pk=model_id)
            data = {
                'id': g.id,
                'record_id': g.record.id,
                'name': g.name
            }
        result = {
            'ok': True,
            'data': data
        }
    except ObjectDoesNotExist:
        result = {
            'ok': False,
            'data': ""
        }
    return JsonResponse(result)

@require_POST
def update(request, model, model_id):
    #Update model_id of type model
    try:
        if (model == 'users'):
            u = User.objects.get(pk=model_id)
            first_name = request.POST.get('first_name', u.first_name)
            last_name = request.POST.get('last_name', u.last_name)
            email = request.POST.get('email', u.email)
            password = request.POST.get('passwordHash', u.passwordHash)
            u = User(id=model_id, first_name=first_name, last_name=last_name, email=email, passwordHash=password)
            u.save()
            data = {
                'id': u.id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'passwordHash': password
            }
        elif (model == 'artists'):
            a = Artist.objects.get(pk=model_id)
            name = request.POST.get('name', a.name)
            a = Artist(id=model_id, name=name)
            a.save()
            data = {
                'id': a.id,
                'name': name
            }
        elif (model == 'records'):
            r = Record.objects.get(pk=model_id)
            artist_id = request.POST.get('artist', r.artist.id)
            artist = Artist.objects.get(pk=artist_id)
            name = request.POST.get('name', r.name)
            release_date = request.POST.get('release_date', r.release_date)
            pressing = request.POST.get('pressing', r.pressing)
            r = Record(id=model_id, artist=artist, name=name, release_date=release_date, pressing=pressing)
            r.save()
            data = {
                'id': r.id,
                'artist_id': artist_id,
                'name': name,
                'release_date': release_date,
                'pressing': pressing
            }
        elif (model == 'songs'):
            s = Song.objects.get(pk=model_id)
            name = request.POST.get('name', s.name)
            duration = request.POST.get('duration', str(s.duration))
            durStr = datetime.datetime.strptime(duration, "%H:%M:%S")
            dur = datetime.timedelta(hours=durStr.hour, minutes=durStr.minute, seconds=durStr.second)
            artist_id = request.POST.get('artist', s.artist.id)
            artist = Artist.objects.get(pk=artist_id)
            record_id = request.POST.get('record', s.record.id)
            record = Record.objects.get(pk=record_id)
            s = Song(id=model_id, name=name, duration=dur, artist=artist, record=record)
            s.save()
            data = {
                'id': s.id,
                'name': name,
                'duration': "%d:%d:%d" % (durStr.hour, durStr.minute, durStr.second),
                'artist_id': artist_id,
                'record_id': record_id
            }
        elif (model == 'listings'):
            l = Listing.objects.get(pk=model_id)
            price = request.POST.get('price', l.price)
            seller_id = request.POST.get('seller', l.seller.id)
            seller = User.objects.get(pk=seller_id)
            buyer_id = request.POST.get('buyer', l.buyer.id)
            buyer = User.objects.get(pk=buyer_id)
            record_id = request.POST.get('record', l.record.id)
            record = Record.objects.get(pk=record_id)
            date_posted = request.POST.get('date_posted', l.date_posted)
            l = Listing(id=model_id, price=price, seller=seller, buyer=buyer, record=record, date_posted=date_posted)
            l.save()
            data = {
                'id': l.id,
                'price': price,
                'seller_id': seller_id,
                'buyer_id': buyer_id,
                'record_id': record_id,
                'date_posted': date_posted
            }
        elif (model == 'genres'):
            g = Genre.objects.get(pk=model_id)
            record_id = request.POST.get('record', g.record.id)
            record = Record.objects.get(pk=record_id)
            name = request.POST.get('name', g.name)
            g = Genre(id=model_id, record=record, name=name)
            g.save()
            data = {
                'id': g.id,
                'record_id': record_id,
                'name': name
            }

        result = {
            'ok': True,
            'data': data
        }
    except ObjectDoesNotExist:
        result = {
            'ok': False,
            'data': ""
        }

    return JsonResponse(result)

@require_POST
def delete(request, model, model_id):
    #Delete model_id of type model
    try:
        if (model == 'users'):
            u = User.objects.get(pk=model_id)
            data = {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email,
                'passwordHash': u.passwordHash
            }
            u.delete()
        elif (model == 'artists'):
            a = Artist.objects.get(pk=model_id)
            data = {
                'id': a.id,
                'name': a.name
            }
            a.delete()
        elif (model == 'records'):
            r = Record.objects.get(pk=model_id)
            data = {
                'id': r.id,
                'artist_id': r.artist.id,
                'name': r.name,
                'release_date': r.release_date,
                'pressing': r.pressing
            }
            r.delete()
        elif (model == 'songs'):
            s = Song.objects.get(pk=model_id)
            data = {
                'id': s.id,
                'name': s.name,
                'duration': json.dumps(s.duration, default=str),
                'artist_id': s.artist.id,
                'record_id': s.record.id
            }
            s.delete()
        elif (model == 'listings'):
            l = Listing.objects.get(pk=model_id)
            data = {
                'id': l.id,
                'price': l.price,
                'seller_id': l.seller.id,
                'buyer_id': l.buyer.id,
                'record_id': l.record.id,
                'date_posted': l.date_posted
            }
            l.delete()
        elif (model == 'genres'):
            g = Genre.objects.get(pk=model_id)
            data = {
                'id': g.id,
                'record_id': g.record.id,
                'name': g.name
            }
            g.delete()
        result = {
            'ok': True,
            'data': data
        }
    except ObjectDoesNotExist:
        result = {
            'ok': False,
            'data': ""
        }
    return JsonResponse(result)

# Return all songs of a given record
def allSongsOnRecord(request, model_id):
    try:
        r = Record.objects.get(pk=model_id)
        songList = r.songLists
        songs = []
        for s in songList:
            songData = {
                'id': s.id,
                'name': s.name,
                'duration': str(s.duration),
                'artist_id': s.artist.id,
                'record_id': s.record.id
            }
            songs.append(songData)

        result = {
            'ok': True,
            'data': songs
        }
    except ObjectDoesNotExist:
        result = {
            'ok': False,
            'data': ""
        }
    return JsonResponse(result)

# Return all listings
def allListings(request):
    listings = Listing.objects.all()
    data = []
    for l in listings:
        listingData = {
                'id': l.id,
                'price': l.price,
                'seller_id': l.seller.id,
                'buyer_id': l.buyer.id,
                'record_id': l.record.id,
                'date_posted': l.date_posted
            }
        data.append(listingData)
    result = {
        'ok': True,
        'data': data
    }
    return JsonResponse(result)
