from django.db import models

class User(models.Model):
    email    = EmailField(max_length=50)
    password = CharField(max_length=30)

