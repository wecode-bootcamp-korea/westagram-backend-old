from django.db import models


class Posting(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content      = models.CharField(max_length=2000)
    user         = models.ForeignKey('account.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'


class PostingImage(models.Model):
    image_url = models.TextField(max_length=1000)
    posting   = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'posting_images'


class Comment(models.Model):
    posting      = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user         = models.ForeignKey('account.User', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    content      = models.CharField(max_length=2000)

    class Meta:
        db_table = 'comments'
