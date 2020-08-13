from django.db import models

from .validators import validate_email, validate_number, validate_password

class User(models.Model):
    name         = models.CharField(max_length = 50, null = False)
    email        = models.EmailField(max_length = 50, validators = [validate_email])
    password     = models.CharField(max_length = 156, null = False, validators = [validate_password])
    phone_number = models.CharField(max_length = 50, validators = [validate_number])
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "users"

    def  __str__(self):
        return self.name
