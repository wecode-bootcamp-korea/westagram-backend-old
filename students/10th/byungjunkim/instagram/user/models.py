from django.db import models


class User(models.Model):
    name       = models.CharField(max_length = 50)
    email      = models.CharField(max_length = 50)
    password   = models.CharField(max_length = 300)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'


class Follow(models.Model):
    follower = models.ForeignKey(User,related_name='Follow',on_delete=models.CASCADE)
    followee = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table ='follows'