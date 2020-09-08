from django.db import models
from django.core.exceptions import ValidationError

def validate_email(email):
   if not '@' in email:
       raise ValidationError("Not a valid email")
   else:
       return email

class User(models.Model):
    name         = models.CharField(max_length = 20)
    email        = models.CharField(max_length = 20, validators=[validate_email])
    password     = models.CharField(max_length = 8)
    phone_number = models.CharField(max_length = 20)

    class Meta:
        db_table = 'users'