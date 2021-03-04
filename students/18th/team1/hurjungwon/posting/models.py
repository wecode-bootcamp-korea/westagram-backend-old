from django.db import models

from account.models import User


class Post(models.Model):
    create_date = models.DateField(auto_now_add=True)
    image_url   = models.CharField(max_length=2000)
    user_name   = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'