from django.db import models


class SignUp(models.Model):
    email = models.EmailField(max_length=45,unique=False,null=True)
    tel = models.CharField(max_length=20,unique=False,null=True)
    name = models.CharField(max_length=30,blank=True,null=True)
    password = models.CharField(max_length=45,null=True)



    class Meta:
        db_table = 'signups'

