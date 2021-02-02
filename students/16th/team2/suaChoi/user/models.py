from django.db import models

class User(models.Model):
    email      = models.EmailField(max_length=800, null=True)
    phone      = models.CharField(max_length=800, null=True)
    name       = models.CharField(max_length=100, null=True)
    password   = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
