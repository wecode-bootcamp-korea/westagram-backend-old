from django.db   import models
from user.models import User

class Post(models.Model):
    time    = models.DateTimeField(auto_now_add = True)
    name    = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url   = models.URLField()
    content = models.TextField(max_length=300)

    class Meta:
        db_table = 'posts'



