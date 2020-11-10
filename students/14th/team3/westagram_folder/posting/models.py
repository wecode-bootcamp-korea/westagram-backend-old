from django.db      import models
from user.models    import Account

class Post(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    content         = models.TextField()
    post_time       = models.DateTimeField(auto_now_add=True)
    image_url       = models.URLField(max_length=500)

    class Meta:
        db_table: 'posts'


