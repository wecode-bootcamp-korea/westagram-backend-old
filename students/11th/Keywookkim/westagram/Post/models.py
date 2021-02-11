from django.db      import models
from django.conf    import settings


class Bulletin(models.Model) :
    account    = models.ForeignKey('User.User',on_delete=models.CASCADE)
    title      = models.CharField(max_length = 100)
    context    = models.TextField()
    img_url    = models.URLField(default='')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.title)
    
    class Meta :
        db_table = 'post'

class Comment(models.Model) :
    account      = models.ForeignKey('User.User', on_delete=models.CASCADE)
    bulletin     = models.ForeignKey('Bulletin', on_delete=models.CASCADE)
    commentbox   = models.TextField(max_length=1000)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.commentbox)
    
    class Meta :
        db_table = 'comment_table'
