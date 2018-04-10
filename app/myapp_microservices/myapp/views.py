from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password, make_password
import myapp_microservices.settings as settings
import os
import hmac
import datetime
from myapp.models import *
from myapp.forms import *
import json
from types import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def create(request, model):
    #Create a new object of type model
    try:
        if (model == 'users'):
           newObj = UserForm(request.POST)
           obj = newObj.save(commit=False)
           obj.passwordHash = make_password(request.POST['passwordHash'])
        elif (model == 'artists'):
            newObj = ArtistForm(request.POST)
        elif (model == 'records'):
            newObj = RecordForm(request.POST)
        elif (model == 'songs'):
            newObj = SongForm(request.POST)
        elif (model == 'listings'):
            auth = request.POST['cookie']
            authUser = Authenticator.objects.get(pk=auth)
            user = User.objects.get(pk=authUser.user_id)
            newObj = ListingForm(request.POST)
            obj = newObj.save(commit=False)
            obj.record = Record.objects.get(name=request.POST['recordName'])
            obj.buyer = user
            obj.seller = user
            obj.date_posted= datetime.date.today()
        elif (model == 'genres'):
            newObj = GenreForm(request.POST)
        elif (model == 'authenticators'):
            newObj = AuthenticatorForm(request.POST)
        if (newObj.is_valid()):
            o = newObj.save()
            data = model_to_dict(o)
        else:
            data = newObj.errors
        if (model == 'songs'):
            data['duration'] = str(data['duration'])
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
            o = User.objects.get(pk=model_id)
        elif (model == 'artists'):
            o = Artist.objects.get(pk=model_id)
        elif (model == 'records'):
            o = Record.objects.get(pk=model_id)
        elif (model == 'songs'):
            o = Song.objects.get(pk=model_id)
        elif (model == 'listings'):
            o = Listing.objects.get(pk=model_id)
        elif (model == 'genres'):
            o = Genre.objects.get(pk=model_id)
        elif (model == 'authenticators'):
            o = Authenticator.objects.get(pk=model_id)
        data = model_to_dict(o)
        if (model == 'songs'):
            data['duration'] = str(data['duration'])
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
            obj = User.objects.get(pk=model_id)
            first_name = request.POST.get('first_name', obj.first_name)
            last_name = request.POST.get('last_name', obj.last_name)
            email = request.POST.get('email', obj.email)
            password = request.POST.get('passwordHash', obj.passwordHash)
            obj = User(id=model_id, first_name=first_name, last_name=last_name, email=email, passwordHash=password)
        elif (model == 'artists'):
            obj = Artist.objects.get(pk=model_id)
            name = request.POST.get('name', obj.name)
            obj = Artist(id=model_id, name=name)
        elif (model == 'records'):
            obj = Record.objects.get(pk=model_id)
            artist_id = request.POST.get('artist', obj.artist.id)
            artist = Artist.objects.get(pk=artist_id)
            name = request.POST.get('name', obj.name)
            release_date = request.POST.get('release_date', obj.release_date)
            pressing = request.POST.get('pressing', obj.pressing)
            obj = Record(id=model_id, artist=artist, name=name, release_date=release_date, pressing=pressing)
        elif (model == 'songs'):
            obj = Song.objects.get(pk=model_id)
            name = request.POST.get('name', obj.name)
            duration = request.POST.get('duration', str(obj.duration))
            durStr = datetime.datetime.strptime(duration, "%H:%M:%S")
            dur = datetime.timedelta(hours=durStr.hour, minutes=durStr.minute, seconds=durStr.second)
            artist_id = request.POST.get('artist', obj.artist.id)
            artist = Artist.objects.get(pk=artist_id)
            record_id = request.POST.get('record', obj.record.id)
            record = Record.objects.get(pk=record_id)
            obj = Song(id=model_id, name=name, duration=dur, artist=artist, record=record)
        elif (model == 'listings'):
            obj = Listing.objects.get(pk=model_id)
            price = request.POST.get('price', obj.price)
            seller_id = request.POST.get('seller', obj.seller.id)
            seller = User.objects.get(pk=seller_id)
            buyer_id = request.POST.get('buyer', obj.buyer.id)
            buyer = User.objects.get(pk=buyer_id)
            record_id = request.POST.get('record', obj.record.id)
            record = Record.objects.get(pk=record_id)
            date_posted = request.POST.get('date_posted', obj.date_posted)
            obj = Listing(id=model_id, price=price, seller=seller, buyer=buyer, record=record, date_posted=date_posted)
        elif (model == 'genres'):
            obj = Genre.objects.get(pk=model_id)
            record_id = request.POST.get('record', obj.record.id)
            record = Record.objects.get(pk=record_id)
            name = request.POST.get('name', obj.name)
            obj = Genre(id=model_id, record=record, name=name)
        elif (model == 'authenticators'):
            obj = Authenticator.objects.get(pk=model_id)
            user_id = request.POST.get('user_id', obj.user_id)
            authenticator = request.POST.get('authenticator', obj.authenticator)
            date_created = request.POST.get('date', obj.date_created)
            obj = Authenticator(user_id=user_id,authenticator=authenticator,date_created=date_created)
        obj.save()
        data = model_to_dict(obj)
        if (model == 'songs'):
            data['duration'] = str(data['duration'])
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
            obj = User.objects.get(pk=model_id)
        elif (model == 'artists'):
            obj = Artist.objects.get(pk=model_id)
        elif (model == 'records'):
            obj = Record.objects.get(pk=model_id)
        elif (model == 'songs'):
            obj = Song.objects.get(pk=model_id)
        elif (model == 'listings'):
            obj = Listing.objects.get(pk=model_id)
        elif (model == 'genres'):
            obj = Genre.objects.get(pk=model_id)
        elif (model == 'authenticators'):
            obj = Authenticator.objects.get(pk=model_id)
        data = model_to_dict(obj)
        if (model == 'songs'):
            data['duration'] = str(data['duration'])
        obj.delete()
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
            songData = model_to_dict(s)
            songData['duration'] = str(songData['duration'])
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
        listingData = model_to_dict(l)
        data.append(listingData)
    result = {
        'ok': True,
        'data': data
    }
    return JsonResponse(result)

def allRecords(request):
    records = Record.objects.all()
    data = []
    for r in records:
        recordData = model_to_dict(r)
        data.append(recordData)
    result = {
        'ok': True,
        'data': data
    }
    return JsonResponse(result)

# Check username and password, return authenticator
@require_POST
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = User.objects.get(email=email) # Raises exception if not found

    except: # User not found
        user = None
    data = {}
    ok = False
    if user is None:
        data['error'] = "User not found"

    elif check_password(password, user.passwordHash):
        #Password success
        ok = True
        authenticator = hmac.new(
            key = settings.SECRET_KEY.encode('utf-8'),
            msg = os.urandom(32),
            digestmod = 'sha256',
        ).hexdigest()
        auth = Authenticator()
        auth.user_id = user.id
        auth.authenticator = authenticator.encode('utf-8')
        auth.date_created = datetime.date.today()
        auth.save()
        data['auth'] = authenticator

    else:
        #Password fail
        data['error'] = "Invalid password"
    result = {
        'ok': ok,
        'data': data
    }
    return JsonResponse(result)

# Logout a user by deleting their authenticator
def logout(request):

    auth = request.POST['auth']
    # Delete the associated authenticator
    try:
        obj = Authenticator.objects.get(pk=auth)
        data = model_to_dict(obj)
        obj.delete()
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
