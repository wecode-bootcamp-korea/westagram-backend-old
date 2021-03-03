from django.db import models

class User(models.Model):
    email    = models.EmailField()
    password = models.CharField(max_length=50)
    
    class Meta(object):
        db_table = 'users'
