from django.db   import models
from .validation import validate_email, validate_password


class User(models.Model):
    name         = models.CharField(max_length  = 20)
    email        = models.EmailField(max_length = 50, validators = [validate_email])
    password     = models.CharField(max_length  = 50, validators = [validate_password])
    phone_number = models.CharField(max_length  = 50)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now     = True)


