from django.db   import models

from user.models import User

class Post(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField() 
    caption   = models.CharField(max_length=500, null=True)
    user      = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='post')

    class Meta:
        db_table='posts'

class Comment(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    text      = models.CharField(max_length=1000)
    user      = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='comment')
    post      = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, related_name='comment')

    class Meta:
        db_table='comments'

class Like(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='like')
    post        = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, related_name='like')

    class Meta:
        db_table='likes'
