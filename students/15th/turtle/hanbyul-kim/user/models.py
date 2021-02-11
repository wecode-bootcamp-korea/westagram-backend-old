from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 100,unique=True,null = True)
    email = models.EmailField(max_length =200,verbose_name='email',unique = True,null = True)
    password = models.CharField(max_length =500)
    mobile_number = models.CharField(max_length = 500,null = True)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name

