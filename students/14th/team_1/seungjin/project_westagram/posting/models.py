from django.db import models
from user.models import User

class Content(models.Model):
    user            = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    article         = models.CharField(max_length=300)

    class Meta:
        db_table    = 'contents'

class Post(models.Model):
    content         = models.ForeignKey(Content, on_delete=models.CASCADE)
    image_url       = models.URLField(max_length=200)

    class Meta:
        db_table    = 'posts'

class Comment(models.Model):
    parent_content = models.ForeignKey(
                            Content, 
                            related_name='related_parent_content',  
                            on_delete = models.CASCADE, null=True
                            )

    content        = models.ForeignKey(
                            Content, 
                            related_name='related_content', 
                            on_delete = models.CASCADE
                            )

    class Meta:
        db_table    = 'comments'

class Like(models.Model):
    user            = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content         = models.ForeignKey(Content, on_delete=models.CASCADE)
    
    class Meta:
        db_table    = 'likes'

