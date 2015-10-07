from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
            "requestData": request.body
        }
    return JsonResponse({
        "result": True,
        "Message": "Welcome to the Jaime API",
        "extra": extra
    })

urlpatterns = [
    url(r'^$', test)
]

