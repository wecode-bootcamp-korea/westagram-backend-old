from django.db                 import models
from django.db.models.deletion import CASCADE

class Posting(models.Model):
    user  = models.ForeignKey('user.User', on_delete=CASCADE)
    image = models.URLField(max_length=2000)
    text  = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postings'
