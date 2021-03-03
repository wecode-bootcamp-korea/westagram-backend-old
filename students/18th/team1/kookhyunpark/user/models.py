from django.db import models

# Create your models here.
class SignUp(models.Model):
    email         = models.EmailField(max_length=50)
    phone         = models.CharField(max_length=11)
    full_name     = models.CharField(max_length=40)
    user_name     = models.CharField(max_length=20)
    password      = models.CharField(max_length=20)
    date_of_birth = models.DateField() 
