from django.db import models

from .validation import Validate_email,Validate_password,Validation_phone

class User(models.Model):
    email = models.EmailField(
        max_length = 50,
        validators = [Validate_email],
        unique = True,
    )
    phone = models.CharField(
        max_length = 30,
        validators = [Validation_phone],
        )
    password = models.CharField(
        max_length = 300,
        validators = [Validate_password],
        )
    class Meta:
        db_table = 'user'

        

    
