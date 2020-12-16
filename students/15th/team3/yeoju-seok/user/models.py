from django.db import models

class Account(models.Model):
    email      = models.EmailField(max_length=200, unique=True),
    password   = models.CharField(max_length=200),
    updated_at = models.DateTimeField(auto_now=True),
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Accounts'
    def __str__(self):
        return self.name


