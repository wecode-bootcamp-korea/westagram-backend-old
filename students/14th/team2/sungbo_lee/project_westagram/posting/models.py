from django.db import models

class Posting(models.Model):
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)
    time         = models.DateField(auto_now_add=True)
    post_content = models.CharField(max_length=2000)
    image_url    = models.URLField(max_length=200)

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    comment_posting = models.ForeignKey('Posting', on_delete=models.CASCADE)
    comment_user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    comment_time    = models.DateField(auto_now=True)
    comment_content = models.TextField()

    class Meta:
        db_table = 'comments'
