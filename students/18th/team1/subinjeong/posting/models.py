from django.db import models

from user import models


class Posting(models.Model):

    username     = models.ForeignKey('User',on_delete=models.CASCADE)
    time_dreated = models.CharField(max_length=45)
    img_url      = models.CharField(max_length=45)

    class Meta(object):
        db_table = "postings"


        