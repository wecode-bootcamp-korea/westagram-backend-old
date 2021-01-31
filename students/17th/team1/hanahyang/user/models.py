from django.db   import models

class User(models.Model):
    email    = models.EmailField(max_length=50, null=True, unique=True) 
    name     = models.CharField(max_length=20, null=True, unique=True) 
    phone    = models.CharField(max_length=15, null=True, unique=True)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'

