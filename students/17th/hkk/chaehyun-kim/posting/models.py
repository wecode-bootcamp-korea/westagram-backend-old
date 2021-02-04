from django.db      import models
from django.utils   import timezone
from user.models    import User

class Posting(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url   = models.URLField(max_length=2000)
    description = models.CharField(max_length=100, null=True)
    create_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'postings'
