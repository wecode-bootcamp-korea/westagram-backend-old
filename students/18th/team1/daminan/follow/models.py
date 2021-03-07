from django.db import models

from account.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE, default='')
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE, default='')    
    # 포린키를 2번 쓰는데 이름을 두 가지로 나눠서 쓴다.
    class Meta:
        db_table = "follows"