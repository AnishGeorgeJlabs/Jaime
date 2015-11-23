from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
from . import db

failure = dumps({"Failed"})
@csrf_exempt
def search_query(request):
    data=db.test
    dumps(request)
    if len(request.body) > 0
        return HttpResponse(request, content_type="application/json")
    else
        return HttpResponse(request, content_type="application/json")
