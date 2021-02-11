from django.db import models

# Create your models here.

class Users(models.Model):
	name       = models.CharField(max_length = 200)
	email      = models.CharField(max_length = 50)
	password   = models.CharField(max_length = 200)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Comments(models.Model):
   name       = models.CharField(max_length = 200)
   comment    = models.TextField()
   created_at = models.DateTimeField(auto_now_add = True)
   updated_at = models.DateTimeField(auto_now = True)

