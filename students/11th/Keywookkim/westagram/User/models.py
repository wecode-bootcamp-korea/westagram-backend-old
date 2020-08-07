from django.db   import models
from django.conf import settings

from .validators import validate_email, validate_password

class User(models.Model):
    account      = models.CharField(max_length = 30)
    email        = models.EmailField(max_length = 50, validators = [validate_email])
    password     = models.CharField(max_length = 50, validators = [validate_password], null=False)
    phone_number = models.CharField(max_length = 50)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'accounts'

