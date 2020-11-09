from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=50)
    name         = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, null=True)
    password     = models.CharField(max_length=300)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name
