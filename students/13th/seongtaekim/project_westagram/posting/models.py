from django.db   import models
from user.models import User

# Create your models here.

class Post(models.Model):
    user     = models.ForeignKey(User, on_delete= models.CASCADE)
    contents = models.CharField(max_length=500)
    time     = models.DateTimeField(auto_now = True)
    user     = models.ManyToManyField('user.User', through = 'Like')

    class Meta :
        db_table = 'post'

class Image_urls(models.Model):
    image_url = models.URLField()
    post      = models.ForeignKey(Post, on_delete= models.CASCADE)

    class Meta :
        db_table = 'image_urls'

class Comment(models.Model):
    user      = models.ForeignKey(User, on_delete= models.CASCADE)
    post      = models.ForeignKey(Post, on_delete= models.CASCADE)
    contents  = models.CharField(max_length=200)
    time      = models.DateTimeField(auto_now = True)

    class Meta :
        db_table = 'comment'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey('user.User', on_delete= models.CASCADE)

    class Meta :
        db_table = 'like_check'