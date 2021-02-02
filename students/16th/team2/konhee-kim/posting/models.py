from django.db import models

class Article(models.Model):
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created   = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now=True)
    content   = models.TextField()
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table = "articles" 

class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

class Like(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"

