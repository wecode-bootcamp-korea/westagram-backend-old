from django.db      import models
from user.models    import Account

class Post(models.Model):
    author      = models.ForeignKey(Account, on_delete=models.CASCADE)
    content     = models.TextField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    image_url   = models.URLField(max_length=500, null=True)

    class Meta:
        db_table: 'posts'


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete = models.CASCADE)
    author     = models.ForeignKey(Account, on_delete = models.CASCADE)
    content    = models.TextField(max_length = 240)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'comments'