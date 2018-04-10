from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
import urllib.request
import urllib.parse
import json
from .forms import *
from urllib.error import HTTPError
from django.contrib import messages

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
            try:
                resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            except HTTPError as e:
                content = e.read()
                return HttpResponse(content)
            resp = json.loads(resp_json)
            if not resp['ok']:
                if resp['data']['email']:
                    messages.info(request, "This email is already in use. Please try again.")
                    return HttpResponseRedirect(reverse('createAccount'), {'messages': messages})

            return redirect('login')
    else:
        form = CreateUser()

    return render(request, 'createAccount.html', {'form': form})

def createListing(request):

    auth = request.COOKIES.get('auth')

    if not auth:
        messages.info(request, "You must be logged in to create a listing")
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createListing"), {'messages': messages})

    if (request.method == 'GET'):
        form = CreateListing()
        return render(request, 'createListing.html', {'form': form})

    elif (request.method == 'POST'):
        form = CreateListing(request.POST)
        if (form.is_valid()):
            params = {'price': request.POST['price'], 'recordName': request.POST['record'], 'condition': request.POST['condition'], 'cookie': auth}
            data = urllib.parse.urlencode(params).encode('utf-8')
            url = 'http://exp-api:8000/api/v1/createListing/'
            req = urllib.request.Request(url, data=data, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            if not resp['ok']:
                return HttpResponse("Listing could not be created")

            return redirect('home')

    return render(request, 'createListing.html', {'form': form})

def recordsList(request):

    url = 'http://exp-api:8000/api/v1/recordsList/'
    req = urllib.request.Request(url)

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    records = json.loads(resp_json)

    names = []
    for r in records:
        names.append(r['name'])
    result = names
    
    return JsonResponse(result, safe=False)
    
    #return render(request, 'listing.html', {})

def login(request):
    # Display form to log a user in
    if (request.COOKIES.get('auth')):
        messages.info(request, 'You are already logged in.')
        return HttpResponseRedirect(reverse('home'), {'message': messages})
    

    if (request.method == 'GET'):
        form = LoginUser()
        next = request.GET.get('next') or reverse('home')
        return render(request, 'login.html', {'form': form})

    elif (request.method == 'POST'):
        form = LoginUser(request.POST)
        if (form.is_valid()):
            next = reverse('home')

            data = urllib.parse.urlencode(request.POST).encode('utf-8')
            url = 'http://exp-api:8000/api/v1/login/'

            req = urllib.request.Request(url, data=data, method='POST')
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            
            resp = json.loads(resp_json)
            if not resp['ok']:
                messages.info(request, "Incorrect email or password. Please try again.")
                return HttpResponseRedirect(reverse('login'), {'messages': messages})

            # Store authenticator in cookie
            auth = resp['data']['auth']
            response = HttpResponseRedirect(next)
            response.set_cookie("auth", auth)

            return response

    return render(request, 'login.html', {'form': form})

def logout(request):
    # Handle logout request and display results
    
    # Get the authenticator's model id from the cookie
    auth = request.COOKIES.get('auth')
    
    next = reverse('home')

    if not auth:
        messages.info(request, "You are not logged in.")
        response = HttpResponseRedirect(next, {'messages': messages} )
        return response

    # Put model id into data
    data = urllib.parse.urlencode({'auth': auth}).encode('utf-8')
    url = 'http://exp-api:8000/api/v1/logout/'

    req = urllib.request.Request(url, data=data, method='POST')
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        content = e.read()
        return HttpResponse(content)
    resp = json.loads(resp_json)

    if not resp['ok']:
        messages.info(request, "You are not logged in.")
        response = HttpResponseRedirect(next, {'messages': messages} )
    else:
        messages.info(request, "Successfully logged out!")
        response = HttpResponseRedirect(next, {'messages': messages} )
        response.delete_cookie('auth')

    return response
