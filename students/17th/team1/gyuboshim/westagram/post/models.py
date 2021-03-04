import os
import sys

from django.db      import models

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from user.models    import User

class Post(models.Model):
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    content     =   models.CharField(max_length = 500)
    image_url   =   models.URLField()
    created_at  =   models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'
