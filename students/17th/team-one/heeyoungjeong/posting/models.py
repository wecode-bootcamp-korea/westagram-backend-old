from django.db import models
from user.models import User


class Posting(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    image_url = models.URLField(null=True)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)


    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'Posting'