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
		new_dict['uniq_id'] = data['uniq_id']
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
		
		
@csrf_exempt
def fe_add(request):
	try:
		data={}
		data['fe_id']=request.GET['id']
		data['lat'] = request.GET['lat']
		data['lon'] = request.GET['lon']
		data['time'] = request.GET['time']
		now = datetime.now() + timedelta(hours=5,minutes=30)
		data['date']=now.strftime("%Y-%m-%d %H:%M")
		max = db.fe_daily.find_one({'$query':{} , '$orderby':{'_id':-1}} , {'_id':0 , 'sn':1})
		try:
			data['sn']= int(max.get('sn')) +1
		except:
			data['sn']=1 
		result =db.fe_daily.insert_one(data)
		if result.inserted_id:
			return basic_success()
		else:
			return basic_error()
	except Exception as e: 
		return basic_error(str(e))

@csrf_exempt
def fe_show(request):
	try:
		date = request.GET.get('date');
		id = request.GET['id'];
		
		if date:
			regex = re.compile(date)
			data =db.fe_daily.find({"fe_id":id , "date":{'$regex':regex}} , {"_id":False }).sort('sn',-1)
		else:
			data =db.fe_daily.find({"fe_id":id} , {"_id":False }).sort('sn',-1)
		
		if data:	
			return basic_success(data)
		else:
			return basic_error();
	except Exception as e:
		return basic_error(str(e))