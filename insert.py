from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from . import db, get_json, basic_success, basic_error
from datetime import datetime, timedelta
import re

failure = dumps({"Failed"})
@csrf_exempt
def insert_query(request):
    try:
        data = get_json(request)
        collection =db.fe_app
        gmapinfo = db.gmapinfo
        fe_track=db.fe_track
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

        new_dict = dict()
        try:
            res=fe_track.distinct("uniq_id")
            new_dict['uniq_id']=max(res)+1
        except:
            new_dict['uniq_id'] = 1
        new_dict['loc']=data['loc']
        now = datetime.now() + timedelta(hours=5,minutes=30)
        new_dict['date_time'] = now.strftime("%Y-%m-%d %H:%M")
        fe_track.insert(new_dict)

        return basic_success(data)
    except Exception as e:
        return basic_error(e)

def fe_track(request):
	try:
		date = request.GET['date']
		if date:	
			regex = re.compile(date)
			data =db.fe_track.find({"date_time":{'$regex':regex}} , {"_id":False , "uniq_id":True})
			ids=list()
			for d in data:
				ids.append(d['uniq_id'])
			data=db.fe_app.find({"uniq_id":{'$in':ids}})
			return basic_success(data)
		else:
			return basic_success(db.fe_app.find({} , {"_id":False}))
	except:
		return basic_error()