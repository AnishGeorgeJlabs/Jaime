__author__ = 'Pradeep'
from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
from . import db

failure = dumps({"success":0})

@csrf_exempt
def all_reviews(request):
    reviews=db.reviews
    try:
        q = int(request.GET['id'])
    except:
        return HttpResponse(failure, content_type="application/json")
    try:
        p = int(request.GET['p'])
    except:
        p=0

    review = reviews.find({"f_uniq_id":q}, {"_id":False,"f_uniq_id": False})[p*10:p*10+10]
    success = dumps({"success": 1, "data": review})
    return HttpResponse(success, content_type="application/json")