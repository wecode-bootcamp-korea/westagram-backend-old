from django.db import models

class User(models.Model):
    name         = models.CharField(max_length = 50, null = False)
    email        = models.EmailField(max_length = 50)
    password     = models.CharField(max_length = 50, null = False)
    phone_number = models.CharField(max_length = 50)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "users"

    def  __str__(self):
        return self.name
