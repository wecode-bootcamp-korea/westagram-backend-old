from django.db import models
from user.models import Users

class Posts(models.Model):

    title = models.CharField(max_length = 100)
    author = models.ForeignKey(Users, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    image_url = models.URLField(max_length = 2000)

    class Meta:
        db_table = "Posts"

class Comments(models.Model):

    author = models.ForeignKey(Users, on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)

    class Meta:

        db_table = "Comments"


