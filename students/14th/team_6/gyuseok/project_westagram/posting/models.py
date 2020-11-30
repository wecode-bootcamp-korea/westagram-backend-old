from django.db import models

class Post(models.Model):
    user        = models.ForeignKey('user.User',on_delete=models.CASCADE)

    created_at  = models.DateTimeField(auto_now_add=True)
    image_url   = models.URLField(max_length=1000)
    content     = models.TextField(null=True)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post        = models.ForeignKey('Post', on_delete=models.CASCADE)

    created_at  = models.DateTimeField(auto_now_add=True)
    content     = models.TextField(null=True)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post        = models.ForeignKey('Post',on_delete=models.CASCADE)

    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
