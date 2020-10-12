from django.db import models
from user.models import User 

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    img_url = models.CharField(max_length=245)
    content = models.TextField()

    class Meta:
        db_table = 'posts'
