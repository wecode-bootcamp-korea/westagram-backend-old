from django.db import models

class Accounts(models.Model):
    email        = models.EmailField(max_length=300)
    name         = models.CharField(max_length=300)
    nickname     = models.CharField(max_length=300)
    password     = models.BinaryField()
    phone_number = models.CharField(max_length=300)
    create_at    = models.DateTimeField(auto_now_add=True)
    update_at    = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.email

    class Meta:
        db_table = "accounts" 

class Follow(models.Model):
    following = models.ForeignKey('accounts', related_name='following', on_delete=models.CASCADE)
    follower  = models.ForeignKey('accounts', related_name='follower', on_delete=models.CASCADE)

    class Meta:
        db_table = "follow"
