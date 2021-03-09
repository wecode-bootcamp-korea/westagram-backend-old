from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=50)
    password = models.CharField(max_length=500)

    class Meta:
        db_table = "users"
