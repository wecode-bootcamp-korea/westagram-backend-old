from django.db   import models
from user.models import Account

class Posting(models.Model):
    account     = models.ForeignKey('user.Account', on_delete=models.SET_NULL, null = True)
    create_date = models.DateField(auto_now_add=True)
    image_url   = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True)

    class Meta:
        db_table = 'postings'
