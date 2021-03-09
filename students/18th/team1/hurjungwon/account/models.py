from django.db import models


class User(models.Model):
    name         = models.CharField(max_length=45, null=True)
    user_name    = models.CharField(max_length=45, unique=True)
    phone_number = models.CharField(max_length=25, null=True, unique=True)
    email        = models.EmailField(max_length=245, unique=True)
    password     = models.CharField(max_length=300)
    follow       = models.ManyToManyField('self', through='Follow', symmetrical=False)

    class Meta:
        db_table = 'users'

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')

    class Meta:
        db_table = 'follows'
