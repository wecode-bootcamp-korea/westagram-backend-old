from django.db import models
from user.models import User

class Post(models.Model):
    user         = models.ForeignKey("User", on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts"



class Image(models.Model):
    image_url = models.CharField(max_length=2000)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"