from django.db import models

from User.models import User

class Posting(models.Model):
    user         = models.ForeignKey(User, on_delete = models.CASCADE)
    image        = models.URLField(max_length = 250)
    text         = models.CharField(max_length = 200)
    created_time = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    post = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length = 200)
    created_time = models.DateTimeField(auto_now_add = True)
