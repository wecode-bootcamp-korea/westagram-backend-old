from django.db import models

# Create your models here.

class User(models.Model):
    name       = models.CharField(max_length=30)
    password   = models.CharField(max_length=30)
    phone      = models.CharField(max_length=40)
    email      = models.EmailField(max_length=130)
#    following  = models.IntegerField(default=0)
#    follow     = models.ManyToManyField('self', through=Follow, related_name=)


    class Meta:
        db_table = 'users'

# class Follow(models.Model):
#     user     = models.ForeignKey('User', on_delete=models.CASCADE, related_name=to_follow)
#     follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name=from_follow)

#     class Meta:
#         db_table = 'follows'