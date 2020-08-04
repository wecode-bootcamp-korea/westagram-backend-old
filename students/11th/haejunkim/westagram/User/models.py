from django.db import models

from .validation import validate_email, validate_password

class User(models.Model): 
    email          = models.EmailField(
        max_length = 50,
        validators = [validate_email],
        unique     = True,
    )
    password       = models.CharField(
        max_length = 300,
        validators = [validate_password],
    )
