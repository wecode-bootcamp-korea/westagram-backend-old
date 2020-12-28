from django.db import models


class SignUp(models.Model):
    email    = models.EmailField(max_length=45)
    tel      = models.CharField(max_length=20,null=True)
    name     = models.CharField(max_length=30,null=True)
    password = models.CharField(max_length=45)



    class Meta:
        db_table = 'signups'