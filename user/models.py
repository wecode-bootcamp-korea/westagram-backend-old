from django.db import models

class Users(models.Model):
        email            = models.EmailField(
                max_length = 50,
                #validators = [validate_email],
                #unique     = True,                       
        )
        name           = models.CharField(max_length=50)
        password        = models.CharField(
                max_length = 300,
                #validators = [validate_password],
        )
        phone_number    = models.CharField(max_length=50)
        created_at      = models.DateTimeField(auto_now_add = True)
        updated_at      = models.DateTimeField(auto_now = True)

