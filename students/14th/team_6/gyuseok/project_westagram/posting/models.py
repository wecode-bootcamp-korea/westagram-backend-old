from django.db import models


class Post(models.Model):
    user     = models.ForeignKey('user.User',on_delete=models.CASCADE)
    date     = models.DateTimeField(auto_now=True)
    image    = models.CharField(max_length=1000)
    content  = models.TextField(null=True)

    class Meta:
        db_table = 'borad'


