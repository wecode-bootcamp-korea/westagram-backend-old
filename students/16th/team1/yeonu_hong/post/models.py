from django.db import models

# Create your models here.
class Post(models.Model):
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    pub_date  = models.DateTimeField(auto_now_add=True)
    likes     = models.IntegerField(default=0)

    class Meta:
        db_table = 'posts'

class Image(models.Model):
    post  = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.URLField(max_length=2100)

    class Meta:
        db_table = 'images'

class Comment(models.Model):
    post     = models.ForeignKey('Post', on_delete=models.CASCADE)
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content  = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'comments'

class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
