from django.db import models


class User(models.Model):
    
    name = models.CharField(max_length=50,  null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=100)
    hashed_password = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
	    return self.name


