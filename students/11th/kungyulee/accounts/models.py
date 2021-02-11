from django.db import models
from django.core.validators import RegexValidator

from .validators import validate_number, validate_password

class User(models.Model):
    phone_number = models.CharField(
        validators = [validate_number],
        max_length = 13,
        blank      = False,
        unique     = True
    )
    password     = models.CharField(
        validators = [validate_password],
        max_length = 64,
        blank      = False
    )
    is_admin = models.BooleanField(
        default = False)

    def __str__(self):
        return self.phone_number
