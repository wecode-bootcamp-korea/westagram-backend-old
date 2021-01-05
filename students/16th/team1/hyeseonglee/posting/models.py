from django.db import models


class Post(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE) 
    title       = models.CharField(max_length=100,unique=True, default='')
    content     = models.TextField(default='')
    created_dt  = models.DateTimeField(auto_now_add=True)
    image_url   = models.URLField(max_length=2800, default='')

    def __str__(self):
        return self.user
    
    class Meta:
        db_table            = 'postings'
        verbose_name        = 'post'
        verbose_name_plural = 'posts'
        ordering            = ('-created_dt',)


class Comment(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE) 
    post        = models.ForeignKey('posting.Post', on_delete=models.CASCADE)
    title       = models.CharField(max_length=100,unique=True,)
    content     = models.TextField()
    created_dt  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table            = 'comments'
        verbose_name        = 'comment'
        verbose_name_plural = 'comments'
        ordering            = ('-created_dt',)
