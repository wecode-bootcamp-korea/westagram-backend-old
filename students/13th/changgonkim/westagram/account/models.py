from django.db import models
# Create your models here.

class Account(models.Model) :
	email		= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username	= models.CharField(max_length=30, unique=True)
	phonenumber	= models.IntergerField(max_length=12, unique=True)
	password	= models.CharField(max_length=30)