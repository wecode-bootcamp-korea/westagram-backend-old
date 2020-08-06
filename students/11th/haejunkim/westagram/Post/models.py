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


class Comment(models.Model):
    email      = models.ForeignKey(User, on_delete = models.CASCADE)
    post       = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment    = models.TextField(max_length = 300)
    created_at = models.DateTimeField(auto_now_add=True)

    class  Meta:
        db_table = "comments"

    def __str__(self):
        return self.email
