from django.db import models

from user.models import Users
# Create your models here.

class PostMedia(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add = True) # 생성된 시간 
    #models.DateTimeField('date published')
    content = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False) #Users table
    

class Photo(models.Model):
    post = models.ForeignKey(PostMedia, on_delete=models.CASCADE, null=True)
    image = models.TextField()
    #image = models.ImageField(upload_to='images/', blank=True, null=True)