from django.db import models
import random

class Tweet(models.Model):
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="images/", blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.description,
            "likes": random.randint(0,200)  
        }