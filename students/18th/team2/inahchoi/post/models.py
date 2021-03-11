from django.db      import models

from User.models    import User

class Post(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    time    = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image   = models.URLField()