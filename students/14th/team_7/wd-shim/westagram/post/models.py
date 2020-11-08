import uuid

from django.db import models

class Post(models.Model):
    post_key = models.UUIDField(
        primary_key=True,
        default=uuid.uuid1,
        editable=False
    )
    post_desc = models.TextField(null=True)
    tags = models.TextField(null=True)
    location_info = models.CharField(max_length=500, null=True)
    pub_date = models.DateTimeField(auto_now=True)
    updated_pub_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"uuid:{self.post_key}, user_id:{self.user}, " \
               f"image_url:{self.updated_pub_date}, post_desc:{self.post_desc}"
    
    class Meta:
        db_table = 'posts'
        ordering = ['-updated_pub_date']

class PostImage(models.Model):
    img_name = models.CharField(max_length=100)
    img_url = models.CharField(max_length=500)
    img_format = models.CharField(max_length=5)
    img_size = models.CharField(max_length=30)
    upload_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'img_name:{self.img_name}, posting:{self.posting}, ' \
               f'img_url:{self.img_url}'
    
    class Meta:
        db_table = 'postimages'