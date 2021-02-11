from django.db   import models
from user.models import Users

class Posts(models.Model):

    title      = models.CharField(max_length=100)
    author     = models.ForeignKey(Users,on_delete=models.CASCADE, related_name = "author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    image_url  = models.URLField(max_length=2000)
    likes      = models.ManyToManyField(Users, related_name="likers")

    class Meta:
        db_table = "posts"

class Comments(models.Model):

    author     = models.ForeignKey(Users,on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    post       = models.ForeignKey(Posts,on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"
