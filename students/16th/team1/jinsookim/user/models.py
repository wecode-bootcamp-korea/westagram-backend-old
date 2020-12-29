from django.db import models

# Create your models here.
class Users(models.Model):
    
    phone_number = models.CharField(max_length = 50, blank = False)
    user_name    = models.CharField(max_length = 50, blank = False)
    email        = models.EmailField(max_length = 254, blank = False)
    password     = models.CharField(max_length = 50)
    
    class Meta:
        db_table = 'users'



