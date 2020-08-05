from django.db import models

from user.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.CharField(max_length = 300)
    img_url = models.URLField(default = "")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'post'