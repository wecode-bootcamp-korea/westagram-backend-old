from django.db import models

# Create your models here.
class Account(models.Model):
    email      = models.EmailField(max_length=200)
    password   = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Accounts'
    def __str__(self):
        return self.name


