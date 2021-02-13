from django.db    import models

from user.models  import Account

# Create your models here.

class Post(models.Model):
    user       = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    created_at = models.TimeField(auto_now_add = True, null=True)
    content    = models.TextField()
    image_url  = models.URLField()

    class Meta:
        db_table = 'posts'


class Comment(models.Model):
    user       = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.TimeField(auto_now_add=True, null=True)
    content    = models.TextField()

    class Meta:
        db_table = 'comments'
