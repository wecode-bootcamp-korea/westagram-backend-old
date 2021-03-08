from django.db   import models
from user.models import User

class Posting(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    image       = models.URLField(max_length=2000)
    content     = models.TextField(null=True)

    class Meta:
        db_table = 'postings'