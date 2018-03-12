from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import urllib.request
import urllib.parse
import json


def home(request): 
    # Display home page

    # Grab Json data for the most recent two listings and display them nicely
    req = urllib.request.Request('http://exp-api:8000/api/v1/recentListings/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    return render(request, 'home.html',
    {   'record0':resp['listings'][0]['record'],
        'date_posted0':resp['listings'][0]['date_posted'],
        'seller0':resp['listings'][0]['seller'],
        'buyer0':resp['listings'][0]['buyer'],
        'price0':resp['listings'][0]['price'],
        'record1':resp['listings'][1]['record'],
        'date_posted1':resp['listings'][1]['date_posted'],
        'seller1':resp['listings'][1]['seller'],
        'buyer1':resp['listings'][1]['buyer'],
        'price1':resp['listings'][1]['price'],
    })
    

def listing(request, listing_id):
    # make a GET request and parse the returned JSON
    # note, no timeouts, error handling or all the other things needed to do this for real
    #print ("About to perform the GET request...")

    url = 'http://exp-api:8000/api/v1/listingDetails/' + listing_id + '/'
    req = urllib.request.Request(url)

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    

    return render(request, 'listing.html', 
    {   
        'listing_id': listing_id,
        'record':resp['listings'][0]['record'],
        'date_posted':resp['listings'][0]['date_posted'],
        'seller':resp['listings'][0]['seller'],
        'buyer':resp['listings'][0]['buyer'],
        'price':resp['listings'][0]['price'],
        'song0':resp['listings'][0]['songs'][0]['name'],
        'duration0':resp['listings'][0]['songs'][0]['duration'],
        'song1':resp['listings'][0]['songs'][1]['name'],
        'duration1':resp['listings'][0]['songs'][1]['duration'],

    })
