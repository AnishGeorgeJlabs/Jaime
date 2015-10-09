from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import db

failure = dumps({"Failed"})


@csrf_exempt
def search(request):
    data = db.test
    try:
        p = int(request.GET['p'])
    except:
        p = 0
    start = (p) * 10
    end = start + 10
    result = data.find({}, {"_id": False})
    result = result[start:end]
    success = dumps({"data": result, "page": p, "total": data.count()})
    return HttpResponse(success, content_type="application/json")