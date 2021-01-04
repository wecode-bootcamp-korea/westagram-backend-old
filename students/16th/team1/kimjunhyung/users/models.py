from django.db import models

class User(models.Model):
    email       = models.CharField(max_length = 45, unique = True)
    password    = models.BinaryField(max_length = 60)
    
    class Meta:
        db_table = "users"
    
class Follow(models.Model):
    follow_user     = models.ForeignKey("User", related_name = "follow", on_delete = models.CASCADE)
    following_user  = models.ForeignKey("User", related_name = "following", on_delete = models.CASCADE)

    class Meta:
        db_table = "follows"
    
