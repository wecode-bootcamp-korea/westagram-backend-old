from django.db import models

class User(models.Model):
    email         = models.CharField(max_length=100, unique=True, null=True)
    mobile_number = models.CharField(max_length=100, unique=True, null=True)
    full_name     = models.CharField(max_length=100)
    username      = models.CharField(max_length=100, unique=True)
    password      = models.CharField(max_length=300)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Follow(models.Model):
    follower  = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')

    class Meta:
        db_table = 'follow'