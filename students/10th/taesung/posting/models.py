from django.db import models

class Article(models.Model):
    head = models.CharField(max_length = 50)
    body = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
