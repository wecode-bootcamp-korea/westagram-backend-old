from django.db    import models
from django.utils import timezone

class Post(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    image_url  = models.URLField(max_length=500)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    comment    = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    post       = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent     = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True)

    class Meta:
        db_table = 'comments'

