from django.db import models


# Create your models here.
class Users(models.Model):
    user_name               = models.CharField(max_length=50)
    phone_number            = models.CharField(max_length=12)
    email                   = models.CharField(max_length=100)
    password                = models.CharField(max_length=50)
    name                    = models.CharField(max_length=50)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "users"
    
