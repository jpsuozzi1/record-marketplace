from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from myapp.utils import getAllListings, getFullListings, getJsonResponse
import urllib.request
import urllib.parse
import json

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

# Login, pass on data through to model layer
@require_POST
def login(request):
    data = urllib.parse.urlencode(request.POST).encode('utf-8')
    req = urllib.request.Request('http://models-api:8000/api/v1/login/',data=data)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)
