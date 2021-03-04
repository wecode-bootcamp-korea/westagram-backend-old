from django.db              import models

# Create your models here.
class User(models.Model):
    email         = models.EmailField(max_length=50)
    phone         = models.CharField(max_length=11, null=True, blank=True)
    full_name     = models.CharField(max_length=40, null=True, blank=True)
    user_name     = models.CharField(max_length=20, null=True, blank=True)
    password      = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'users'
