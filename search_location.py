__author__ = 'Pradeep'
from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
from . import db

failure = dumps({"success":0})

@csrf_exempt
def search_query(request):
    data = db.test
    try:
        q = request.GET['q']
    except:
        return HttpResponse(failure, content_type="application/json")
    query = {"title": re.compile(q, re.IGNORECASE)}
    result = data.distinct("title", query)
    success = dumps({"success": 1, "data": result, "total": len(result)})
    return HttpResponse(success, content_type="application/json")