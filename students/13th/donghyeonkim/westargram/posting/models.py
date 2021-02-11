from django.db   import models

from user.models import User

class Post(models.Model):
    time            = models.DateTimeField(auto_now_add=True)
    image_url       = models.CharField(max_length=1000)
    posting_comment = models.CharField(max_length=1000)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    likes           = models.ManyToManyField(
        User,
        related_name='likes'
    )

    class Meta:
        db_table = 'post'

class Comment(models.Model):
    comment     = models.CharField(max_length=1000)
    time        = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    post        = models.ForeignKey(Post, on_delete=models.CASCADE)
    response_to = models.IntegerField(null=True)

    class Meta:
        db_table = 'comment'