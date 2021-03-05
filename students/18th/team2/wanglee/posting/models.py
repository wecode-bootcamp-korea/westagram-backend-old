from django.db      import models
from account.models import User

class Post(models.Model):
    user    = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    time    = models.DateTimeField(auto_now=False, auto_now_add=True)
    head    = models.CharField(max_length=300)
    body    = models.TextField()
    image   = models.CharField(max_length=2000)

    class Meta:
        db_table  = 'posts'

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    body = models.CharField(max_length=300)

    class Meta:
        db_table = 'replies'