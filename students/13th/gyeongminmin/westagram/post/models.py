# autopep8: off
from django.db import models
from auth.models import Users

class Follows(models.Model):
    user_id     = models.ForeignKey(Users, related_name='user', on_delete=models.CASCADE)
    followed_by = models.ForeignKey(Users, related_name='followed_by', on_delete=models.CASCADE)

class Posts(models.Model):
    content = models.CharField(max_length=500)
    write_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def get_json(self):
        return {
            'id'         : self.id,
            'content'    : self.content,
            'write_time' : self.write_time,
            'update_time': self.update_time,
            'user_id'    : self.user_id,
            'urls'       : [{'id': url.id, 'url':url.url} for url in PostImage.objects.filter(post=self)]
        }

class PostLikes(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Comments(models.Model):
    content     = models.CharField(max_length=200)
    write_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user     = models.ForeignKey(Users, on_delete=models.CASCADE)
    post    = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

class PostImage(models.Model):
    url = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='image')
