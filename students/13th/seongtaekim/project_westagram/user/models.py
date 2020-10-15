from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=40,null=True)
    name         = models.CharField(max_length=40,null=True)    
    user_name    = models.CharField(max_length=40)
    password     = models.CharField(max_length=100)
    following    = models.ManyToManyField('self',symmetrical=False,through='Follow', related_name='follows')

    class Meta :
        db_table = 'user'

class Follow(models.Model):
    follower = models.ForeignKey('User', on_delete = models.CASCADE, related_name='follower')
    followee = models.ForeignKey('User', on_delete = models.CASCADE, related_name='followee')

    class Meta :
        db_table = 'follow'