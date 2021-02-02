from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    name     = models.CharField(max_length=30, null=True)
    phone    = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name