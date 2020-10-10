from django.db import models

# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=45)
    user_email = models.EmailField(max_length=254)
    user_password = models.CharField(max_length=25)

    class Meta:
        db_table = 'users'
