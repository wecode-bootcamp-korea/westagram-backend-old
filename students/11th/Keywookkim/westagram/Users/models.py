from django.db import models

class Users(models.Model):
    user_id    = models.CharField(max_length = 30)
    email      = models.CharField(max_length = 50)
    password   = models.CharField(max_length = 50)
    phonenumber= models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = 'users'
