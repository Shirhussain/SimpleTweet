import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404, HttpResponse
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated

from . serializers import TweetSerializer, ActionSerializer
from .models import Tweet
from .forms import TweetForm



ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST']) # method that client have to send === "POST"
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status = 201) #201 Created. 
    return Response({}, status=400)  #The 400 Bad Request error 
    
@api_view(['GET'])
def list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detail_view(request, tweet_id, * args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)
    

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"Message": "you can not deete thsi tweet unutorised"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"Message": "Tweet Removed"}, status=200)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def action_view(request,*args, **kwargs):
    '''
    id is required 
    Action option are : like , Unlike , Retweet
    '''
    serializer = ActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action   = data.get("action")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status = 200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            # to do 
            pass
    return Response({}, status=200)




def create_view_pure_django(request, *args, **kwargs):
    user = request.user 
    if not request.user.is_authenticated:
        user = None # if they are not authenticated so the user is none
        if request.is_ajax():
            return JsonResponse({}, staus=401)  #Unauthorized client 
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user 
        obj.save()
        # when our Ajax is working i don't need the redirect (next_url) i can do many thing righ now 
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status =201) #201 it means that created
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS): 
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status = 400)
    context = {
        'form':form
    }
    return render(request, "components/form.html", context)
    

def list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def detail_view_pure_django(request, tweet_id, * args, **kwargs):

    data = {
        'id': tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    return JsonResponse(data)
