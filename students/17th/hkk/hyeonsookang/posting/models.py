from django.db import models

class Post(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title      = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    image      = models.URLField(max_length=200)

    class Meta:
        db_table = 'post'
