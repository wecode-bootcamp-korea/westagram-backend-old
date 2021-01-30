from django.db import models

class Accounts(models.Model):
    email        = models.EmailField(max_length=300)
    name         = models.CharField(max_length=300)
    nickname     = models.CharField(max_length=300)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=300)
    create_at    = models.DateTimeField(auto_now_add=True)
    update_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "accounts" 

