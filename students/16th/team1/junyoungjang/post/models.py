from django.db     import models

from user.models   import User

class Post(models.Model):
    title      = models.CharField(max_length = 150)
    writer     = models.ForeignKey(User, on_delete = models.CASCADE)    
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'

class PostImage(models.Model):
    image_url = models.CharField(max_length = 2000, null=True)
    post      = models.ForeignKey('Post', on_delete = models.CASCADE)

    class Meta:
        db_table = 'post_images'