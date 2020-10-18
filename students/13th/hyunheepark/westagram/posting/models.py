from django.db   import models 

# Create your models here.

class Post(models.Model):
    user       = models.ForeignKey('user.User',on_delete=models.CASCADE)  
    commenter  = models.ManyToManyField('user.User', through='Comment', related_name='user')
    created_at = models.DateTimeField(auto_now_add=True)
    img_url    = models.CharField(max_length=245)
    content    = models.TextField()

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    user            = models.ForeignKey('user.User',on_delete=models.CASCADE)
    post            = models.ForeignKey('Post',on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField()

    class Meta:
        db_table = 'comments'
    
