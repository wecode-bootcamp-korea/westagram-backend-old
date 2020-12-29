from django.db import models

class Post(models.Model):
    user        = models.ForeignKey("users.User", on_delete = models.CASCADE)
    content     = models.TextField()
    image_url   = models.CharField(max_length = 200, null = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    def get_first_comment(post):
        first_comment = Comment.objects.select_related("post").filter(post = post)
        if first_comment.exists():
            return first_comment[0].content
        return "댓글을 입력해주세요"

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
