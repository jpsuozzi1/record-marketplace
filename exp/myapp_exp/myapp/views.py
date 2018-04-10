from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from myapp.utils import getAllListings, getFullListings, getJsonResponse, getAllRecords
import urllib.request
import urllib.parse
import json
from urllib.error import HTTPError

@require_GET
def recentListings(request):
    #Grab all listings (until response is not okay)
    listings = getAllListings()['data']
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

# Create account, pass data to model layer and return response
@require_POST
def createAccount(request):
    data = urllib.parse.urlencode(request.POST).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/users/create/', data=data)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

@require_POST
def createListing(request):
    data = urllib.parse.urlencode(request.POST).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/listings/create/', data=data)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

@require_GET
def recordsList(request):
    records = getAllRecords()['data']
    return JsonResponse(records, safe=False)


# Login, pass on data through to model layer and return response
@require_POST
def login(request):
    data = urllib.parse.urlencode(request.POST).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/login/',data=data)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

# Logout, pass on data through to model layer and return response
@require_POST
def logout(request):
    data = urllib.parse.urlencode(request.POST).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/logout/',data=data)
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        content = e.read()
        return HttpResponse(content)
    resp = json.loads(resp_json)
    return JsonResponse(resp)
