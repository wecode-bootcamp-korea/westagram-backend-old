from django.db import models

class Account(models.Model):
    email    = models.EmailField()
    name     = models.CharField(max_length=20)
    nicname  = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

    def __Str__(self):
        return f'{self.name} : {self:email}'
    class Meta:
        db_table = 'accounts'


