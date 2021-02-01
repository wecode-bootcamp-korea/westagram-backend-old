from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=500, null=False)

    class Meta:
        db_table = 'users'