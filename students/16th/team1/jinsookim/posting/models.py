from django.db import models
from user.models import Users
# Create your models here.
# 게시물 등록
class Post_register(models.Model):
    user         = models.ForeignKey('user.Users', on_delete = models.CASCADE)
    image_url    = models.CharField(max_length=100)
    create_time  =  models.DateField(auto_now=True)
    upadte_time  =  models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'post_register'

# 게시물 표출
class Post_express(models.Model):
    user         = models.CharField(max_length=50)
    image_url    = models.CharField(max_length=100)
    post_time    = models.DateField(auto_now=True)

    class Meta:
        db_table = 'post_express'