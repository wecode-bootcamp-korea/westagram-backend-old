from django.db import models

from Account.models import User

# 게시물 모델
class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 해당 게시물을 업로드한 유저의 id
    text = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    img_url = models.URLField(max_length=500)

# 댓글 모델
class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE) # 댓글이 달린 게시물
    text = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)