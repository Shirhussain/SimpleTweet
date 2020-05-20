from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS
class ActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip() # if it was Upercase so we have to make sure that is lower we can do like that
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid option we only accept Like , unlike and retweet")
        return value


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['description']

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("The tweet is too long")
        return value
        
