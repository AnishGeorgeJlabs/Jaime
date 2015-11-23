from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
from . import db

failure = dumps({"Failed"})
@csrf_exempt
def insert_query(request):
    data = db.test
    try:
        result=data.insert(request)
        return HttpResponse("{'success':1}", content_type="application/json")
    except:
        return HttpResponse(failure, content_type="application/json")
    return HttpResponse(failure, content_type="application/json")


