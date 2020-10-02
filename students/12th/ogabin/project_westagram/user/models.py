from django.db import models

class User(models.Model):
    name         = models.CharField(max_length = 200, unique = True)
    email        = models.EmailField(unique = True)
    password     = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length = 200, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "users"