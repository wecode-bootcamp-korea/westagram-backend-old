from django.db import models
from user.models import Users

# Create your models here.
class Posts(models.Model):
    user            = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at      = models.DateTimeField()
    image_url       = models.CharField(max_length=300)
    article         = models.CharField(max_length=300)

    class Meta:
        db_table    = 'posts'

    def __str__(self):
        return self.name

class Comments(models.Model):
    article         = models.CharField(max_length=300)
    user            = models.ForeignKey(Users, on_delete=models.CASCADE)
    post            = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at      = models.DateTimeField()

    class Meta:
        db_table    = 'comments'

    def __str__(self):
        return self.name

