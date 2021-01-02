from django.db import models
from user.models import Users
# Create your models here.
# 게시물 등록
class Post_register(models.Model):
    user         = models.ForeignKey('user.Users', on_delete = models.CASCADE)
    content      = models.CharField(max_length=100)
    title        = models.CharField(max_length=100)
    image_url    = models.CharField(max_length=100)
    create_time  = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'post_register'

# 게시물 표출
class Post_express(models.Model):
    post_register   = models.ForeignKey('Post_register', on_delete = models.CASCADE)
    content         = models.CharField(max_length=100)
    image_url       = models.CharField(max_length=100)
    upload_time     = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'post_express'


# 댓글 기능
class Comments(models.Model):
    post_register   = models.ForeignKey('Post_register', on_delete = models.CASCADE)
    user            = models.ForeignKey('user.Users', on_delete = models.CASCADE)
    comment         = models.CharField(max_length=100)
    create_time     = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'comments'


# "좋아요" 기능
class Love(models.Model):
    user          = models.ForeignKey('user.Users', on_delete = models.CASCADE)
    post_register = models.ForeignKey('Post_register', on_delete = models.CASCADE)

    class Meta:
        db_table = 'love'