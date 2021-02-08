from django.db      import models
from django.db.models.fields.related import ForeignKey
from django.utils   import timezone
from user.models    import User
# 이미 user가 FK 로 지정되어 있어서 MtoM으로 못씀,, 흠,,,
class Posting(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url   = models.URLField(max_length=2000)
    description = models.CharField(max_length=100, null=True)
    create_at   = models.DateTimeField(auto_now_add=True)
    userlike   = models.ManyToManyField('UserLike', through='Like')

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    posting     = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    comment     = models.CharField(max_length=100)
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'

class UserLike(models.Model):
    userlike   = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    userlike    = models.ForeignKey(UserLike, on_delete=models.CASCADE, null=True)
    posting     = models.ForeignKey(Posting, on_delete=models.CASCADE)
    create_at   = models.DateTimeField(auto_now_add=True, null=timezone.now())

    class Meta:
        db_table = 'likes'
