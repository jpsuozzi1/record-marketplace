from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import urllib.request
import urllib.parse
import json

from  myapp.utils import getJsonResponse, getAllSongsOnRecord, getFullListings


@require_GET
def recentListings(request):
    #Grab all listings (until response is not okay)
    listings = []
    i = 1
    while(True):
        resp = getJsonResponse("listings", i)
        if resp['ok']:
            listings.append(resp['data'])
            i = i + 1
        else:
            break

    # Grab two most recent listings
    listings.sort(key=lambda d: d['date_posted'], reverse=True)
    listings = listings[:2]

    # Get full listing details instead of just ids
    data = {}
    data['ok'] = True
    data['listings'] = getFullListings(listings)

    return JsonResponse(data)
@require_GET
def listingDetails(request, model_id):
    resp = getJsonResponse("listings", model_id)
    if resp['ok']:
        listings = []
        listings.append(resp['data'])
        # Get full listing details instead of just ids
        data = {}
        data['ok'] = True
        data['listings'] = getFullListings(listings)
    else:
        data = {}
        data['ok'] = False
        data['listings'] = []

    return JsonResponse(data)
