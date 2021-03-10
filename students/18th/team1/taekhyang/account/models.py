from django.db import models

class User(models.Model):
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=50, unique=True, null=True)
    password     = models.CharField(max_length=100)
    follow       = models.ManyToManyField('self', through='Follow', symmetrical=False)

    class Meta:
        db_table = 'users'


class Follow(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follow_by_from_user')
    to_user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follow_by_to_user')

    class Meta:
        db_table = 'follows'
