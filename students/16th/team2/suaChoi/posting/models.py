from django.db import models

from user.models import User

class Post(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    img          = models.URLField(max_length=2000)
    content      = models.TextField(null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "postings"

