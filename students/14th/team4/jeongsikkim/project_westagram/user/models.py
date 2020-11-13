from django.db import models


class User(models.Model):
    user_name     = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=13)
    email         = models.EmailField(max_length=100)
    password      = models.CharField(max_length=1000)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.user_name

