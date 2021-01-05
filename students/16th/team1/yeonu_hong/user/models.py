from django.db import models

# Create your models here.

class User(models.Model):
    name      = models.CharField(max_length=30)
    password  = models.CharField(max_length=2000)
    phone     = models.CharField(max_length=40)
    email     = models.EmailField(max_length=130)
    follow    = models.ManyToManyField('self', through='Follow', related_name='followers')

    class Meta:
        db_table = 'users'

class Follow(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = 'follows'