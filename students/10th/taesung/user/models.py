from django.db import models

class User(models.Model):
    email      = models.CharField(max_length = 1000)
    password   = models.CharField(max_length = 300)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'members'
