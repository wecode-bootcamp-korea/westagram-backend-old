from django.db   import models

from user.models import User

class Article(models.Model):
    head        = models.CharField(max_length = 50)
    body        = models.CharField(max_length = 500)
    created_at  = models.DateTimeField(auto_now_add = True)
    update_at   = models.DateTimeField(auto_now = True)
    user        = models.ForeignKey('user.User', on_delete = models.SET_NULL, null=True)

    class Meta:
        db_table = 'articles'

class Comment(models.Model):
    content = models.CharField(max_length = 2000)
    article = models.ForeignKey('Article', on_delete=models.SET_NULL, null=True)
    email   = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'comments'
