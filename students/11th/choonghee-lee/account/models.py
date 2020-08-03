from django.db import models

class User(models.Model):
    username = models.CharField(max_length = 30, blank = True, unique = True)
    email    = models.EmailField(blank = True, unique = True)
    phone    = models.CharField(max_length = 30, blank = True, unique = True)
    password = models.CharField(max_length = 40, blank = False, null = False)

    class Meta:
        db_table = "users"