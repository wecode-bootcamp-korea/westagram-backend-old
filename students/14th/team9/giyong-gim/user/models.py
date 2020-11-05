from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    user_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
