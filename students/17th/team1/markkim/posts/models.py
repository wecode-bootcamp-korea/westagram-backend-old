from django.db import models


class Post(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField() 
    caption   = models.CharField(max_length=500, null=True)
    user      = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='post')

    class Meta:
        db_table='posts'
