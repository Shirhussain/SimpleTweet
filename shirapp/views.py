import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404, HttpResponse
from django.utils.http import is_safe_url 


from .models import Tweet
from .forms import TweetForm



ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS): 
            return redirect(next_url)
        form = TweetForm()
    context = {
        'form':form
    }
    return render(request, "components/form.html", context)
    

def list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{"id":x.id, "content":x.description,"likes": random.randint(0,200)} for x in qs]
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
