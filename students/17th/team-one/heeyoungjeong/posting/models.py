from django.db import models
from user.models import User


class Posting(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    image_url = models.URLField(null=True)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    like = models.ManyToManyField('user.User', through='UserPostingLike', related_name='like')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'Posting'


class Comment(models.Model):
    posting = models.ForeignKey('posting.Posting', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True)
    depth = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.content[:10]}'

    class Meta:
        db_table = 'Comment'


class UserPostingLike(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('posting.Posting', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}:{self.posting}'

    class Meta:
        db_table = 'UserPostingLike'