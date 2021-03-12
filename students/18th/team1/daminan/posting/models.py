from django.db import models

from account.models import User


class Posting(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    img_url     = models.CharField(max_length=1000)
    user        = models.ForeignKey('account.User', on_delete=models.CASCADE)
    # 외부 폴더에서 받아온 클래스는 ''를 붙이지 않는다

    class Meta:
        db_table = "postings"
        
class Comment(models.Model):
    update_time = models.DateTimeField(auto_now_add=True)
    comment     = models.CharField(max_length=2000)    
    image       = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user        = models.ForeignKey('account.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "comments"
        
class Like(models.Model):
    user_like = models.CharField(max_length=10, default='좋아요')
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    image     = models.ForeignKey('Posting', on_delete=models.CASCADE)
    class Meta:
        db_table = "likes"