from django.db import models

class Post(models.Model):
    user        = models.ForeignKey("users.User", on_delete = models.CASCADE)
    content     = models.TextField()
    image_url   = models.CharField(max_length = 200, null = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "posts"

class Comment(models.Model):
    user        = models.ForeignKey("users.User", on_delete = models.CASCADE)
    post        = models.ForeignKey("Post", on_delete = models.CASCADE)
    content     = models.CharField(max_length = 300)
    created_at  = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "comments"

class Like(models.Model):
    user = models.ForeignKey("users.User", on_delete = models.CASCADE)
    post = models.ForeignKey("Post", on_delete = models.CASCADE)
    
    class Meta:
        db_table = "likes"

class CommentByComment(models.Model):
    user        = models.ForeignKey("users.User", on_delete = models.CASCADE)
    comment     = models.ForeignKey("Comment", on_delete = models.CASCADE)
    content     = models.CharField(max_length = 100)
    created_at  = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "comment_by_comments"