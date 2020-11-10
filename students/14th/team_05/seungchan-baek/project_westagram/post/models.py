from django.db import models

class Posting(models.Model):
    content     = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at  = models.DateField(auto_now_add=True)
    author      = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'

    def __str__(self):
        return self.description
    
class Comment(models.Model):
    content    = models.TextField(null=True)
    postedtime = models.DateTimeField(auto_now_add=True)
    post       = models.ForeignKey('Posting', on_delete = models.CASCADE)
    user       = models.ForeignKey('user.User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.content