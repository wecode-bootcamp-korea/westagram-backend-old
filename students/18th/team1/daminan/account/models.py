from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    relation = models.ManyToManyField('self', through='Follow', symmetrical=False)

    class Meta:
        db_table = "users"
        
 
class Follow(models.Model):
    following = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, related_name = "following")
    follower  = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, related_name = "follower")    
    
    class Meta:
        db_table = "follows"