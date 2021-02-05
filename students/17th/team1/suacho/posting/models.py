from django.db   import models
from user.models import User

class Posting(models.Model):
    writer     = models.CharField(max_length=100)
    content    = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'

class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    posting   = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'

class Comment(models.Model):
    writer     = models.CharField(max_length=100)
    content    = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting    = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
