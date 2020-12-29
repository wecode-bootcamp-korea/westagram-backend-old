from django.db import models

# Create your models her.
class User(models.Model):
    name          = models.CharField(max_length=50)
    email         = models.EmailField(max_length=50)
    phone_number  = models.CharField(max_length=50)
    password      = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return "{}".format(self.full_name)
    



    
    



    

