from django.db import models

# Create your models here.

class User(models.Model):
    #objects = models.Manager()
    name     = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=30, blank=True)
    phone    = models.CharField(max_length=40, blank=True)
    email    = models.EmailField(max_length=130, blank=True)

    class Meta:
        db_table = 'users'

class Post(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    image    = models.CharField(max_length=2000)

    class Meta:
        db_table = 'posts'
