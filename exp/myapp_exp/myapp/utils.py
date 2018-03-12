import urllib.request
import urllib.parse
import json

def getJsonResponse(model, id):
        req = urllib.request.Request('http://models-api:8000/api/v1/' + model + '/' + str(id) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        return resp
