from django.db      import models

# Create your models here.

class User(models.Model):
   email        = models.EmailField(max_length=100, unique=True)
   password     = models.CharField(max_length=300)
   name         = models.CharField(max_length=10, unique=True)
   phone_number = models.CharField(max_length=20, unique=True)

   def __str__(self):
       return f'{self.name}'

   class Meta:
       db_table = 'users'

