author="Pradeep"

import pymongo
from django.http import HttpResponse
from bson.json_util import dumps
from math import *

# ------- Database Authentication and access ---------------- #
import json
import os

file = os.path.join(
    os.path.dirname(__file__),
    'db_creds.json'
)
with open(file, 'r') as cfile:
    creds = json.load(cfile)['jaime']

dbclient = pymongo.MongoClient("45.55.232.5:27017")
dbclient.jaime.authenticate(creds['u'], creds['p'], mechanism='MONGODB-CR')

# hello
db = dbclient.jaime

# ------- Json response format ------------------------------ #
def get_json(request):
    return json.loads(request.body.decode())

def jsonResponse(d):
    return HttpResponse(dumps(d), content_type='application/json')

def basic_failure(reason=None):
    return base_response(success=False, ekey="reason", reason=reason)

def basic_error(reason=None):
    return base_response(success=False, ekey="error", reason=str(reason))

def haversine(lon1, lat1, lon2, lat2):
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	r = 6371 
	return c * r

def basic_success(data=None):
    return base_response(success=1, data=data)

def base_response(success=False, data=None, ekey="reason", reason=None):
    res = {"success": success}

    if data is not None:
        res['data'] = data

    if reason is not None:
        res[ekey] = reason
    return jsonResponse(res)

# -------------------------------------------------------------- #
