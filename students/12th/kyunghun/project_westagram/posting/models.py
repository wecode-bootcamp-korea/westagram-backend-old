from django.db          import models
from user.models        import User

class PostMedia(models.Model):
    title               = models.CharField(max_length=200)
    pub_date            = models.DateTimeField(auto_now_add = True) 
    content             = models.TextField()
    user                = models.ForeignKey(User, on_delete=models.CASCADE, null=False) 

    class Meta:
        db_table = 'postmedia'


class Photo(models.Model):
    post                = models.ForeignKey(PostMedia, on_delete=models.CASCADE, null=True)
    image               = models.URLField()
    
    class Meta:
        db_table = 'photos'

class Comment(models.Model):
    content             = models.CharField(max_lenght= 1000)
    post                = models.ForeignKey(PostMedia, on_delete= models.CASCADE, null= True)
    related_comment     = models.ForeignKey('self', on_delete= models.CASCADE, null= True)

    class Meta:
        db_table = 'comments'
