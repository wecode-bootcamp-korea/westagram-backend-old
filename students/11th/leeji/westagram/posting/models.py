from django.db import models

from user.models import User

class Post(models.Model):
    email   = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField(max_length = 500)
    img_url = models.URLField()
    created_time = models.DateTimeField(auto_now_add = True) 

    class Meta:
        db_table = "post"

class Comment(models.Model):
    email   = models.ForeignKey(User, on_delete = models.CASCADE)
    post    = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment = models.TextField(max_length = 500)
    created_time = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "comment"
