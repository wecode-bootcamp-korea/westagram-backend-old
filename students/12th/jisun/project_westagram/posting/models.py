from django.db      import models

from account.models import User

class Posting(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    image_url  = models.URLField()
    contents   = models.CharField(max_length = 300, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'posting'

class Commenting(models.Model):
    image_url        = models.ForeignKey(Posting, on_delete = models.CASCADE)
    user             = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at       = models.DateTimeField(auto_now_add = True)
    comment_contents = models.CharField(max_length = 100)
    class Meta:
        db_table = 'commenting'
