from django.db import models

class Board(models.Model):
    user_name = models.CharField(max_length=10)
    upload_time = models.TimeField()
    image_url = models.CharField(max_length=200)

    class Meta:
        db_table : 'boards'
# Create your models here.
