from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import urllib.request
import urllib.parse
import json

from  myapp.utils import getJsonResponse


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
    fullListings = []
    for listing in listings:
        # Get seller name
        resp = getJsonResponse("users", listing['seller_id'])
        if resp['ok']:
            sellerName = resp['data']['first_name'] + " " + resp['data']['last_name']
        else:
            sellerName = "No Seller Found"

        # Get buyer name
        resp = getJsonResponse("users", listing['buyer_id'])
        if resp['ok']:
            buyerName = resp['data']['first_name'] + " " + resp['data']['last_name']
        else:
            buyerName = "No Buyer"

        # Get Record Name
        resp = getJsonResponse("records", listing['record_id'])
        if resp['ok']:
            recordName = resp['data']['name']
        else:
            recordName = "No Record Name"

        fullListing = {
            "date_posted": listing['date_posted'],
            "record": recordName,
            "price": listing['price'],
            "seller": sellerName,
            "buyer": buyerName
        }

        fullListings.append(fullListing)

    data['listings'] = fullListings
    return JsonResponse(data)
