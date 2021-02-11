from django.db import models

class User(models.Model):
    name        =   models.CharField(max_length=50)
    email       =   models.CharField(max_length=50)
    password    =   models.CharField(max_length=300)
    created_at  =   models.DateTimeField(auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

class Following(models.Model):
    followed_user   =   models.ForeignKey(User,related_name='Followed_User',on_delete=models.CASCADE)
    following_user  =   models.ForeignKey(User,related_name='Following_User',on_delete=models.CASCADE)

    class Meta:
        db_table = 'following' 

