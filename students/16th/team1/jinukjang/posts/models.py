from django.db import models

class Post(models.Model):

    title       = models.CharField(max_length=100)
    writer      = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    count_likes = models.IntegerField(default=0)

    class Meta:
        db_table = "posts"

class PostImage(models.Model):

    post    = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    img_url = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = "post_images"


class Comment(models.Model):
    
    post = models.ForeignKey('posts.Post',on_delete=models.CASCADE)
    user = models.ForeignKey('users.User',on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

class Like(models.Model):

    user = models.ForeignKey("users.User",on_delete=models.CASCADE)
    post = models.ForeignKey("Post",on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"
