from django.db import models

from user.models import User

class Post(models.Model):
    author       = models.ForeignKey(User, on_delete = models.CASCADE)
    title        = models.CharField(max_length = 40)
    content      = models.TextField(max_length = 400, null = True)
    image        = models.URLField()
    post_created = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'post'


    def __str__(self):
        return self.title


