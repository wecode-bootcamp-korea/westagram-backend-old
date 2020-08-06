from django.db   import models

from User.models import User

class Post(models.Model):
    email      = models.ForeignKey(User, on_delete = models.CASCADE)
    content    = models.TextField(max_length = 300)
    image_url  = models.URLField()
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "posts"

    def  __str__(self):
        return self.email
