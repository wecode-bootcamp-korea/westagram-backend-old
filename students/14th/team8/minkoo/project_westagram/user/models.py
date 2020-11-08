from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=15)
    phone    = models.CharField(max_length=12)
    email    = models.EmailField() 
    password = models.CharField(max_length=20)
    follow = models.ManyToManyField('self', through='FollowList', symmetrical=False)

    class Meta:
        db_table = 'users'

class FollowList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    follow_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follow')

    class Meta:
        db_table = 'follow_lists'
