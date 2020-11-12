from django.db import models

class User(models.Model):
    email        = models.EmailField()
    name         = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, null=True)
    password     = models.CharField(max_length=300)

    class Meta:
        db_table = 'users'
