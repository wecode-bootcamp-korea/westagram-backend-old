from django.db                     import models
from phonenumber_field.modelfields import PhoneNumberField

class User(models.Model):
    name          = models.CharField(max_length=30, null=True)
    email         = models.EmailField(null=True)
    phone_number  = PhoneNumberField(null=True)
    password      = models.CharField(max_length=300)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='users'
