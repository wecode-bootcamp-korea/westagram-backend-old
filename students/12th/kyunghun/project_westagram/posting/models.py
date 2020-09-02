from django.db import models

# from ..user.models import Users
# # Create your models here.

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     content = models.TextField()
#     user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    

# class Photo(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
#     image = models.TextField()
#     #image = models.ImageField(upload_to='images/', blank=True, null=True)