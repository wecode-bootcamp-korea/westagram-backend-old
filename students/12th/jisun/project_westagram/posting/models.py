from django.db      import models

from account.models import Users

class Posting(models.Model):
    writer      = models.ForeignKey(Users, on_delete = models.CASCADE)
    image_url  = models.URLField()
    contents   = models.CharField(max_length = 300, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'posting'
