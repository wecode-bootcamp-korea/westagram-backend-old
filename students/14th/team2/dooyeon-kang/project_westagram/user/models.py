from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=80)
    email    = models.EmailField()
    phone    = models.CharField(max_length=20)
    password = models.CharField(max_length=2000)
    posting  = models.ManyToManyField('posting.Posting', related_name='User', through='Like')

    class Meta:
        db_table = 'users'

class Like(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    posting = models.ForeignKey('posting.Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class Profile(models.Model):
    description = models.TextField(null=True)
    image_url   = models.CharField(max_length=2000)
    user        = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_profiles'
