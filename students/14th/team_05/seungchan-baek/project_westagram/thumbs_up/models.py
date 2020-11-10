from django.db import models

class ThumbsUp(models.Model):
    user = models.ForeignKey('user.User',    on_delete   = models.CASCADE)
    post = models.ForeignKey('post.Posting', on_delete   = models.CASCADE)

    class Meta:
        db_table = 'thumbs_up'