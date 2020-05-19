from django.conf import settings
from django import forms
from .models import Tweet


MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['description']

    # this is gnna valided my description, so i have to make sure that the length is under 240
    # because it's tweeter style of posting
    def clean_description(self):
        content = self.cleaned_data.get("description")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("The tweet is too long")
        return content
        