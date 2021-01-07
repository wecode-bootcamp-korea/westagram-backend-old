from django.db import models

class Article(models.Model):
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)
   # generated_date = models.TimeField
    content        = models.TextField()
    image_url      = models.URLField(max_length=200)

    class Meta:
        db_table = "articles" 
