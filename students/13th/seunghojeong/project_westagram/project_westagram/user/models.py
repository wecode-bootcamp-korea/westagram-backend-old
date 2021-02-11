from django.db import models

class Users(models.Model):
    name         = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 50)
    email        = models.CharField(max_length = 200)
    password     = models.CharField(max_length = 100)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'Users'
