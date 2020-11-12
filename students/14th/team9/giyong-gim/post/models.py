from django.db import models

class Post(models.Model):
    author       = models.ForeignKey('user.User', on_delete = models.CASCADE)
    title        = models.CharField(max_length = 40)
    content      = models.TextField(max_length = 400, null = True)
    image_url    = models.URLField(max_length = 200)
    created_at   = models.DateTimeField(auto_now_add = True)
    is_liked     = models.ManyToManyField('user.User', through='Like', related_name='post_like')

    class Meta:
        db_table = 'posts'


    def __str__(self):
        return self.title

class Comment(models.Model):
    author          = models.ForeignKey('user.User', on_delete = models.CASCADE)
    post            = models.ForeignKey(Post, on_delete = models.CASCADE)
    content         = models.TextField(max_length = 400)
    created_at      = models.DateTimeField(auto_now_add = True)
    parent          = models.ForeignKey('Comment', on_delete = models.SET_NULL, null = True, related_name = 'cmt_parent')

    class Meta:
        db_table ='comments'

    def __str__(self):
        return self.content

class Like(models.Model):
    user = models.ForeignKey('user.User', on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)
    # status = models.BooleanField(initial = False)

    class Meta:
        db_table = 'likes'

class Follow(models.Model):
    follower = models.ForeignKey('user.User', on_delete=models.CASCADE)
    followee = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='victim')
    # status = models.BooleanField(initial = False)

    class Meta:
        db_table = 'follows'
