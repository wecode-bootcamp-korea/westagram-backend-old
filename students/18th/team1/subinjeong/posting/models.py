from django.db import models

from user.models import User

class Posting(models.Model):

    username     = models.ForeignKey('user.User',on_delete=models.CASCADE)
    title        = models.CharField(max_length=50)
    img_url      = models.CharField(max_length=1000)
    time_created = models.DateTimeField(auto_now_add=True)    

    class Meta(object):
        db_table = "postings"