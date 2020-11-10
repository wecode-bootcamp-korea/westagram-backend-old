from django.db import models

class User(models.Model):
    name      = models.CharField(max_length=10)
    telephone = models.CharField(max_length=12)
    password  = models.CharField(max_length=20)
    email     = models.EmailField(max_length=20)


    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name
