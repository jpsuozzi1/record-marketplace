from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import urllib.request
import urllib.parse
import json


def home(request):

    return render(request, 'home.html',{})

def listing(request, listing_id):
    # make a GET request and parse the returned JSON
    # note, no timeouts, error handling or all the other things needed to do this for real
    #print ("About to perform the GET request...")

    req = urllib.request.Request('http://exp-api:8000/dummy/0/')

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)


    return render(request, 'listing.html', {'success':resp, 'listing_id':listing_id,'price':resp})
