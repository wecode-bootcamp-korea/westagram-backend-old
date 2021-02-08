from django.db import models
from user.models import User

class Posting(models.Model):
    username    = models.ForeignKey('user.User', on_delete=models.CASCADE) #Installedapps - Class
    image_url   = models.CharField(max_length=2000)
    created_at  = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=100, null=True)

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    comment_username = models.ForeignKey('user.User', on_delete=models.CASCADE)
    text             = models.TextField(max_length=300)
    created_at       = models.DateTimeField(auto_now_add=True)
    posting_photo    = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'