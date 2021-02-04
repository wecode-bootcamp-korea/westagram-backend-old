from django.db import models
from user.models import User

class Posting(models.Model):
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE) #Installedapps - Class
    image_url = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=100, null=True)

    class Meta:
        db_table = 'postings'
