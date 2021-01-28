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
    image_url = models.CharField(max_length = 2000)
    post      = models.ForeignKey('Post', on_delete = models.CASCADE)

    class Meta:
        db_table = 'post_images'

class Comment(models.Model):
    post       = models.ForeignKey('Post', on_delete = models.CASCADE)
    writer     = models.ForeignKey(User, on_delete = models.CASCADE)
    recomment  = models.ForeignKey('Comment', on_delete = models.CASCADE, null=True)
    image_url  = models.CharField(max_length = 2000, null=True)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    class Meta:
        db_table= 'comments'

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)

    class Meta:
        db_table= 'post_likes' 