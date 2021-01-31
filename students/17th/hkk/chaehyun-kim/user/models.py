from django.db      import models

# Create your models here.

class User(models.Model):
   email        = models.EmailField(max_length=100)
   password     = models.CharField(max_length=20)
   name         = models.CharField(max_length=10, default='stranger')
   phone_number = models.CharField(max_length=20, default=000)

   def __str__(self):
       return f'{self.name}'

   class Meta:
       db_table = 'users'

