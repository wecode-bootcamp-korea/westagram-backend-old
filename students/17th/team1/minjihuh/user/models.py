from django.db import models

class User(models.Model):
    name              = models.CharField(max_length=50)
    phone             = models.CharField(max_length=20, null=True, unique=True)
    email             = models.EmailField(max_length=100, null=True, unique=True)
    password          = models.CharField(max_length=300)
    username          = models.CharField(max_length=100, unique=True) 
    created_at        = models.DateTimeField(auto_now_add=True)
    modified_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


class Follow(models.Model): # 팔로우 수 관리
    follower  = models.ForeignKey('User', related_name = "follower", on_delete=models.CASCADE)
    following = models.ForeignKey('User', related_name = "following", on_delete=models.CASCADE) 

    class Meta:
        db_table = 'follows'