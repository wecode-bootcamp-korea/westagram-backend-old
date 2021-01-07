from django.db      import models

class User(models.Model):
    account      = models.CharField(max_length = 20, null=True)
    password     = models.CharField(max_length= 200)
    email        = models.EmailField(max_length = 30, null=True)
    phone        = models.CharField(max_length = 20, null=True)
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

