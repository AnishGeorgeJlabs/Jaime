__author__ = 'Pradeep'
from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
from . import db

failure = dumps({"success":0})

@csrf_exempt
def description(request):
    data = db.test
    reviews=db.reviews
    try:
        q = int(request.GET['id'])
    except:
        return HttpResponse(failure, content_type="application/json")
    review = reviews.find({"f_uniq_id":q}, {"_id":False,"f_uniq_id": False})[0:2]
    result = data.find_one({"uniq_id": q}, {"_id":False,"desc": True,"icons":True})
    success = dumps({"success": 1, "data": result,"review":review})
    return HttpResponse(success, content_type="application/json")