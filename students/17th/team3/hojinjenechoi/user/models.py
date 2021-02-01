from django.db import models

from django.core.validators import RegexValidator

# Create your models here.
class User(models.Model):
    email           = models.EmailField(max_length=200, unique=True, verbose_name='Username')#, validators=[validate_email])
    password        = models.CharField(max_length=200, verbose_name='Password') #, validators=[validate_password])
    nickname        = models.CharField(max_length=50)
    phone           = models.CharField(null=True, max_length=11, validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$')])
    registered_time = models.DateTimeField(auto_now_add=True)
    updated_time    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

