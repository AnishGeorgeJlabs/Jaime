from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from . import db, get_json, basic_success, basic_error

failure = dumps({"Failed"})
@csrf_exempt
def add_review(request):
    try:
        data = get_json(request)
        collection =db.test
        reviews = db.reviews
        try:
            result=reviews.distinct("uniq_id")
            data['uniq_id']=max(result)+1
        except:
            data['uniq_id']= 1
        reviews.insert(data)
        #collection.update({'uniq_id':data['f_uniq_id']},{ "review": 1 },{"upsert":True})
        return basic_success()
    except Exception as e:
        return basic_error(e)

