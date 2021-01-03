from django.db import models

# Create your models here.
class Post(models.Model):
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    pub_date  = models.DateTimeField(auto_now_add=True)
    likes     = models.IntegerField(default=0) 
    # likes 테이블에서 해당 포스트의 아이디로 좋아요 수를 조회해올 건데 
    # 좋아요 버튼이 눌릴 때마다 db다녀오면서 계산을 하게 될 것이고 비효율적으로 보임

    class Meta:
        db_table = 'posts'

class Image(models.Model):
    post  = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.CharField(max_length=2000)

    class Meta:
        db_table = 'images'

class Comment(models.Model):
    post     = models.ForeignKey('Post', on_delete=models.CASCADE)
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content  = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'comments'

class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
