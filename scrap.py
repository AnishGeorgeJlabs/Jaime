from bson.json_util import dumps
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib.parse
import urllib.request
import json
from . import db, basic_error

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
def scrap(request):

    #url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=28.563578,77.238551&radius=5000&name=toilet&key=AIzaSyDtcQVt2YgYKL0RAamqswNBuC7Dz3LQ9CU'
    url = 'https://dmaps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=CqQDmwEAAKLgNV4pUxy1loQNUsfd0chuDUbF64TuyJHq14iL0Br28q-m_y3ibvTOUiTHE8uRVbpyrPyPLZULMBaR-UMSH7_OeKxdo1WCzcDEt7kB0SEvIDtmIWmHLdMJLumDPcl62jkLOjx0WGAQGTRQIVtqoGGfOmd7tiZaf6N8WYfSWumMmDPjO4BoC2erEHf-KGpQkUU4hSm07Jo-QbmyoTZ5vHEHg63t0PrN9KEgleKfoOWxzGxG0w3nq3gm41UEVp5oYHoOabHZKurU9UT4Kczvlk0N1zfvoVM9e33vwHWQ5LFegiZk85Qps6rVW_s4KaSm71rfTBezg1fr7aD9pynb6iijVTmvU70owyQ4dhANFcXAxXzN97fsMDuuf6FPUYwvnMp-ZJRkyaNtH-vmVpct8Hn11jsQT5xCMNyDs0k-TPuZMzejsUHa6Kxx4ReTtl4M5HxcjEt-YKBPeL3ueDxhpABD3msub_k35oRFvRdyFxaFYxanNjE2wYkJH2SyPJX33Pun4uTYQI2MXVO6V0f-DrUW00XYQLIZzoTTc3UodbqFEhDxwj_yiVHLg_ReBUadZRPsGhT37R664NV3AdxU-AxuaJZQRwILpQ&key=AIzaSyDtcQVt2YgYKL0RAamqswNBuC7Dz3LQ9CU'
    #url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?location=28.658237,77.207837&radius=5000&query=toilet&key=AIzaSyDtcQVt2YgYKL0RAamqswNBuC7Dz3LQ9CU'
    values = {}
    List_Map = []
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        the_page = response.read().decode("utf-8")
    the_page=json.loads(the_page)
    #data['next_page_token']=the_page['next_page_token']
    #next_page_token = the_page['next_page_token']
    max_result=1
    try:
        collection =db.gmapinfo
        try:
            result=collection.distinct("uniq_id")
            max_result=max(result)+1
        except:
            max_result= 1
    except Exception as e:
        return basic_error(e)
    for resz in the_page['results']:
        new_dict = dict()
        new_dict['title']=resz['vicinity']
        new_dict['lat']=resz['geometry']['location']['lat']
        new_dict['lng']=resz['geometry']['location']['lng']
        new_dict['uniq_id']=max_result
        max_result=max_result+1
        collection.insert(new_dict)
        List_Map.append(new_dict)
        #new_dict.clear()


    new_data=json.dumps(List_Map)
    return HttpResponse(new_data, content_type="application/json")