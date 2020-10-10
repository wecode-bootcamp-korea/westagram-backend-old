from django.db   import models
from user.models import User

class Post(models.Model):
    time            = models.DateTimeField(auto_now_add=True)
    image_url       = models.CharField(max_length=1000)
    posting_comment = models.CharField(max_length=1000)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post'