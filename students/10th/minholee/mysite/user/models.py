from django.db import models

class User(models.Model):
    name       = models.CharField(max_length = 255)
    email      = models.CharField(max_length = 511)
    password   = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email
