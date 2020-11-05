from django.db import models

# Create your models here.
class Users(models.Model):
    name            = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=20)
    email           = models.CharField(max_length=50)
    password        = models.CharField(max_length=300)
    #created_at      = models.CharField(auto_now_add=True)
    #updated_at      = models.CharField(auto_now=True)
    
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name
