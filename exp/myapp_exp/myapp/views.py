from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import urllib.request
import urllib.parse
import json


@require_GET
def recentListings(request):

    #Grab all listings (until response is not okay)
    listings = []
    i = 1
    while(True):
        req = urllib.request.Request('http://models-api:8000/api/v1/listings/' + str(i) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
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
        req = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(listing['seller_id']) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        if resp['ok']:
            sellerName = resp['data']['first_name'] + " " + resp['data']['last_name']
        else:
            sellerName = "No Seller Found"

        # Get buyer name
        req = urllib.request.Request('http://models-api:8000/api/v1/users/' + str(listing['buyer_id']) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        if resp['ok']:
            buyerName = resp['data']['first_name'] + " " + resp['data']['last_name']
        else:
            buyerName = "No Buyer"

        # Get Record Name
        req = urllib.request.Request('http://models-api:8000/api/v1/records/' + str(listing['record_id']) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
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
