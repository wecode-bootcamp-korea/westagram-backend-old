from django.db import models

# Create your models here.
class Users(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
 
    class Meta:
        db_table = 'Users'




