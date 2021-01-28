from django.db import models
from django.views.generic.edit import CreateView

class Post(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE) 
    title       = models.CharField(max_length=100, default='')
    content     = models.TextField(default='')
    created_dt  = models.DateTimeField(auto_now_add=True)
    image_url   = models.URLField(max_length=2800, default='',null=True)
    like_num    = models.IntegerField(default=0)
    
    class Meta:
        db_table            = 'postings'
        verbose_name        = 'post'
        verbose_name_plural = 'posts'
        ordering            = ('-created_dt',)


class Comment(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE) 
    post        = models.ForeignKey('posting.Post', on_delete=models.CASCADE, related_name='comments')
    parent      = models.ForeignKey('posting.Comment', on_delete=models.CASCADE, related_name='parent_comment', null=True)
    title       = models.CharField(max_length=100)
    content     = models.TextField()
    created_dt  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    depth       = models.IntegerField(default=0)
    
    class Meta:
        db_table            = 'comments'
        verbose_name        = 'comment'
        verbose_name_plural = 'comments'
        ordering            = ('-created_dt',)


class Like(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post        = models.ForeignKey('posting.Post', on_delete=models.CASCADE)
    created_dt  = models.DateTimeField(auto_now_add=True)
  
    class Meta:
        db_table = 'likes'
        verbose_name        = 'like'
        verbose_name_plural = 'likes'
        ordering            = ('-created_dt',)