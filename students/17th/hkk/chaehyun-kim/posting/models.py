from django.db      import models
from django.db.models.fields.related import ForeignKey
from django.utils   import timezone
from user.models    import User

class Posting(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url   = models.URLField(max_length=2000)
    description = models.CharField(max_length=100, null=True)
    create_at   = models.DateTimeField(auto_now_add=True)
    like_user   = models.ManyToManyField(User, through='Like', related_name='like_user')

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    posting     = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    comment     = models.CharField(max_length=100)
    create_at   = models.DateTimeField(auto_now_add=True)
    parent      = models.ForeignKey('self', on_delete=models.CASCADE, related_name='recomment', null=True)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
