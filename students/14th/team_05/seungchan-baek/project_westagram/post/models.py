from django.db import models

# from user.models import User
# Create your models here.

class Posting(models.Model):
    content       =  models.TextField(null=True)
    description   =  models.TextField(null=True)
    postedtime    =  models.DateField(auto_now_add=True)
    author        =  models.ForeignKey('user.User', on_delete=models.CASCADE)
    # users       =  models.ForeignKey('User', on_delete=models.CASCADE)
    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.name

    
class Comment(models.Model):
    content       =  models.TextField(null=True)
    postedtime    =  models.DateTimeField(auto_now_add=True)
    post          =  models.ForeignKey('Posting', on_delete = models.CASCADE)
    user          =  models.ForeignKey('user.User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.name
