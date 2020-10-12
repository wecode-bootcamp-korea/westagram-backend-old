from django.db   import models
from user.models import User

# Create your models here.

class Post(models.Model):
    user      = models.ForeignKey(User, on_delete= models.CASCADE)
    content   = models.CharField(max_length=500)
    time      = models.DateTimeField(auto_now = True)

    class Meta :
        db_table = 'post'

class Image_urls(models.Model):
    image_url = models.URLField()
    post      = models.ForeignKey(Post, on_delete= models.CASCADE)

    class Meta :
        db_table = 'image_urls'