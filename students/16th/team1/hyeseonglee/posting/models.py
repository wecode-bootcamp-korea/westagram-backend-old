from django.db import models

class Post(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE) 
    email       = models.CharField(max_length=30, verbose_name='이메일', default='default@gmail.com')
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
