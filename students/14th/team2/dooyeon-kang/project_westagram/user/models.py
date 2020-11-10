from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=80)
    email         = models.EmailField()
    profile_image = models.CharField(max_length=2000, null=True)
    phone         = models.CharField(max_length=20)
    password      = models.CharField(max_length=2000)
    posting       = models.ManyToManyField('posting.Posting', related_name='likes', through='Like')
    follow        = models.ManyToManyField('self', related_name='follows', through='Follow')

    class Meta:
        db_table = 'users'

class Like(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    posting = models.ForeignKey('posting.Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class Follow(models.Model):
    follower = models.ForeignKey('User', related_name='follower', on_delete=models.CASCADE)
    followee = models.ForeignKey('User', related_name='followee', on_delete=models.CASCADE)

    class Meta:
        db_table = 'follows'
