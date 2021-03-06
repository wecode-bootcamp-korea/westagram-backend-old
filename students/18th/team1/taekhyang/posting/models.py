from django.db import models


class Posting(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content      = models.CharField(max_length=2000)
    user         = models.ForeignKey('account.User', on_delete=models.CASCADE)
    liked_users  = models.ManyToManyField('account.User',
                                          through='PostingLike',
                                          related_name='liked_postings'
                                          )

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


class PostingLike(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user         = models.ForeignKey('account.User', on_delete=models.CASCADE)
    posting      = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'posting_likes'
