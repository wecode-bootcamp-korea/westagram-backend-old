from django.db import models
from django.conf import settings
from pytz import timezone

class Posting(models.Model):
    image_url   = models.CharField(max_length=2000)
    description = models.TextField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    user        = models.ForeignKey('user.User', related_name='User', on_delete=models.CASCADE)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.created_at.astimezone(korean_timezone)

    @property
    def updated_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.updated_at.astimezone(korean_timezone)

    class Meta:
        db_table = 'postings'


class Comment(models.Model):
    text       = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting    = models.ForeignKey('Posting', on_delete=models.CASCADE)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)

        return self.created_at.astimezone(korean_timezone)

    class Meta:
        db_table = 'comments' 
