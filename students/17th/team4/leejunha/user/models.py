from django.db import models


class Account(models.Model):
    email    = models.EmailField(max_length=254)
    password = models.CharField(max_length=400)

    class Meta:
        db_table = "accounts"
