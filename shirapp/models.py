from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL

# one important thing i wnna mesure that i have to collect the time of like, in business it's very impot 
# to know when usre is like something so i wnna have a historical recored ---> to do this i wnna to the following class
class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    user = models.ForeignKey(User,null=True, on_delete = models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="images/", blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    # i don't need to add in above line (through) model --> all i does is that add a timestamp to many to many field
    timestamp = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.description,
            "likes": random.randint(0,200)  
        }