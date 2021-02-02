from django.db   import models
from user.models import User

class Post(models.Model):
    user_id    = models.ForeignKey('User.nickname', on_delete=models.CASCADE)
    img        = models.URLField(max_length=1000)
    content    = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "postings"    
