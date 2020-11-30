from django.db import models

class Post(models.Model):
    author       = models.ForeignKey('user.User', on_delete = models.CASCADE)
    title        = models.CharField(max_length = 40)
    content      = models.TextField(max_length = 400, null = True)
    image        = models.URLField()
    post_created = models.DateTimeField(auto_now_add = True)
    is_liked = models.ManyToManyField('user.User', through='Like', related_name='post_like')

    class Meta:
        db_table = 'post'


    def __str__(self):
        return self.title

class Comment(models.Model):
    author          = models.ForeignKey('user.User', on_delete = models.CASCADE)
    post_id         = models.ForeignKey(Post, on_delete = models.CASCADE)
    content         = models.TextField(max_length = 200)
    comment_created = models.DateTimeField(auto_now_add = True)
    parent          = models.ForeignKey('Comment', on_delete = models.SET_NULL, null = True, related_name = 'cmt_parent')
    child           = models.ForeignKey('Comment', on_delete = models.SET_NULL, null = True, related_name = 'cmt_child')

    class Meta:
        db_table ='comment'

    def __str__(self):
        return self.content

class Like(models.Model):
    user = models.ForeignKey('user.User', on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)

    class Meta:
        db_table = 'likes'

class Follow(models.Model):
    follower = models.ForeignKey('user.User', on_delete=models.CASCADE)
    followee = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='victim')

    class Meta:
        db_table = 'follow'
