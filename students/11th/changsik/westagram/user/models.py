from django.db import models

class User(models.model):
    name       = models.CharField(max_length = 30)
    email      = models.CharField(max_length = 30)
    password   = models.CharField(max_length = 30)
    created_at = models.DataTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)