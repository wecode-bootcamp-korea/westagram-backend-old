from django.db import models

class Account(models.Model):
	name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	phone = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
