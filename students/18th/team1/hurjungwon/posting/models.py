from django.db import models

from account.models import User


class Post(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    image_url   = models.URLField(max_length=2000)
    content     = models.TextField()
    user_name   = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'

