from django.db   import models

from user.models import User

class Article(models.Model):
    head        = models.CharField(max_length = 50)
    body        = models.CharField(max_length = 5000)
    created_at  = models.DateTimeField(auto_now_add = True)
    update_at   = models.DateTimeField(auto_now = True)
    user        = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, related_name = 'article_user')
    like        = models.ManyToManyField(User, through='Like', related_name = 'article_like')
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'articles'

class Comment(models.Model):
    content = models.CharField(max_length = 1000)
    article = models.ForeignKey('Article', on_delete=models.SET_NULL, null=True)
    user   = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name = 'comment_user')

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'like_user')
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name = 'like_article')

    class Meta:
        db_table = 'likes'
