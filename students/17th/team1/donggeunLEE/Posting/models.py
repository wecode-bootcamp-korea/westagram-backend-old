from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BLANK_CHOICE_DASH

# Create your models here.

class UserPosting(models.Model):
    user_ID    = models.ForeignKey('User.Userinfo', on_delete=models.SET_NULL, null=True)
    create_at  = models.DateTimeField(auto_now=True)
    image_url  = models.CharField(max_length=500)

    like       = models.ManyToManyField('User.Userinfo', related_name='Userlike', blank = True)

    def __str__(self):
        return f'{self.user_ID.name}'

    class Meta:
        db_table =  'userposting'


# User가 여러개의 포스팅에 좋아요를 누를 수 있고 posting 이 여러명한테 받을 수 있음 MtoM
class Userlike(models.Model):
    user = models.ForeignKey('User.Userinfo', on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey('UserPosting',on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'{self.user_id, self.post_id}'


    class Meta:
        db_table = 'userlike'





# 댓글이 달린 게시물, 댓글을 다는 사용자, 생성시간, 댓글
# 해당 댓글의 유저와 댓글이 달리는 게시물은 ForeignKey를 이용해서 이미 가입된 사람과 
# 이미 등록된 게시물로 연결해 주세요
class UserComment(models.Model):
    user_id   = models.ForeignKey('User.userinfo', on_delete=models.SET_NULL, null=True)
    image     = models.ForeignKey('UserPosting', on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    comment   = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user_id.name}'


    class Meta:
        db_table = 'usercomment'


class AdditonalComment(models.Model):
    comment    = models.ForeignKey('UserComment',on_delete=models.CASCADE)
    name       = models.ForeignKey('User.Userinfo', on_delete=models.CASCADE)
    addcomment = models.CharField(max_length=200)


