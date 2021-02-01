from django.db import models

class User(models.Model):
    full_name    = models.CharField(max_length=30)
    email        = models.EmailField()
    phone_number = models.IntegerField(null=True)
    username     = models.CharField(max_length=20)
    password     = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'
