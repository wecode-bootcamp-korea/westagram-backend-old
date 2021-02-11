from django.db    import models
from django.utils import timezone
from user.models  import User


class Board(models.Model):
    name      = models.CharField(max_length=45)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    time      = models.DateTimeField(default=timezone.now)
    image_url = models.URLField(max_length=200)
    contents  = models.TextField()

    class Meta:
        db_table = 'boards'

class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    tiem  = models.DateTimeField(default=timezone.now)
    body  = models.CharField(max_length=100)

    class Meta:
        db_table = 'comments'

