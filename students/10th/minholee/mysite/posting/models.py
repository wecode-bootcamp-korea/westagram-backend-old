from django.db   import models
from user.models import User

class Post(models.Model):

    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    content    = models.CharField(max_length = 5000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'postings'

class Comment(models.Model):

    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    post       = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment    = models.CharField(max_length = 5000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'comments'
