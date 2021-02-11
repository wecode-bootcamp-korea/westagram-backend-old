from django.db import models


class Users(models.Model):
    name       = models.CharField(max_length = 50)
    email      = models.CharField(max_length = 50)
    password   = models.CharField(max_length = 300)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    github_id  = models.CharField(max_length=10, null = True)

class Meta: 
    db_table = "users"

def __str__(self):
    return self.name
