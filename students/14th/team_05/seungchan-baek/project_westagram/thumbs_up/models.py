from django.db import models

# Create your models here.

class ThumbsUp(models.Model):
    good     =   models.BooleanField(default=False)
    user     =   models.ForeignKey('user.User',    on_delete   = models.CASCADE)
    post     =   models.ForeignKey('post.Posting', on_delete   = models.CASCADE)

    class Meta:
        db_table = 'thumbup'

    def __str__(self):
        return self.name