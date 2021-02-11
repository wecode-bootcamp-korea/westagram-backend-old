from django.db import models
from account.models import Account

class Posting(models.Model):
    user            =   models.ForeignKey(Account, on_delete = models.CASCADE)
    img_url         =   models.URLField(max_length = 1000)
    content         =   models.TextField(max_length = 200)
    created_time    =   models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    user            =   models.ForeignKey(Account, on_delete = models.CASCADE)
    post            =   models.ForeignKey(Posting, on_delete = models.CASCADE) # 댓글 달린 post
    content         =   models.CharField(max_length = 200)
    created_time    =   models.DateTimeField(auto_now_add = True) 
