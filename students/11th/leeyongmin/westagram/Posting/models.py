from django.db import models

from Account.models import User

class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 해당 게시물을 업로드한 유저의 id
    text = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    img_url = models.URLField(max_length=500)