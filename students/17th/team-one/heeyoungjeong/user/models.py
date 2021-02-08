from django.db import models


class User(models.Model):
    name         = models.CharField(max_length=20)
    user_name    = models.CharField(max_length=20)
    email        = models.EmailField(max_length=30)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'User'




