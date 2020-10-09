from django.db import models

from user.models import User
class Posting(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)