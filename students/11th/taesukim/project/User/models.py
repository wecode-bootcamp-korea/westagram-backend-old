from django.db import models

class User(models.Model):
    email        = models.CharField(max_length = 50)
    password     = models.CharField(max_length = 300)
    name         = models.CharField(max_length = 50, null=True)
    phone_number = models.CharField(max_length = 50, null=True)

    def __str__(self):
        return self.email

class Follow(models.Model):
    following_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'following_user')
    followed_user  = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'followed_user')
