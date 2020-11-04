from django.db import models

from user.models import User

class Posting(models.Model):
    posting_date    = models.DateTimeField(auto_now_add=True)
    img_url         = models.URLField(max_length=2000)
    contents        = models.TextField(max_length=200, null=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'
