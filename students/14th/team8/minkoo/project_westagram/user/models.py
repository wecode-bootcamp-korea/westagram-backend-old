from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=15)
    phone    = models.CharField(max_length=12)
    email    = models.EmailField() 
    password = models.TextField()
    like     = models.ManyToManyField('posting.Post', related_name='like_user')
    follow   = models.ManyToManyField('self', through='FollowList', symmetrical=False)

    class Meta:
        db_table = 'users'

class FollowList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follow_from_user')
    follow_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follow_to_user')

    class Meta:
        db_table = 'follow_lists'
