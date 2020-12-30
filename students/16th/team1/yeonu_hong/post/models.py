from django.db import models

# Create your models here.
class Post(models.Model):
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

class Image(models.Model):
    post  = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.CharField(max_length=2000)

    class Meta:
        db_table = 'images'