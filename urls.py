from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import search,search_location,insert,gmap,scrap,description,all_reviews,add_review
import json

@csrf_exempt
def test(request):
    if request.method == "GET":
        extra = {
            "method": "GET",
            "requestData": request.GET
        }
    else:
        extra = {
            "method": "POST",
            "requestData": json.loads(request.body.decode())
        }
    return JsonResponse({
        "result": True,
        "Message": "Welcome to the Jaime API",
        "extra": extra
    })

urlpatterns = [
    url(r'^$', test),
    url(r'^search',  search.search),
    url(r'^scrap',  scrap.scrap),
    url(r'^description',  description.description),
    url(r'^reviews',  all_reviews.all_reviews),
    url(r'^add_review',  add_review.add_review),
    url(r'^gmap',  gmap.gmap),
    url(r'^location',  search_location.search_query),
    url(r'^insert',  insert.insert_query)

]



