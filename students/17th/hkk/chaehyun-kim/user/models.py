from django.db      import models
from django.utils   import timezone

class User(models.Model):
   email        = models.EmailField(max_length=100, unique=True)
   password     = models.CharField(max_length=300)
   name         = models.CharField(max_length=10, unique=True)
   phone_number = models.CharField(max_length=20, unique=True)
   create_at    = models.DateTimeField(auto_now_add=True)
   update_at    = models.DateTimeField(auto_now=True)

   def __str__(self):
       return f'{self.name}'

   class Meta:
       db_table = 'users'

class Follow(models.Model):
    user        = models.ForeignKey('User', on_delete=models.CASCADE)
    following   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
