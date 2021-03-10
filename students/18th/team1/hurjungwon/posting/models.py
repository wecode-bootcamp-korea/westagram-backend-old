from django.db import models

from account.models import User


class Post(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    image_url   = models.URLField(max_length=2000)
    content     = models.TextField()
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_user  = models.ManyToManyField(User, through='Like', related_name='liked_user')
    likes       = models.IntegerField(default=0)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    content     = models.CharField(max_length=300)
    create_date = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    post        = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'