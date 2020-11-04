from django.db import models

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length= 100, null = True)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return self.email
            
