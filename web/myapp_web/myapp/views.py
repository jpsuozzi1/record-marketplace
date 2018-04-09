from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import urllib.request
import urllib.parse
import json
from .forms import *

def home(request):
    # Display home page

    # Grab Json data for the most recent two listings and display them nicely
    req = urllib.request.Request('http://exp-api:8000/api/v1/recentListings/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if not resp['ok']:
        return HttpResponse("Error: Listing not found")

    return render(request, 'home.html',
    {
        'listing0':resp['listings'][0],
        'listing1':resp['listings'][1],
    })


def listing(request, listing_id):
    # make a GET request and parse the returned JSON
    # note, no timeouts, error handling or all the other things needed to do this for real
    #print ("About to perform the GET request...")

    url = 'http://exp-api:8000/api/v1/listingDetails/' + listing_id + '/'
    req = urllib.request.Request(url)

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if not resp['ok']:
        return HttpResponse("Error: Listing not found")

    # Grab all of the listing information, minus songs
    context = {
        'listing_id': listing_id,
        'record':resp['listings'][0]['record'],
        'date_posted':resp['listings'][0]['date_posted'],
        'seller':resp['listings'][0]['seller'],
        'buyer':resp['listings'][0]['buyer'],
        'price':resp['listings'][0]['price'],
        'songs':resp['listings'][0]['songs'],
    }

    return render(request, 'listing.html', context)

def createAccount(request):
    # Display form to create a new user account
    if (request.method == 'POST'):
        form = CreateUser(request.POST)
        if (form.is_valid()):
            data = urllib.parse.urlencode(request.POST).encode('utf-8')            
            url = 'http://exp-api:8000/api/v1/createAccount/'
            req = urllib.request.Request(url, data=data, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')            
            resp = json.loads(resp_json)
            if not resp['ok']:
                return HttpResponse("User could not be created")

            return redirect('login')
    else:
        form = CreateUser()

    return render(request, 'createAccount.html', {'form': form})

def login(request):
    # Display form to log a user in
    # if (request.method == 'POST'):
    #     form = LoginUser(request.POST)
    #     if (form.is_valid()):
    #         data = urllib.parse.urlencode(request.POST).encode('utf-8')
    #         url = 'http://exp-api:8000/api/v1/login/'

    #         req = urllib.request.Request(url, data=data, method='POST')
    #         resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            
    #         resp = json.loads(resp_json)
    #         if not resp['ok']:
    #             return HttpResponse("User could not be logged in")

    #         return redirect('home')
    # else:
    form = LoginUser()

    return render(request, 'login.html', {'form': form})

def logout(request):
    # Handle logout request and display results

    return render(request, 'logout.html', {})
