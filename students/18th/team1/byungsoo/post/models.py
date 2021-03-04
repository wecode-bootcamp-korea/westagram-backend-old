from django.db import models
from user.models import User

class Post(models.Model):
    user         = models.ForeignKey("User", max_length=45)
    created_at   = models.DateTimeField(auto_now_add=True)
    image_url    = models.CharField(max_length=2000)

    class Meta:
        db_table = "posts"
