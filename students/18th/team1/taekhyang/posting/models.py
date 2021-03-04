from django.db import models


class Posting(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content      = models.CharField(max_length=2000, blank=True)
    user         = models.ForeignKey('account.User', on_delete=models.CASCADE)

    class Meta(object):
        db_table = 'postings'


class PostingImage(models.Model):
    image_url = models.TextField(max_length=1000)
    posting   = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta(object):
        db_table = 'posting_images'
