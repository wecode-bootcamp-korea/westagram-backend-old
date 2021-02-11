from django.db import models

class User(models.Model):
    full_name    = models.CharField(max_length=30)
    email        = models.EmailField()
    phone_number = models.CharField(max_length=30)
    username     = models.CharField(max_length=20)
    password     = models.CharField(max_length=300)

    class Meta:
        db_table = 'users'

class Following(models.Model):
    following_id = models.IntegerField(default=0)
    user         = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='following')

    class Meta:
        db_table = 'following'

class Follower(models.Model): 
    follower_id = models.IntegerField(default=0)
    user        = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='follower')

    class Meta:
        db_table = 'followers'
