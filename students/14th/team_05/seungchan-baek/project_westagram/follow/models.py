from django.db import models

class Follow(models.Model):
    be_followed  = models.ForeignKey('user.User', on_delete = models.CASCADE, related_name = 'followed_user',null=True)
    follower     = models.ForeignKey('user.User', on_delete = models.CASCADE, related_name = 'follow_user', null=True)

    class Meta:
        db_table='follows'
