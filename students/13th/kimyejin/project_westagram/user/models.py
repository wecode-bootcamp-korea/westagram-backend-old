from django.db import models

class SignUp(models.Model):
	name = models.CharField(max_length=30)
	phone_number = models.CharField(max_length=30)
	email = models.EmailField(max_length=250)
	user_name = models.CharField(max_length=30)
	password = models.CharField(max_length=300)
