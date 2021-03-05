from django.db import models

class User(models.Model):

    username  = models.CharField(max_length=45)
    email     = models.CharField(max_length=45)
    password  = models.CharField(max_length=45)

    class Meta(object):
        db_table = "usernames"  
        db_table = "emails"
        db_table = "passwords"


        
        
        

        

