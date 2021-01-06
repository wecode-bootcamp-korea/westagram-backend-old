from django.db   import models

from user.models import User

class Post(models.Model):
    user      = models.ForeignKey('user.User', on_delete = models.CASCADE)
    img_url   = models.URLField()
    content   = models.TextField(max_length = 300)
    create_at = models.DateTimeField(auto_now_add = True)

    class Meta :
        db_table = 'posts'
