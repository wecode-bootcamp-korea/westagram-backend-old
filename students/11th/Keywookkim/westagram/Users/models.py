from django.db import models
from django.conf import settings
from pytz import timezone

class Users(models.Model):
    user_id    = models.CharField(max_length = 30)
    email      = models.CharField(max_length = 50)
    password   = models.CharField(max_length = 50)
    phonenumber= models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    @property
    def created_at_korean(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.created_at.astimezone(korean_timezone)
    
    class Meta:
        db_table = 'users'

