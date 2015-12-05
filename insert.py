from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from . import db, get_json, basic_success, basic_error

failure = dumps({"Failed"})
@csrf_exempt
def insert_query(request):
    try:
        data = get_json(request)
        collection =db.test
        gmapinfo = db.gmapinfo
        try:
            result=collection.distinct("uniq_id")
            data['uniq_id']=max(result)+1
        except:
            data['uniq_id']= 1
        data['review']=0
        data['confirm']=0
        data['rating']=3.5
        if "uniq_code" in data:
            gmapinfo.delete_one({"uniq_id": data['uniq_code']})
            del data['uniq_code']
        collection.insert(data)
        return basic_success(data)
    except Exception as e:
        return basic_error(e)

