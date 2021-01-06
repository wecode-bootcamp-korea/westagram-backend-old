from django.db import models

class User(models.Model):

    username = models.CharField(unique=True, max_length=10)
    password = models.CharField(max_length=100)
    name     = models.CharField(max_length=10, null=True)
    email    = models.EmailField(unique=True, null=True)
    phone    = models.CharField(unique=True, max_length=45, null=True)
    
    class Meta:
        db_table = "users"

class Follow(models.Model):

    from_user = models.ForeignKey('User', related_name="from_follows", on_delete=models.CASCADE)
    to_user   = models.ForeignKey('User', related_name="to_follows", on_delete=models.CASCADE)

    class Meta:
        db_table = "follows"

