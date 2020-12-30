from django.db import models

class User(models.model)
#    mobile_number = models.IntegerField() to be added
    email         = models.EmailField() # shall be unique
    full_name     = models.CharField()
    username      = models.CharField()
    password      = models.CharField() # shall be change as hashed password later

    class Meta:
        db_table = 'users'

