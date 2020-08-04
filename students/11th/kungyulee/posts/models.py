from datetime import datetime 

from django.db import models

from accounts.models import User

class Post(models.Model):
    author    = models.ForeignKey(User, on_delete = models.CASCADE)
    contents  = models.TextField()
    image_url = models.URLField(max_length = 200, blank = False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author)

