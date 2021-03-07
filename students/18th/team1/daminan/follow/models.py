from django.db import models

from account.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE, default='')
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE, default='')    
    class Meta:
        db_table = "follows"