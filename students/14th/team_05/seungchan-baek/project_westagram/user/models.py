from django.db import models

class User(models.Model):
    name      = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20)
    password  = models.CharField(max_length=100)
    email     = models.EmailField(max_length=30)


    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name
