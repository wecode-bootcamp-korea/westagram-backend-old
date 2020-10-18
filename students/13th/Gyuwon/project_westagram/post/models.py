from django.db   import models
from user.models import User

class Post(models.Model):
    time        = models.DateTimeField(auto_now_add = True)
    name        = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url   = models.URLField()
    content     = models.TextField(max_length=1000)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    time    = models.DateTimeField(auto_now_add = True)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    name    = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    name    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'