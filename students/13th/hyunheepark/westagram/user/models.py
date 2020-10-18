from django.db      import models

# Create your models here.


class User(models.Model):
    name      = models.CharField(max_length=45,unique=True)
    phone     = models.CharField(max_length=30,unique=True)
    email     = models.EmailField(max_length=254,unique=True)
    password  = models.CharField(max_length=100)
    like_post = models.ManyToManyField('posting.Post',through='Like', related_name='post')

    class Meta:
        db_table = 'users'

class Like(models.Model):
    post_id = models.ForeignKey('posting.Post',on_delete=models.CASCADE)
    user_id = models.ForeignKey('User',on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes_info'
