from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re

from . import db
from math import pi, sin, cos, atan2, sqrt

failure = dumps({"Failed"})
def distance(obj):
    R = 6371
    dLat = (obj['l2'] - obj['l1']) * pi / 180
    dLon = (obj['ln2'] - obj['ln1']) * pi / 180
    lat1 = obj['l1'] * pi / 180
    lat2 = obj['l2'] * pi / 180
    a = sin(dLat / 2) * sin(dLat / 2) + sin(dLon / 2) * sin(dLon / 2) * cos(lat1) * cos(lat2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    return d

@csrf_exempt
def search(request):
    data = db.fe_app
    try:
        p = int(request.GET['p'])
    except:
        p = 0
    try:
        type=request.GET['t']
    except:
        type="toilet"
    if 'lat' in request.GET.keys() and 'lng' in request.GET.keys():
        lat = re.sub("[^0-9\.]", "", request.GET['lat'])
        lon = re.sub("[^0-9\.]", "", request.GET['lng'])
    else:
        lat = False

    start = (p) * 10
    end = start + 10
    result = list(data.find({"type":type}, {"_id": False,"uniq_id":True,"pics":True,"title":True,"rating":True,"review":True,"img":True,"loc":True}))
    for resz in result:
        if lat:
            data_for_distance = {
                "l1": float(lat),
                "ln1": float(lon),
                "l2": float(re.sub("[^0-9\.]", "", str(resz['loc']['lat']  if (resz.get('loc')) else 0) )),
                "ln2": float(re.sub("[^0-9\.]", "", str(resz['loc']['lng']  if (resz.get('loc')) else 0)))
            }
            resz.update({"distance": distance(data_for_distance)})
        else:
            resz.update({"distance": False})
    result=sorted(result, key=lambda o: 10000 if False else o['distance'])
    result = [x for x in result if x['distance'] < 500]
    i=len(result)
    #result = result[start:end]
    success = dumps({"data": result, "page": p, "total": i})
    return HttpResponse(success, content_type="application/json")