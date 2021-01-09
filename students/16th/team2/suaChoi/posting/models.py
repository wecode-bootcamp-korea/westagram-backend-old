from django.db import models

from user.models import User

class Post(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url    = models.URLField(max_length=2000)
    content      = models.TextField(null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts"

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    post       = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment    = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False) # is deleted 가 true 였다가 false 였다가

    class Meta:
        db_table = "likes"
