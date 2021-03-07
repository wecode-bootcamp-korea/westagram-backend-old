from django.db import models

from account.models import User


class Follow(models.Model):
    follower = models.ManyToManyField(User, related_name="following") 
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "follows"