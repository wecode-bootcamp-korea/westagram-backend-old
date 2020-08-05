from django.db import models

from User.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    content    = models.TextField(default = "")
    img_url    = models.URLField(default = "")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "postings"

    def __str__(self):
        return self.user
