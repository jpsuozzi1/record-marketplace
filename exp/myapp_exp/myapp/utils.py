import urllib.request
import urllib.parse
import json

def getJsonResponse(model, id):
    req = urllib.request.Request('http://models-api:8000/api/v1/' + model + '/' + str(id) + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def getAllSongsOnRecord(id):
    req = urllib.request.Request('http://models-api:8000/api/v1/records/' + str(id) + '/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def getAllListings():
    req = urllib.request.Request('http://models-api:8000/api/v1/allListings/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def getAllRecords():
    req = urllib.request.Request('http://models-api:8000/api/v1/allRecords/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def getFullListings(listings):
    fullListings = []
    for listing in listings:
        # Get seller name
        resp = getJsonResponse("users", listing['seller'])
        if resp['ok']:
            sellerName = resp['data']['first_name'] + " " + resp['data']['last_name']
        else:
            sellerName = "No Seller Found"

        # Get buyer name
        resp = getJsonResponse("users", listing['buyer'])
        if resp['ok']:
            buyerName = resp['data']['first_name'] + " " + resp['data']['last_name']
        else:
            buyerName = "No Buyer"

        # Get Record Name
        resp = getJsonResponse("records", listing['record'])
        if resp['ok']:
            recordName = resp['data']['name']
        else:
            recordName = "No Record Name"

        songs = getAllSongsOnRecord(listing['record'])['data']
        fullSongs = getFullSongs(songs)

        fullListing = {
            "listing_id": listing['id'],
            "date_posted": listing['date_posted'],
            "record": recordName,
            "songs": fullSongs,
            "price": listing['price'],
            "seller": sellerName,
            "buyer": buyerName,
        }

        fullListings.append(fullListing)
    return fullListings

def getFullSongs(songs):
    fullSongs = []
    for song in songs:
        # Get artist name
        resp = getJsonResponse("artists", song['artist'])
        if resp['ok']:
            artistName = resp['data']['name']
        else:
            artistName = "No Artist Found"

        fullSong = {
            "duration": song['duration'],
            "artist": artistName,
            "name": song['name'],
        }

        fullSongs.append(fullSong)
    return fullSongs
