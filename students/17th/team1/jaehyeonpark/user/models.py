from django.db      import models

import posting

class User(models.Model):
    email        = models.EmailField(max_length=255, null=False, unique=True)
    password     = models.TextField(max_length=500, null=False)
    phone_number = models.TextField(max_length=1000, null=False, unique=True)
    account      = models.TextField(max_length=1000, null=False, unique=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    follow       = models.ManyToManyField('self', through='posting.Follow', symmetrical=False)

    class Meta:
        db_table = 'users'