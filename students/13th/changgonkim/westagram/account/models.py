from django.db import models
# Create your models here.

class Account(models.Model) :
	email		= models.EmailField(verbose_name="email", max_length=60)
	username	= models.CharField(max_length=30)
	phonenumber	= models.CharField(max_length=12)
	password	= models.CharField(max_length=1000)

	class Meta:
		db_table = 'accounts'
