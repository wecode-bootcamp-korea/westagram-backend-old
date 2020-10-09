from django.db import models

from user.models import User
class Posting(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField(null=True)
    image=models.URLField()
    created_date=models.DateTimeField()
    modified_date=models.DateTimeField(null=True)