from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    password     = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name