__author__ = 'Pradeep'
from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
from . import db

failure = dumps({"success":0})

@csrf_exempt
def search_query(request):
    data = db.fe_app
    try:
        q = request.GET['q']
        type=request.GET['t']
    except:
        return HttpResponse(failure, content_type="application/json")
    query = {"title": re.compile(q, re.IGNORECASE),"type":type}
    result = data.find(query, {"_id":False,"title": True,"loc":True,})
    success = dumps({"success": 1, "data": result, "total": result.count()})
    return HttpResponse(success, content_type="application/json")