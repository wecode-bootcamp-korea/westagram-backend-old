from django.db import models

class User(models.Model):
    password = models.CharField(max_length=255, verbose_name='비밀번호')
    email    = models.CharField(max_length=30, verbose_name='이메일',unique=True)
    follows = models.ManyToManyField('self', through='Follow', symmetrical=False)
        
    class Meta:
        db_table            = 'users'
        verbose_name        = 'user'
        verbose_name_plural = 'users'
        ordering            = ('email',)

class Follow(models.Model):
    following  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_follows",db_column='following')
    follower   = models.ForeignKey(User,  on_delete=models.CASCADE, related_name="who_is_followed", db_column='follower')
    created_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'follows'
        verbose_name        = 'follow'
        verbose_name_plural = 'follows'
        ordering            = ('-created_dt',)