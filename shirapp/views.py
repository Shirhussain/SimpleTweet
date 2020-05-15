from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse

from .models import Tweet



def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)
    

def list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{"id":x.id, "content":x.description} for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def detail_view(request, tweet_id, * args, **kwargs):

    data = {
        'id': tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    return JsonResponse(data)
