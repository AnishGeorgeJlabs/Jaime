from bson.json_util import dumps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
from . import db, get_json, basic_success, basic_error

failure = dumps({"Failed"})
@csrf_exempt
def insert_query(request):
    try:
        data = get_json(request)
        collection =db.test
        try:
            result=collection.distinct("sub_id")
            data['sub_id']=max(result)+1
        except:
            data['sub_id']= 1
        collection.insert(data)
        return basic_success(data)
    except Exception as e:
        return basic_error(e)

