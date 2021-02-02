from django.db   import models

from user.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE) 
    image_url  = models.URLField(max_length=500)
    content    = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'posts'
