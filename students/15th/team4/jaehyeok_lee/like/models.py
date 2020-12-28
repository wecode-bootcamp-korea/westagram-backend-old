from django.db    import models
from django.utils import timezone

from user.models import User
from post.models import Post

class Like(models.Model):
    like_user  = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    datetime   = models.DateTimeField(default = timezone.now)
    class Meta:
        db_table = 'likes'
