from django.db import models

class User(models.Model):

    username  = models.CharField(max_length=254)
    email     = models.EmailField(max_length=254)
    password  = models.CharField(max_length=254)

    class Meta(object):
        db_table = "users"