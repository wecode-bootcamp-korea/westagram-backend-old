from django.db import models
from user.models import User


class Posting(models.Model):
    image_url  = models.CharField(max_length=1000)
    content    = models.TextField(null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user       = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "postings"

