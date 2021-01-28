from django.db import models

class Id(models.Model):
    email = models.CharField(max_length=30)

    class Meta:
        db_table = 'ids'

class Password(models.Model):
    password = models.CharField(max_length=30)
    ids      = models.ForeignKey('Id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'passwords'
# Create your models here.
