from django.db  import models

class User(models.Model):
    email    = models.CharField(max_length=30)
    password = models.CharField(max_length=18)
    account  = models.CharField(max_length=12, null=True)
    phone_number = models.CharField(max_length=12, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

