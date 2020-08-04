from django.db import models

class User(models.Model):
    name     = models.CharField(max_length = 50)
    email    = models.CharField(max_length = 50, unique = True)
    phone    = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 50)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.name