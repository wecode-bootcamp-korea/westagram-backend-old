from django.db import models

class User(models.Model):
    name     = models.CharField(max_length = 30, null = True, unique = True)
    email    = models.EmailField(null = True, unique = True)
    phone    = models.CharField(max_length = 30, null = True, unique = True)
    password = models.CharField(max_length = 40, blank = False, null = False)

    class Meta:
        db_table = "users"