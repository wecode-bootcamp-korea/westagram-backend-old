from django.db    import models
from django.utils import timezone
from user.models  import User


class Board(models.Model):
    name     = models.CharField(max_length=45)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    time     = models.DateTimeField(default=timezone.now)
    image    = models.CharField(max_length=200, blank=True)
    contents = models.TextField()

    class Meta:
        db_table = 'boards'

class Comment(models.Model):
    board_title  = models.ForeignKey(Board, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_tiem = models.DateTimeField(default=timezone.now)
    comment_body = models.CharField(max_length=100)

    class Meta:
        db_table = 'comments'

# Create your models here.
