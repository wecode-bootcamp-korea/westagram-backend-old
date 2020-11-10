from django.db import models

class User(models.Model):
    name            = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=20)
    email           = models.CharField(max_length=50)
    password        = models.CharField(max_length=300)
    
    class Meta:
        db_table = 'users'

class Follow(models.Model):
    followed_user   = models.ForeignKey(
                                    User, 
                                    related_name='related_followed_user',  
                                    on_delete=models.CASCADE
                                    )

    following_user  = models.ForeignKey(
                                    User, 
                                    related_name='related_following_user', 
                                    on_delete=models.CASCADE
                                    )

    class Meta:
        db_table = 'follows'
