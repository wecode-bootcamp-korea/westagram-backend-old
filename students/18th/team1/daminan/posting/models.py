from django.db import models

from account.models import User


class Posting(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    img_url     = models.CharField(max_length=1000)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    # 외부 폴더에서 받아온 클래스는 ''를 붙이지 않는다.