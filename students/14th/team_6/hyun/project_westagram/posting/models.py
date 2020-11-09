from django.db import models
from django.utils import timezone
from user.models  import User
from user.views import LogInView

class Post(models.Model):
    user_name =  models.ForeignKey('user.User', on_delete= models.CASCADE)
    title = models.CharField(max_length= 200)
    content  = models.TextField(null = True)
    date = models.DateTimeField(default = timezone.now)
#    img_url = models.ImageField(upload_to = 'images/' , blank = True , null = True),

    def __str__(self):
        return self.title

class Photo(models.Model):
    post = models.ForeignKey('Post' , on_delete = models.CASCADE, null = True)
    image = models.ImageField(upload_to = 'images/' , blank =True , null =True)

