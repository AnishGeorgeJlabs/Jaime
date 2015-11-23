from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
from . import db

failure = dumps({"Failed"})
@csrf_exempt
def insert_query(request):
    data = db.test
    try:
        result=data.insert(request.body)
        return HttpResponse(request)
    except:
        return HttpResponse(failure, content_type="application/json")
    return HttpResponse(failure, content_type="application/json")


