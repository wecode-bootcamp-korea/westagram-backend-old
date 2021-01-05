from django.db import models

# Create your models here.
class Post(models.Model):
    author     = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='posts')
    title      = models.CharField(max_length=255)
    content    = models.TextField()
    image_url  = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return f"{self.author.pk}'s post"

    
