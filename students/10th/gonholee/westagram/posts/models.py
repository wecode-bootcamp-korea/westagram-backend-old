from django.db import models

class Post(models.Model):
    user            =   models.ForeignKey('users.user',on_delete=models.CASCADE)
    post_text       =   models.CharField(max_length=1500)
    hearts          =   models.IntegerField(default=0)
    image_url       =   models.URLField()
    created_at      =   models.DateTimeField(auto_now_add=True)
    updated_at      =   models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    post            =   models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_text    =   models.CharField(max_length=300)
    created_at      =   models.DateTimeField(auto_now_add=True)
    updated_at      =   models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
