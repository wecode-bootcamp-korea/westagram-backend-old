from django.db import models
from user.models import Users

class Contents(models.Model):
    user            = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at      = models.DateTimeField()
    article         = models.CharField(max_length=300)

    class Meta:
        db_table    = 'contents'

    def __str__(self):
        return self.name

class Posts(models.Model):
    content         = models.ForeignKey(Contents, on_delete=models.CASCADE)
    image_url       = models.CharField(max_length=300)

    class Meta:
        db_table    = 'posts'

    def __str__(self):
        return self.name

class Comments(models.Model):
    parent_comment = models.ForeignKey('self', on_delete = models.CASCADE, null=True)
    content        = models.ForeignKey(Contents, on_delete = models.CASCADE)

    class Meta:
        db_table    = 'comments'

    def __str__(self):
        return self.name

class Likes(models.Model):
    user            = models.ForeignKey(Users, on_delete=models.CASCADE)
    content         = models.ForeignKey(Contents, on_delete=models.CASCADE)
    
    class Meta:
        db_table    = 'likes'

    def __str__(self):
        return self.name


