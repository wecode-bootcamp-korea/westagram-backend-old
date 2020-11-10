import uuid

from django.db import models

class Post(models.Model):
    post_key = models.UUIDField(
        primary_key = True,
        default     = uuid.uuid1,
        editable    = False
    )
    post_desc     = models.TextField(null=True)
    tags          = models.TextField(null=True)
    location_info = models.CharField(max_length=500, null=True)
    created_at    = models.DateTimeField(auto_now=True)
    updated_at    = models.DateTimeField(auto_now_add=True)
    is_deleted    = models.BooleanField(default=False)
    user          = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"uuid:{self.post_key}, user_id:{self.user}, " \
               f"updated_at:{self.updated_at}, post_desc:{self.post_desc}"
    
    class Meta:
        db_table = 'posts'
        ordering = ['-updated_at']

class PostImage(models.Model):
    img_name   = models.CharField(max_length=100)
    img_url    = models.URLField(max_length=500)
    img_format = models.CharField(max_length=5)
    img_size   = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    post       = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'img_name:{self.img_name}, post:{self.post}, ' \
               f'img_url:{self.img_url}'
    
    class Meta:
        db_table = 'post_images'

class Comment(models.Model):
    comment    = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    post       = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'comment{self.comment}, created_at{self.created_at}' \
               f'post{self.post}'
    
    class Meta:
        db_table = 'comments'
        ordering = ['updated_at']