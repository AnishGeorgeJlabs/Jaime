from bson.json_util import dumps
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib
import urllib.parse
import urllib.request
import json
from . import db, basic_error

from math import pi, sin, cos, atan2, sqrt

@csrf_exempt
def datascrap(request):
    #max_result= 1090
    try:
        collection =db.dhalao
        try:
            result=collection.distinct("uniq_id")
            max_result=max(result)+1
        except:
            max_result= 1
    except Exception as e:
        return basic_error(e)

    with open("data.json") as json_file:
        the_page=json.load(json_file)
    for resz in the_page:
        resz['uniq_id']=max_result
        max_result=max_result+1
        collection.insert(resz)
    new_data=json.dumps(the_page)

    return HttpResponse(new_data, content_type="application/json")