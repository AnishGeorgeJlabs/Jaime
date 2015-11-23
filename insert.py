from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
from . import db

failure = dumps({"Failed"})
@csrf_exempt
def insert_query(request):
    data=db.test
    dumps(request)
    return HttpResponse(request, content_type="application/json")
